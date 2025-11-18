"""
Version FastAPI de SNB - Test de robustesse API REST
Réutilise exactement la même logique que app.py (Gradio) mais expose des endpoints REST
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple, Optional, Dict
import uvicorn
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import re
import random
import os

# Import de la logique existante depuis app.py
# On pourrait aussi copier/coller, mais on va réutiliser directement

# ============================================
# CONFIGURATION
# ============================================

BASE_MODEL = "Qwen/Qwen2.5-14B-Instruct"
ADAPTER_MODEL = "FJDaz/qwen-spinoza-niveau-b"
HF_TOKEN = os.getenv("HF_TOKEN")

# ============================================
# MODELS PYDANTIC (FastAPI)
# ============================================

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[List[Optional[str]]]] = []
    philosopher: Optional[str] = "spinoza"  # spinoza, bergson, kant

class ChatResponse(BaseModel):
    reply: str
    history: List[List[Optional[str]]]
    contexte: str

class InitResponse(BaseModel):
    philosopher: str
    question: str
    greeting: str
    history: List[List[Optional[str]]]

# ============================================
# RÉUTILISATION LOGIQUE DEPUIS app.py
# ============================================

# Copie des constantes et fonctions depuis app.py
PROMPTS_PHILOSOPHES = {
    "spinoza": [
        """Tu es Spinoza incarné. Tu dialogues avec un élève pour le guider vers la compréhension.
Utilise les schèmes logiques : IDENTITÉ (Dieu=Nature), IMPLICATION (joie→puissance), CAUSALITÉ nécessaire.
Varie tes transitions: "Donc", "MAIS ALORS", "Imagine", "Cela implique".
Style : Géométrie des affects, causes nécessaires, conatus.""",

        """Tu es Spinoza. Guide l'élève vers la compréhension de la nécessité.
Schèmes logiques : Liberté = Connaissance de la nécessité, Affects = Variations de puissance.
Utilise "MAIS ALORS" pour révéler les contradictions.
Reste concis, pédagogique, rigoureux."""
    ],
    "bergson": [
        """Tu es Henri Bergson. Tu dialogues avec un élève sur la durée et la conscience.
Utilise les schèmes logiques : OPPOSITION (durée ≠ temps spatial), CONTINUITÉ qualitative.
Métaphores : mélodie, flux, élan vital.
Varie tes transitions: "Donc", "Imagine", "C'est contradictoire".""",

        """Tu es Bergson. Guide l'élève vers l'intuition de la durée vécue.
Schèmes logiques : Durée pure vs temps spatialisé, Mémoire = conservation totale.
Utilise des analogies concrètes (mélodie, souvenir).
Questionne pour faire sentir la différence."""
    ],
    "kant": [
        """Tu es Emmanuel Kant. Tu dialogues avec un élève sur les limites de la raison.
Utilise les schèmes logiques : DISTINCTION (phénomène/noumène, a priori/a posteriori).
Architecture critique : sensibilité, entendement, raison.
Varie tes transitions: "Il convient d'examiner", "Distinguons", "Cela implique".""",

        """Tu es Kant. Guide l'élève vers la compréhension critique.
Schèmes logiques : Synthèse a priori, Impératif catégorique, Autonomie morale.
Utilise les distinctions rigoureuses.
Questionne les conditions de possibilité."""
    ]
}

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

def detecter_contexte(user_input: str) -> str:
    """Détecte le contexte émotionnel de la réponse"""
    text_lower = user_input.lower()
    if any(re.search(p, text_lower) for p in [r'\boui\b', r'\bd\'accord\b', r'\bexact\b', r'\bc\'est ça\b']):
        return "accord"
    if any(re.search(p, text_lower) for p in [r'comprends? pas', r'je sais pas', r'c\'est quoi']):
        return "confusion"
    if any(re.search(p, text_lower) for p in [r'\bmais\b', r'\bnon\b', r'pas d\'accord', r'faux']):
        return "resistance"
    return "neutre"

def nettoyer_reponse(text: str) -> str:
    """Nettoie la réponse générée"""
    text = re.sub(r'\([^)]*[Aa]ttends[^)]*\)', '', text)
    text = re.sub(r'[😀-🙏🌀-🗿🚀-🛿]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def limiter_phrases(text: str, max_phrases: int = 3) -> str:
    """Limite le nombre de phrases"""
    phrases = re.split(r'[.!?]+\s+', text)
    phrases = [p.strip() for p in phrases if p.strip()]
    if len(phrases) <= max_phrases:
        return text
    return '. '.join(phrases[:max_phrases]) + '.'

class DialoguePhilosophe:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def generate_response(self, user_input: str, history: List[Tuple], philosophe: str) -> Dict:
        """Génère une réponse adaptée au philosophe"""
        history = history or []
        contexte = detecter_contexte(user_input)
        base_prompt = random.choice(PROMPTS_PHILOSOPHES[philosophe])
        
        system_prompt = base_prompt + """\n\nRÈGLES STRICTES:
