# M3 – Model Serving & Deployment Plan (Professional Workflow)

## 🎯 Syfte med uppgiften

Målet är att simulera ett professionellt arbetsflöde där:

- En tränad PyTorch-modell integreras i en applikation
- Modellen exponeras via ett REST API
- Systemet containeriseras med Docker
- Arbetet sker i team med branches och code reviews

Detta handlar INTE om att förbättra modellen.

Det handlar om:
- Integration
- Separation of concerns
- API design
- Deployment readiness
- Teamarbete

Vi bygger en production-style inference microservice.

---

# 🧠 Övergripande Arkitektur

Client  
↓  
POST /predict  
↓  
FastAPI  
↓  
Model Loader (TorchScript)  
↓  
Inference  
↓  
JSON Response  

Modellen ska laddas EN gång vid startup.

---

# 📁 Slutlig Projektstruktur

m3_model_serving/

app/
    main.py
    model_loader.py
    schemas.py

model/
    model.pt

Dockerfile
requirements.txt
README.md
MODEL_CONTEXT.md

---

# 🗺 FAS 1 – Repository Setup & Struktur

## Mål
Skapa ett rent serving-repo utan training-kod.

## Steg
- Skapa nytt GitHub-repo
- Initiera lokalt repo
- Skapa mappstruktur
- Kopiera:
    - model.pt
    - MODEL_CONTEXT.md

## Definition of Done
Repo innehåller endast serving-relaterade filer.

## Får INTE finnas
- DVC
- Dataset
- Training loop
- CIFAR-data
- Experimentkod

---

## 🔍 Sökord för att lära dig mer

- "monorepo vs microservice architecture"
- "clean architecture python"
- "separation of concerns backend"
- "production ML architecture overview"

---

# 🗺 FAS 2 – Model Export & Inference Layer

## Mål
Göra modellen production-ready via TorchScript.

## Steg
1. Exportera modell:
   torch.jit.script() eller torch.jit.trace()
2. Spara som TorchScript
3. Bygg model_loader.py:
   - Ladda modellen
   - Hantera device (CPU)
   - Konvertera input → tensor
   - Returnera prediction

## Viktiga principer
- Ingen training-kod
- Inference isolerat från API
- Modellen laddas vid startup

## Definition of Done
Kan köra inference lokalt utan FastAPI.

---

## 🔍 Sökord

- "PyTorch TorchScript tutorial"
- "torch.jit.script vs torch.jit.trace"
- "model inference best practices"
- "lazy loading vs eager loading model serving"
- "production inference optimization PyTorch"

---

# 🗺 FAS 3 – API Design (FastAPI)

## Mål
Exponera modellen via POST /predict.

## Steg
1. Skapa schemas.py (Pydantic)
   - InputSchema
   - OutputSchema

2. Skapa main.py
   - Initiera FastAPI
   - Ladda modell globalt
   - Implementera POST /predict

3. Input:
   - JSON
   - Rätt dimensioner
   - Validering

4. Output:
   - predicted_class
   - ev. probabilities

## Definition of Done
Kan anropa API via curl och få korrekt svar.

---

## 🔍 Sökord

- "FastAPI tutorial"
- "FastAPI dependency injection"
- "Pydantic request validation"
- "REST API design best practices"
- "ML model serving FastAPI"

---

# 🗺 FAS 4 – Docker & Reproducerbarhet

## Mål
Kunna bygga och köra systemet via Docker.

## Steg
1. Skapa Dockerfile
   - Base image (python:3.11-slim)
   - Installera uv
   - Installera dependencies
   - Kopiera kod
   - Exponera port 8000
   - CMD uvicorn app.main:app

2. Bygg image:
   docker build -t m3-serving .

3. Kör container:
   docker run -p 8000:8000 m3-serving

4. Testa endpoint

## Definition of Done
Containern startar och svarar korrekt.

---

## 🔍 Sökord

- "Dockerfile best practices python"
- "multi stage docker build python"
- "containerizing FastAPI"
- "uv python package manager"
- "reproducible environments Docker"

---

# 🗺 FAS 5 – Git Workflow & Samarbete

## Mål
Arbeta som ett professionellt utvecklingsteam.

## Branch-struktur

main (skyddad)

feature/model-loader  
feature/api  
feature/docker  
feature/docs  

## Workflow

1. Skapa feature branch från main
2. Implementera feature
3. Testa lokalt
4. Push branch
5. Skapa Pull Request
6. Code review
7. Merge

Inga direkta commits till main.

## Code Review ska innehålla

- Fungerar koden?
- Är strukturen tydlig?
- Finns onödig kod?
- Är separation korrekt?
- Är README uppdaterad?

---

## 🔍 Sökord

- "git flow workflow"
- "pull request code review checklist"
- "branch protection rules GitHub"
- "collaborative software development best practices"

---

# 👥 Ansvarsfördelning

## Person A – Modell & Inference

- TorchScript export
- model_loader.py
- Tensorhantering
- Prediction-logik

## Person B – API & Infrastruktur

- schemas.py
- main.py
- Dockerfile
- requirements.txt

## Båda

- Code review
- README
- Testning
- Slutverifiering i Docker

---

# 🧪 Teststrategi

Testa i tre nivåer:

1. Modell isolerat
2. API lokalt
3. API via Docker

Testa med:
- curl
- Postman
- Swagger UI

---

# 🧠 Viktiga Arkitekturprinciper

- Separation of concerns
- Single responsibility
- Reproducerbar miljö
- Minimal attack surface
- Stateless API

---

# 📦 Slutleverans ska uppfylla

- Docker build fungerar
- POST /predict returnerar korrekt prediktion
- Minst två Pull Requests finns
- README beskriver hur man kör projektet

---

# 🚀 Vad detta tränar inför verkligheten

Detta är exakt vad en ML Engineer gör:

- Tar modell från data scientist
- Gör den production-ready
- Exponerar via API
- Containeriserar
- Samarbetar via Git

Detta är skillnaden mellan:
"Jag kan träna modeller"
och
"Jag kan deploya ML-system"