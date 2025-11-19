#!/usr/bin/env python3
"""
SNB API avec HuggingFace Space Gradio backend
Appelle le Space bergsonAndFriends pour Spinoza
"""

import os
import random
import re
import httpx
from typing import List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import RAG system
from rag_system import extract_concepts, rag_lookup, format_rag_context

# Configuration
HF_SPACE_NAME = "FJDaz/bergsonAndFriends"
HF_SPACE_URL = "https://fjdaz-bergsonandfriends.hf.space"
HF_SPACE_API = f"{HF_SPACE_URL}/call"

# HTTP client pour appels directs
http_client = httpx.Client(timeout=60.0)

async def call_gradio_api(message: str, history: List[List]) -> str:
    """
    Appel direct à l'API Gradio via HTTP (bypass gradio_client)
    Utilise le endpoint /call/chat_function
    """
    try:
        print(f"[GRADIO] Appel direct API: {HF_SPACE_API}/chat_function")

        # Gradio API flow: POST /call/{fn_name} → GET /call/{fn_name}/{event_id}
        # Step 1: Initier l'appel
        response = http_client.post(
            f"{HF_SPACE_API}/chat_function",
            json={
                "data": [message, history]
            }
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Gradio API error: {response.text}"
            )

        result = response.json()
        event_id = result.get("event_id")

        if not event_id:
            raise HTTPException(status_code=500, detail="No event_id in response")

        # Step 2: Récupérer le résultat via SSE
        sse_url = f"{HF_SPACE_API}/chat_function/{event_id}"
        print(f"[GRADIO] Récupération résultat: {sse_url}")

        with http_client.stream("GET", sse_url) as sse_response:
            for line in sse_response.iter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]  # Remove "data: " prefix

                    if data_str.strip() == "":
                        continue

                    try:
                        import json
                        data = json.loads(data_str)

                        # Le dernier message contient le résultat final
                        if data.get("msg") == "process_completed":
                            output = data.get("output", {}).get("data")
                            if output and len(output) >= 2:
                                # output = [textbox_value, updated_history]
                                updated_history = output[1]
                                if updated_history and len(updated_history) > 0:
                                    return updated_history[-1][1]  # Dernière réponse assistant
                    except json.JSONDecodeError:
                        continue

        raise HTTPException(status_code=500, detail="No valid response from Gradio API")

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout calling HF Space")
    except Exception as e:
        print(f"[GRADIO] ❌ Erreur API: {e}")
        raise HTTPException(status_code=500, detail=f"Gradio API error: {str(e)}")

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
        "message": "SNB API (HF Space Mode)",
        "space": HF_SPACE_URL,
        "status": "Appelle HF Space Gradio pour génération",
        "philosophers": ["spinoza"]
    }

@app.get("/health")
async def health():
    # Tester la connectivité HTTP au Space
    try:
        response = http_client.get(f"{HF_SPACE_URL}/", timeout=5.0)
        space_status = "connected" if response.status_code == 200 else "disconnected"
    except Exception:
        space_status = "disconnected"

    return {
        "status": "ok",
        "mode": "hf_space_http",
        "space_name": HF_SPACE_NAME,
        "space_url": HF_SPACE_URL,
        "space_api": HF_SPACE_API,
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
    """Appelle le Space HF Gradio pour génération (via HTTP direct)"""

    # Convertir histoire au format Gradio
    # Format: [[user_msg, assistant_msg], ...] ou [[None, greeting]]
    gradio_history = [[h[0], h[1]] for h in history if h[0] or h[1]]

    # Appel HTTP direct à l'API Gradio
    return await call_gradio_api(message, gradio_history)

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
