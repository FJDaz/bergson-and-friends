#!/usr/bin/env python3
"""
SNB API avec Modal backend
Appelle l'API Modal pour Spinoza (Qwen + LoRA)
"""

import os
import random
import httpx
from typing import List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import RAG system
from rag_system import extract_concepts, rag_lookup, format_rag_context

# Configuration Modal
MODAL_API_URL = os.environ.get(
    "MODAL_API_URL",
    "https://fjdaz--spinoza-api-chat.modal.run"  # ✅ URL Modal déployée
)

# HTTP client
http_client = httpx.Client(timeout=120.0)  # Modal peut prendre du temps au cold start

app = FastAPI(title="SNB API - Modal Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Questions du bac
QUESTIONS_BAC = {
    "spinoza": [
        "La liberté est-elle une illusion ?",
        "Suis-je esclave de mes désirs ?",
        "La raison peut-elle tout expliquer ?",
        "Peut-on être heureux en étant soumis ?",
        "La conscience est-elle source de liberté ?",
    ]
}

# Models
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[List[Any]]] = None
    philosopher: str = "spinoza"

class ChatResponse(BaseModel):
    reply: str
    history: List[List[Any]]
    contexte: str
    rag_passages: List[Dict]

class InitResponse(BaseModel):
    philosopher: str
    question: str
    greeting: str
    history: List[List[Any]]

@app.get("/")
async def root():
    return {
        "message": "SNB API (Modal Backend)",
        "modal_api": MODAL_API_URL,
        "status": "Appelle Modal serverless pour génération",
        "philosophers": ["spinoza"]
    }

@app.get("/health")
async def health():
    # Tester la connectivité à Modal
    try:
        health_url = MODAL_API_URL.replace("/chat", "/health")
        response = http_client.get(health_url, timeout=5.0)
        modal_status = "connected" if response.status_code == 200 else "disconnected"
    except Exception:
        modal_status = "disconnected"

    return {
        "status": "ok",
        "mode": "modal_serverless",
        "modal_api": MODAL_API_URL,
        "modal_status": modal_status
    }

def detecter_contexte(message: str) -> str:
    """Détecte le contexte de la réponse utilisateur"""
    message_lower = message.lower()

    if any(word in message_lower for word in ["oui", "d'accord", "exactement", "tout à fait"]):
        return "accord"
    elif any(word in message_lower for word in ["non", "pas d'accord", "faux", "erreur"]):
        return "resistance"
    elif any(word in message_lower for word in ["comprends pas", "quoi", "pourquoi", "comment"]):
        return "confusion"
    else:
        return "neutre"

async def call_modal_api(message: str, history: List[List]) -> str:
    """Appelle l'API Modal pour génération"""

    try:
        print(f"[MODAL] Appel API: {MODAL_API_URL}")

        # Convertir histoire au format Modal
        modal_history = [[h[0], h[1]] for h in history if h[0] or h[1]]

        # Appel Modal API
        response = http_client.post(
            MODAL_API_URL,
            json={
                "message": message,
                "history": modal_history,
                "max_tokens": 512,
                "temperature": 0.7,
            }
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Modal API error: {response.text}"
            )

        result = response.json()
        return result.get("reply", "")

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Timeout calling Modal API (cold start peut prendre 30-60s)"
        )
    except Exception as e:
        print(f"[MODAL] ❌ Erreur API: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Modal API error: {str(e)}"
        )

@app.post("/init/{philosopher}", response_model=InitResponse)
async def init_philosopher(philosopher: str):
    """Initialise conversation avec question du bac"""

    if philosopher not in QUESTIONS_BAC:
        raise HTTPException(status_code=404, detail=f"Philosophe {philosopher} non supporté")

    question = random.choice(QUESTIONS_BAC[philosopher])
    greeting = f"Bonjour ! Je suis Spinoza. Discutons ensemble de cette question :\n\n**{question}**\n\nQu'en penses-tu ?"

    return InitResponse(
        philosopher=philosopher,
        question=question,
        greeting=greeting,
        history=[[None, greeting]]
    )

@app.post("/chat/{philosopher}", response_model=ChatResponse)
async def chat(philosopher: str, request: ChatRequest):
    """Chat avec Modal backend"""

    print(f"[CHAT] {philosopher.upper()} - Message: {request.message[:100]}...")

    # Extract concepts et RAG lookup
    concepts = extract_concepts(request.message)
    rag_passages = rag_lookup(philosopher, concepts, top_k=3)
    rag_context = format_rag_context(rag_passages)

    # Construire message enrichi avec RAG
    enriched_message = f"{request.message}\n\n[Contexte RAG disponible: {len(rag_passages)} passages]"

    # Appeler Modal
    try:
        response = await call_modal_api(enriched_message, request.history or [])
    except HTTPException as e:
        # Fallback sur message d'erreur
        print(f"[WARN] Modal inaccessible: {e.detail}")
        response = f"Modal API temporairement indisponible. Réessaye dans quelques secondes (cold start)."

    # Détection contexte
    contexte = detecter_contexte(request.message)

    # Mise à jour historique
    history = request.history or []
    history.append([request.message, response])

    print(f"[CHAT] Réponse générée - Contexte: {contexte}")

    return ChatResponse(
        reply=response,
        history=history,
        contexte=contexte,
        rag_passages=[{"title": p["title"], "score": p["score"]} for p in rag_passages]
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    print(f"🚀 Démarrage SNB API (Modal Backend) sur port {port}...")
    print(f"📡 Modal API: {MODAL_API_URL}")
    uvicorn.run(app, host="0.0.0.0", port=port)
