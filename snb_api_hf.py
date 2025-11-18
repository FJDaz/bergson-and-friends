#!/usr/bin/env python3
"""
SNB API avec HuggingFace Space Gradio backend
Appelle le Space bergsonAndFriends pour Spinoza
"""

import os
import random
import re
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

# Import RAG system
from rag_system import extract_concepts, rag_lookup, format_rag_context

# Configuration
HF_SPACE_URL = "https://fjdaz-bergsonandfriends.hf.space"
HF_API_ENDPOINT = f"{HF_SPACE_URL}/api/predict"

app = FastAPI(title="SNB API - HF Space Bridge")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Questions du bac (même système que mock)
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
    history: Optional[List[List[Optional[str], Optional[str]]]] = None
    philosopher: str = "spinoza"

class ChatResponse(BaseModel):
    reply: str
    history: List[List[Optional[str], Optional[str]]]
    contexte: str
    rag_passages: List[Dict]

class InitResponse(BaseModel):
    philosopher: str
    question: str
    greeting: str
    history: List[List[Optional[str], Optional[str]]]

@app.get("/")
async def root():
    return {
        "message": "SNB API (HF Space Mode)",
        "space": HF_SPACE_URL,
        "status": "Appelle HF Space Gradio pour génération",
        "philosophers": ["spinoza"]
    }

@app.get("/health")
async def health():
    # Test si HF Space répond
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(HF_SPACE_URL)
            space_status = "online" if response.status_code == 200 else "paused"
    except:
        space_status = "unreachable"

    return {
        "status": "ok",
        "mode": "hf_space",
        "space_url": HF_SPACE_URL,
        "space_status": space_status
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

async def call_hf_space(message: str, history: List[List]) -> str:
    """Appelle le Space HF Gradio pour génération"""

    # Convertir histoire au format Gradio
    gradio_history = [[h[0], h[1]] for h in history if h[0] and h[1]]

    payload = {
        "data": [message, gradio_history]
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                HF_API_ENDPOINT,
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                # Gradio renvoie {"data": [result]}
                return data["data"][0]
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"HF Space error: {response.text}"
                )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="HF Space timeout - le Space est peut-être en pause"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur appel HF Space: {str(e)}"
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
    """Chat avec HF Space Gradio backend"""

    print(f"[CHAT] {philosopher.upper()} - Message: {request.message[:100]}...")

    # Extract concepts et RAG lookup
    concepts = extract_concepts(request.message)
    rag_passages = rag_lookup(philosopher, concepts, top_k=3)
    rag_context = format_rag_context(rag_passages)

    # Construire message enrichi avec RAG
    enriched_message = f"{request.message}\n\n[Contexte RAG disponible: {len(rag_passages)} passages]"

    # Appeler HF Space
    try:
        response = await call_hf_space(enriched_message, request.history or [])
    except HTTPException as e:
        # Fallback sur mock si HF Space inaccessible
        print(f"[WARN] HF Space inaccessible, fallback mock: {e.detail}")
        response = f"Le Space HF est en pause. Démarre-le sur https://huggingface.co/spaces/FJDaz/bergsonAndFriends"

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
    print(f"🚀 Démarrage SNB API (HF Space Mode) sur port {port}...")
    print(f"📡 HF Space: {HF_SPACE_URL}")
    uvicorn.run(app, host="0.0.0.0", port=port)
