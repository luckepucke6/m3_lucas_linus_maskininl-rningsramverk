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
