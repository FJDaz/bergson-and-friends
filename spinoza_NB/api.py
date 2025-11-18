"""
API REST pour exposer les 3 philosophes via HTTP
À lancer en parallèle de Gradio
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple, Optional
import uvicorn
import random

# Import du modèle depuis app.py
from app import load_model, DialoguePhilosophe, QUESTIONS_BAC

app = FastAPI(title="Bergson & Friends API")

# CORS pour Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle au démarrage
print("🔄 Chargement du modèle pour l'API...")
model, tokenizer = load_model()
dialogue = DialoguePhilosophe(model, tokenizer)
print("✅ API prête!")

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[List[Optional[str]]]] = []
    philosopher: str  # "spinoza", "bergson", ou "kant"

class ChatResponse(BaseModel):
    answer: str
    history: List[List[Optional[str]]]
    contexte: str

class InitRequest(BaseModel):
    philosopher: str

class InitResponse(BaseModel):
    greeting: str
    question: str
    history: List[List[Optional[str]]]

@app.post("/init", response_model=InitResponse)
async def init_conversation(req: InitRequest):
    """Initialise une conversation avec un philosophe"""
    if req.philosopher not in ["spinoza", "bergson", "kant"]:
        raise HTTPException(status_code=400, detail="Philosophe invalide")

    question = random.choice(QUESTIONS_BAC[req.philosopher])
    noms = {"spinoza": "Spinoza", "bergson": "Henri Bergson", "kant": "Emmanuel Kant"}

    greeting = f"Bonjour ! Je suis {noms[req.philosopher]}. Discutons ensemble de cette question :\n\n**{question}**\n\nQu'en penses-tu ?"

    return InitResponse(
        greeting=greeting,
        question=question,
        history=[[None, greeting]]
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Dialogue avec un philosophe"""
    if req.philosopher not in ["spinoza", "bergson", "kant"]:
        raise HTTPException(status_code=400, detail="Philosophe invalide")

    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message vide")

    try:
        result = dialogue.generate_response(req.message, req.history, req.philosopher)
        response = result["message"]
        contexte = result["contexte"]

        history = req.history or []
        history.append([req.message, f"{response}\n\n*[Contexte: {contexte}]*"])

        return ChatResponse(
            answer=response,
            history=history,
            contexte=contexte
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok", "model": "SNB - Qwen 14B + LoRA Niveau B"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
