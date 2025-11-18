"""
SNB API - Version Mock + RAG pour tests rapides
Sans dépendances lourdes (torch, transformers)
Réponses mock basées sur le philosophe, contexte ET passages RAG
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import random
import re
import os

# Import du système RAG
from rag_system import extract_concepts, rag_lookup, format_rag_context

# ============================================
# MODELS PYDANTIC
# ============================================

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[List[Optional[str]]]] = []
    philosopher: Optional[str] = "spinoza"

class ChatResponse(BaseModel):
    reply: str
    history: List[List[Optional[str]]]
    contexte: str
    rag_passages: Optional[List[dict]] = []  # Passages RAG utilisés

class InitResponse(BaseModel):
    philosopher: str
    question: str
    greeting: str
    history: List[List[Optional[str]]]

# ============================================
# QUESTIONS BAC
# ============================================

QUESTIONS_BAC = {
    "spinoza": [
        "La liberté est-elle une illusion ?",
        "Suis-je esclave de mes désirs ?",
        "La joie procure-t-elle un pouvoir ?",
        "Peut-on désirer sans souffrir ?",
        "La raison peut-elle tout expliquer ?"
    ],
    "bergson": [
        "Le temps passe-t-il vraiment ?",
        "Se souvenir, est-ce revivre ?",
        "L'art requiert-il de l'inspiration ?",
        "Peut-on se connaître soi-même ?",
        "La conscience fait-elle notre identité ?"
    ],
    "kant": [
        "Agir moralement, est-ce agir par devoir ?",
        "Être libre, est-ce faire ce qui nous plaît ?",
        "Que puis-je savoir du monde ?",
        "La morale est-elle universelle ?",
        "Qu'est-ce qu'une société juste ?"
    ]
}

# ============================================
# RÉPONSES MOCK PAR PHILOSOPHE
# ============================================

MOCK_RESPONSES = {
    "spinoza": [
        "Imagine : la joie augmente ta puissance d'agir, la tristesse la diminue. C'est une loi nécessaire, comme la gravité. Alors, comment les réseaux sociaux affectent-ils ta puissance ?",
        "MAIS ALORS, si tout est déterminé par des causes nécessaires, qu'est-ce que la liberté pour toi ? Réfléchis : tu dis 'je veux' mais d'où vient ce vouloir ?",
        "Donc, si la liberté = connaissance de la nécessité, plus tu comprends les causes de tes affects, plus tu es libre. Tu vois le lien avec l'éducation ?",
        "Pense à un désir qui te fait souffrir. Il naît d'une idée inadéquate, une illusion. Comment la raison peut-elle dissoudre cette illusion ?",
    ],
    "bergson": [
        "Imagine une mélodie : tu ne peux pas la diviser en instants isolés sans la détruire. C'est ça, la durée pure. Le temps de l'horloge, lui, spatialise. Tu vois la différence ?",
        "Se souvenir, ce n'est pas re-consulter une image morte. C'est revivre, avec toute ton expérience accumulée. Alors, es-tu le même qu'avant ?",
        "L'intuition ne s'oppose pas à l'intelligence : elle la complète. L'intelligence analyse, découpe. L'intuition saisit le mouvement continu. Qu'en penses-tu ?",
        "Donc, si le passé se conserve entièrement, ton présent contient tout ton passé. C'est pour ça que tu n'es jamais le même. Tu comprends l'élan vital maintenant ?",
    ],
    "kant": [
        "Distinguons : phénomène (ce que tu connais) ≠ noumène (la chose en soi). Tu ne peux connaître que les phénomènes, structurés par ton esprit. Qu'est-ce que cela implique ?",
        "Agir par devoir, c'est agir selon une maxime universalisable. Si tout le monde faisait pareil, ce serait cohérent ? Teste ta maxime.",
        "Être libre, ce n'est PAS faire ce qui te plaît (hétéronomie). C'est te donner ta propre loi (autonomie). Tu vois la différence morale ?",
        "Donc, la morale est universelle car fondée sur la raison pure pratique. L'impératif catégorique ne dépend d'aucun désir particulier. Qu'en penses-tu ?",
    ]
}

# ============================================
# DÉTECTION CONTEXTUELLE
# ============================================

def detecter_contexte(user_input: str) -> str:
    """Détecte le contexte émotionnel de la réponse"""
    text_lower = user_input.lower()

    # Accord explicite
    if any(re.search(p, text_lower) for p in [r'\boui\b', r'\bd\'accord\b', r'\bexact\b', r'\bc\'est ça\b', r'\bvoilà\b']):
        return "accord"

    # Confusion
    if any(re.search(p, text_lower) for p in [r'comprends? pas', r'je sais pas', r'c\'est quoi', r'pourquoi']):
        return "confusion"

    # Résistance
    if any(re.search(p, text_lower) for p in [r'\bmais\b', r'\bnon\b', r'pas d\'accord', r'faux', r'n\'importe quoi']):
        return "resistance"

    return "neutre"

def generate_mock_response(philosopher: str, user_message: str, contexte: str, rag_context: str = "") -> str:
    """Génère une réponse mock adaptée au philosophe, contexte ET passages RAG"""
    responses = MOCK_RESPONSES.get(philosopher, MOCK_RESPONSES["spinoza"])
    base_response = random.choice(responses)

    # Adapter selon le contexte
    if contexte == "confusion":
        prefix = "Je vois que c'est flou. "
    elif contexte == "resistance":
        prefix = "Intéressant, tu résistes. "
    elif contexte == "accord":
        prefix = "Parfait, tu commences à voir. "
    else:
        prefix = ""

    # Si RAG context disponible, mentionner l'utilisation du corpus
    if rag_context and "Passages pertinents" in rag_context:
        prefix += "[Basé sur le corpus] "

    return prefix + base_response

# ============================================
# FASTAPI APP
# ============================================

app = FastAPI(
    title="SNB API (Mock Mode)",
    description="API REST Mock pour Bergson and Friends - Tests rapides sans modèle lourd",
    version="0.1.0-mock"
)

# CORS pour permettre appels depuis Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "SNB API (Mock Mode) - Endpoints: /init/{philosopher}, /chat/{philosopher}, /health",
        "philosophers": ["spinoza", "bergson", "kant"],
        "note": "Mode MOCK activé : réponses pré-écrites, pas de modèle ML"
    }

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "mode": "mock",
        "model_loaded": False,
        "note": "Mode mock : réponses pré-écrites actives"
    }

@app.post("/init/{philosopher}", response_model=InitResponse)
async def init_philosopher(philosopher: str):
    """Initialise une conversation avec une question du bac"""
    if philosopher not in ["spinoza", "bergson", "kant"]:
        raise HTTPException(
            status_code=400,
            detail=f"Philosophe invalide: '{philosopher}'. Utilise: spinoza, bergson, ou kant"
        )

    question = random.choice(QUESTIONS_BAC[philosopher])
    noms = {
        "spinoza": "Spinoza",
        "bergson": "Henri Bergson",
        "kant": "Emmanuel Kant"
    }
    greeting = f"Bonjour ! Je suis {noms[philosopher]}. Discutons ensemble de cette question :\n\n**{question}**\n\nQu'en penses-tu ?"

    print(f"[INIT] Philosophe: {philosopher}, Question: {question[:50]}...")

    return InitResponse(
        philosopher=philosopher,
        question=question,
        greeting=greeting,
        history=[[None, greeting]]
    )

@app.post("/chat/{philosopher}", response_model=ChatResponse)
async def chat(philosopher: str, request: ChatRequest):
    """
    Endpoint de chat par philosophe
    Mode MOCK : Réponses pré-écrites adaptées au contexte
    """
    if philosopher not in ["spinoza", "bergson", "kant"]:
        raise HTTPException(
            status_code=400,
            detail=f"Philosophe invalide: '{philosopher}'"
        )

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message vide")

    # Extraction concepts pour RAG
    concepts = extract_concepts(request.message)
    print(f"[RAG] Concepts extraits: {concepts}")

    # RAG Lookup
    rag_passages = rag_lookup(philosopher, concepts, top_k=3)
    rag_context = format_rag_context(rag_passages)
    print(f"[RAG] {len(rag_passages)} passages trouvés (scores: {[p['score'] for p in rag_passages]})")

    # Détection du contexte
    contexte = detecter_contexte(request.message)

    # Génération réponse mock (avec indication RAG)
    response = generate_mock_response(philosopher, request.message, contexte, rag_context)

    # Mise à jour historique
    history = request.history or []
    history.append([request.message, f"{response}\n\n*[Contexte: {contexte} | RAG: {len(rag_passages)} passages | Mode: MOCK]*"])

    print(f"[CHAT] {philosopher.upper()} - Contexte: {contexte} - User: {request.message[:50]}...")

    return ChatResponse(
        reply=response,
        history=history,
        contexte=contexte,
        rag_passages=[{"title": p["title"], "score": p["score"]} for p in rag_passages]
    )

# Endpoints alternatifs (compatibilité)
@app.post("/chat_spinoza", response_model=ChatResponse)
async def chat_spinoza(request: ChatRequest):
    return await chat("spinoza", request)

@app.post("/chat_bergson", response_model=ChatResponse)
async def chat_bergson(request: ChatRequest):
    return await chat("bergson", request)

@app.post("/chat_kant", response_model=ChatResponse)
async def chat_kant(request: ChatRequest):
    return await chat("kant", request)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    print(f"🚀 Démarrage SNB API Mock sur port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
