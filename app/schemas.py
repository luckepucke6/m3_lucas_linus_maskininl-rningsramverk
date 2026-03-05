# Definerar hur vårt API förväntar sig att input och output ska se ut

# FastAPI använder Pydantic-modeller för:
# - Validering av inkommande data
# - Automatisk dokumentation (/docs)
# - Typ-säkerhet

from pydantic import BaseModel
from typing import List


class ImageInput(BaseModel):
# Denna klass definerar hur JSON-inputen ska se ut
    data: List[float]

class PredictionOutput(BaseModel):
# Denna klass definerar hur API:t svarar
    prediction: int