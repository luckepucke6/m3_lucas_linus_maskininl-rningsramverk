# Detta är själva API-applikationen
# Här:
# - Skapar vi FastAPI-appen
# - Laddar modellen EN gång vid startup
# - Skapar endpointen POST /predict

from fastapi import FastAPI
from app.model_loader import ModelLoader, InferenceConfig
from app.schemas import ImageInput, PredictionOutput

app = FastAPI(title="CIFAR-10 Model API",
              description="API for serving TorchScript image classification model",
              version="1.0.0"
              )

# Laddar modellen vid startup
# Detta sker när servern startar, inte per request
loader = ModelLoader(
    InferenceConfig(
        model_path="model/model_scripted.pt"
        )
        )

@app.post("/predict", response_model=PredictionOutput)

# Denna funktionen körs varje gång någon anropar.
# Detta är flödet:
# 1. FastAPI tar emot JSON
# 2. Pydantic validerar att "data" är en lista av floats
# 3. input_data blir ImageInput-objekt
# 4. Vi skickar input_data.data till ModelLoader
# 5. ModelLoader:
#   - konverterar till tensor
#   - reshapar till (1, 3, 32, 32)
#   - kör modellen
#   - returnerar predicted class
# 6. Vi returnerar ett JSON-svar
def predict(input_data: ImageInput):
    # Anropa vår inference-layer
    prediction = loader.predict_from_flat(input_data.data)

    # Returnera enligt vårt response schema
    return PredictionOutput(prediction=prediction)