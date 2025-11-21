# Créer un Space FastAPI de test sur HF

## Étapes rapides

1. **Va sur HF**: https://huggingface.co/new-space
   - Nom du Space: `spinoza_NB_fastapi` (ou autre nom)
   - SDK: **Python** (plus simple que Docker)
   - Licence: `apache-2.0`
   - Hardware: **GPU** (nécessaire pour Qwen 14B)

2. **Clone le nouveau Space**:
```bash
cd /Users/francois-jeandazin/bergsonAndFriends
git clone https://huggingface.co/spaces/FJDaz/spinoza_NB_fastapi
cd spinoza_NB_fastapi
```

3. **Copie les fichiers depuis spinoza_NB**:
```bash
cp ../spinoza_NB/app_fastapi.py app.py
cp ../spinoza_NB/requirements_fastapi.txt requirements.txt
```

4. **Crée un README.md minimal**:
```markdown
---
title: SNB FastAPI
sdk: python
app_file: app.py
---
```

5. **Commit & push**:
```bash
git add app.py requirements.txt README.md
git commit -m "Add FastAPI version of SNB"
git push
```

6. **Attends le build** (5-10 minutes pour charger le modèle)

7. **Teste l'API REST**:
```bash
curl https://fjdaz-spinoza-nb-fastapi.hf.space/health
curl -X POST https://fjdaz-spinoza-nb-fastapi.hf.space/chat_spinoza \
  -H 'Content-Type: application/json' \
  -d '{"message":"oui","history":[]}'
```

## Avantage FastAPI vs Gradio

- ✅ REST standard (pas de gradio_api)
- ✅ Asynchrone (moins de timeout)
- ✅ Documentation auto: https://fjdaz-spinoza-nb-fastapi.hf.space/docs
- ✅ Contrôle total (timeouts, erreurs, etc.)