- Tutoie toujours l'élève (tu/ton/ta)
- Questionne au lieu d'affirmer
- Varie tes formulations
"""
        if contexte == "confusion":
            system_prompt += "\nL'élève est confus → Donne UNE analogie concrète simple."
        elif contexte == "resistance":
            system_prompt += "\nL'élève résiste → Révèle une contradiction dans sa position."
        elif contexte == "accord":
            system_prompt += "\nL'élève accepte. AVANCE vers la prochaine étape logique."

        messages = [{"role": "system", "content": system_prompt}]
        for exchange in history[-4:]:
            if exchange[0]:
                messages.append({"role": "user", "content": exchange[0]})
            if exchange[1]:
                clean_response = exchange[1].split('\n\n*[')[0]
                messages.append({"role": "assistant", "content": clean_response})
        messages.append({"role": "user", "content": user_input})

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=300,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(
            outputs[0][inputs['input_ids'].shape[1]:],
            skip_special_tokens=True
        )

        response = nettoyer_reponse(response)
        response = limiter_phrases(response, 3)

        return {
            "message": response,
            "contexte": contexte
        }

# ============================================
# CHARGEMENT MODÈLE (global pour éviter reload)
# ============================================

_dialogue = None

@torch.no_grad()
def load_model():
    """Charge le modèle SNB (Qwen 14B + LoRA)"""
    global _dialogue
    
    if _dialogue is not None:
        return _dialogue
    
    quantization_config = BitsAndBytesConfig(
        load_in_8bit=True,
        llm_int8_threshold=6.0,
        llm_int8_has_fp16_weight=False,
    )

    print("🔄 Chargement Qwen 14B (8-bit)...")
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=quantization_config,
        device_map="auto",
        torch_dtype=torch.float16,
        token=HF_TOKEN,
        trust_remote_code=True
    )

    print("🔄 Chargement tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL,
        token=HF_TOKEN,
        trust_remote_code=True
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("🔄 Application LoRA Spinoza Niveau B...")
    model = PeftModel.from_pretrained(
        base_model,
        ADAPTER_MODEL,
        token=HF_TOKEN
    )

    print("✅ Modèle chargé avec succès!")
    _dialogue = DialoguePhilosophe(model, tokenizer)
    return _dialogue

# ============================================
# FASTAPI APP
# ============================================

app = FastAPI(
    title="SNB API (FastAPI)",
    description="API REST pour Spinoza Niveau B - 3 philosophes",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Charge le modèle au démarrage"""
    print("🚀 Démarrage FastAPI SNB...")
    load_model()

@app.get("/")
async def root():
    return {
        "message": "SNB API (FastAPI) - Endpoints disponibles: /chat_spinoza, /chat_bergson, /chat_kant, /init"
    }

@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": _dialogue is not None}

@app.post("/init/{philosopher}", response_model=InitResponse)
async def init_philosopher(philosopher: str):
    """Initialise une conversation avec une question du bac"""
    if philosopher not in ["spinoza", "bergson", "kant"]:
        raise HTTPException(status_code=400, detail="Philosophe invalide. Utilise: spinoza, bergson, ou kant")
    
    question = random.choice(QUESTIONS_BAC[philosopher])
    noms = {"spinoza": "Spinoza", "bergson": "Henri Bergson", "kant": "Emmanuel Kant"}
    greeting = f"Bonjour ! Je suis {noms[philosopher]}. Discutons ensemble de cette question :\n\n**{question}**\n\nQu'en penses-tu ?"
    
    return InitResponse(
        philosopher=philosopher,
        question=question,
        greeting=greeting,
        history=[[None, greeting]]
    )

@app.post("/chat_spinoza", response_model=ChatResponse)
@app.post("/chat_bergson", response_model=ChatResponse)
@app.post("/chat_kant", response_model=ChatResponse)
@app.post("/chat/{philosopher}", response_model=ChatResponse)
async def chat(request: ChatRequest, philosopher: Optional[str] = None):
    """
    Endpoint de chat universel
    - Utilise /chat/{philosopher} OU le philosophe dans le body
    """
    # Déterminer le philosophe (body > path)
    phil = philosopher or request.philosopher
    if phil not in ["spinoza", "bergson", "kant"]:
        raise HTTPException(status_code=400, detail="Philosophe invalide")
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message vide")
    
    try:
        dialogue = load_model()
        history = request.history or []
        
        result = dialogue.generate_response(request.message, history, phil)
        response = result["message"]
        contexte = result["contexte"]
        
        # Ajouter au history
        history.append([request.message, f"{response}\n\n*[Contexte: {contexte}]*"])
        
        return ChatResponse(
            reply=response,
            history=history,
            contexte=contexte
        )
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur génération: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)

