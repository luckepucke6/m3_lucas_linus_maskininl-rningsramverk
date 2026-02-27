# Gör så man kan använda moderna type hints även i äldre python versioner
from __future__ import annotations

# Används för att skapa enkel konfigurationsklass
from dataclasses import dataclass

# Ger oss säkrare filhantering
from pathlib import Path
import torch

# Konfigurations objekt
# Samlar all konfiguration för inference (inference = att använda en tränad modell för att ta beslut på ny data)
@dataclass(frozen=True)
class InferenceConfig:
    model_path: str = "model/model_scripted.pt"
    device: str = "cpu"

# ModelLoader ansvarar för:
# 1. Ladda modellen 1 gång
# 2. Konvertera input till korrekt tensor
# 3. Köra inference säkert
class ModelLoader:
    # Här laddas modellen en gång vid applikationens start
    def __init__(self, config: InferenceConfig):
        self.config = config

        # Ladda modellen
        self.model = self._load_model()

        # Modellen i eval-läge
        # Detta stänger av dropout och batchnorm-training-mode
        self.model.eval()

    # Laddar TorchScript-modellen från disk
    def _load_model(self):
        model_path = Path(self.config.model_path)

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found: {model_path.resolve()}"
            )
        
        # torch.jit.load används för torchscript modeller
        # map_location="cpu" säkerställer att modellen laddas på CPU
        model = torch.jit.load(
            str(model_path),
            map_location=self.config.device
        )

        return model
    
    # Tar emot en flattenad lista med 3072 floats.
    # CIFAR-10:
    # 3 kanaler * 32 * 32 = 3072
    # Returnerar en tensor med shape:
    # (1, 3, 32, 32)
    # 1 = batch dimension
    def _to_tensor(self, flat: list[float]) -> torch.Tensor:
        expected_length = 3 * 32 * 32

        # Input-validering (väldigt viktigt i API-system)
        if len(flat) != expected_length:
            raise ValueError(
                f"Expected {expected_length} values, got {len(flat)}"
            )

        # Skapa tensor med rätt dtype
        # float32 är standard för neural networks
        x = torch.tensor(flat, dtype=torch.float32)

        # Reshape till CNN-format
        # view ändrar bara dimensioner, kopierar inte data
        x = x.view(1, 3, 32, 32)

        return x
    
    
    # Huvudmetod som API:t kommer anropa.
    # 1) Konverterar input till tensor
    # 2) Kör modellen
    # 3) Returnerar predicted class index (0–9)
    def predict_from_flat(self, flat: list[float]) -> int:

        # Konvertera input
        x = self._to_tensor(flat)

        # no_grad():
        # Stänger av gradient-beräkning.
        # Sparar minne och gör inference snabbare.
        with torch.no_grad():

            # Modellens output = logits (råa värden)
            logits = self.model(x)

            # argmax hittar klassen med högst värde
            # dim=1 = över klassdimensionen
            predicted_class = torch.argmax(logits, dim=1).item()

        # Säkerställ att vi returnerar en vanlig Python-int
        return int(predicted_class)