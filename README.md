# M3 - Model Serving & Deployment (FastAPI + Docker)

This project serves a trained PyTorch model (from K2) through a FastAPI REST API and runs it in Docker.

## Model
- Framework: PyTorch
- Export format: TorchScript
- Task: CIFAR-10 image classification (returns class index 0-9)

## Run with Docker

Build:
```bash
docker build -t m3-serving .
docker run -p 8000:8000 m3-serving

Vi bygger med uv.lock och pyproject.toml

Länk till swagger
curl -s http://localhost:8000/docs

Länk till predict sidan i swagger.

http://localhost:8000/docs#/default/predict_predict_post
Predictions behöver korrekt antal värden/pixlar vilket är 3072. Detta för att få "200 ok" annars får mna "500 error"