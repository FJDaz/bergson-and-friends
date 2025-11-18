---
title: SNB FastAPI
sdk: python
app_file: app.py
license: apache-2.0
short_description: Spinoza Niveau B - FastAPI version (test)
---

# SNB FastAPI - Version test

Version FastAPI de SNB pour tester la robustesse de l'API REST vs Gradio.

## Endpoints REST

- `GET /` - Info
- `GET /health` - Status du modèle
- `POST /init/{philosopher}` - Initialise conversation
- `POST /chat_spinoza` - Chat Spinoza
- `POST /chat_bergson` - Chat Bergson
- `POST /chat_kant` - Chat Kant
- `POST /chat/{philosophe}` - Chat universel

Documentation OpenAPI: `/docs`

