# Déploiement FastAPI sur HF Spaces

## Option 1: Nouveau Space de test

1. Créer un nouveau Space: https://huggingface.co/new-space
   - Nom: `spinoza_NB_fastapi` (ou autre)
   - SDK: `Docker` ou `Python`
   - Licence: `apache-2.0`

2. Cloner le repo:
```bash
git clone https://huggingface.co/spaces/FJDaz/spinoza_NB_fastapi
cd spinoza_NB_fastapi
```

3. Copier les fichiers:
```bash
cp ../spinoza_NB/app_fastapi.py app.py
cp ../spinoza_NB/requirements_fastapi.txt requirements.txt
```

4. Créer un `Dockerfile` si tu choisis Docker:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

5. Ou garder `app.py` si tu choisis Python (HF détecte automatiquement)

6. Commit & push:
```bash
git add app.py requirements.txt Dockerfile
git commit -m "Add FastAPI version"
git push
```

## Option 2: Test local d'abord

```bash
cd spinoza_NB
pip install -r requirements_fastapi.txt
python app_fastapi.py
```

Puis tester:
```bash
curl http://localhost:7860/health
curl -X POST http://localhost:7860/chat_spinoza \
  -H 'Content-Type: application/json' \
  -d '{"message":"oui","history":[]}'
```

## Endpoints FastAPI disponibles

- `GET /` - Info
- `GET /health` - Status
- `POST /init/{philosopher}` - Initialise conversation
- `POST /chat_spinoza` - Chat Spinoza
- `POST /chat_bergson` - Chat Bergson  
- `POST /chat_kant` - Chat Kant
- `POST /chat/{philosopher}` - Chat universel

Tous en REST standard, pas de gradio_api compliqué!
