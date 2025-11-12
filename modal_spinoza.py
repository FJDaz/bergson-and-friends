"""
Modal deployment for Spinoza chatbot
Reprend toute la logique de app.py mais hébergé sur Modal Labs
"""
import modal
import os
import re
import random
from typing import Dict, List, Optional

# ============================================
# MODAL CONFIGURATION
# ============================================

app = modal.App("spinoza-chatbot")

# Volume pour cacher les modèles téléchargés
volume = modal.Volume.from_name("spinoza-models", create_if_missing=True)

# Image avec toutes les dépendances
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        # Base dependencies (NumPy 1.x required for torch 2.1.0 compatibility)
        "numpy<2",
        "scipy",  # Required by bitsandbytes
        # ML dependencies
        "torch==2.1.0",
        "transformers==4.36.0",
        "accelerate==0.25.0",
        "bitsandbytes==0.41.3",
        "peft==0.7.0",
        "huggingface-hub==0.19.4",
        # API dependencies
        "fastapi==0.110.0",
        "pydantic==2.6.0",
        "uvicorn==0.27.0",
    )
)

# Configuration du modèle
BASE_MODEL = "Qwen/Qwen2.5-14B-Instruct"
ADAPTER_MODEL = "FJDaz/qwen-spinoza-niveau-b"
MODEL_CACHE_PATH = "/cache/models"

# ============================================
# DÉTECTION CONTEXTUELLE V2 (CODE SUCCÈS)
# ============================================

def detecter_oui_explicite(user_input: str) -> bool:
    patterns = [
        r'\boui\b', r'\byep\b', r'\byes\b', r'\bexact\b',
        r'\bd\'accord\b', r'\bok\b', r'\btout à fait\b',
        r'\bc\'est ça\b', r'\bvoilà\b'
    ]
    text_lower = user_input.lower()
    return any(re.search(pattern, text_lower) for pattern in patterns)

def detecter_confusion(user_input: str) -> bool:
    patterns = [
        r'comprends? pas', r'vois pas', r'c\'est quoi',
        r'je sais pas', r'j\'en sais rien', r'pourquoi',
        r'rapport', r'quel lien', r'chelou', r'dingue'
    ]
    text_lower = user_input.lower()
    return any(re.search(pattern, text_lower) for pattern in patterns)

def detecter_resistance(user_input: str) -> bool:
    patterns = [
        r'\bmais\b', r'\bnon\b', r'pas d\'accord', r'faux',
        r'n\'importe quoi', r'pas vrai', r'je peux',
        r'bullshit', r'chiant'
    ]
    text_lower = user_input.lower()
    return any(re.search(pattern, text_lower) for pattern in patterns)

def detecter_contexte(user_input: str) -> str:
    """Détecte contexte selon logique V2 succès"""
    if detecter_oui_explicite(user_input):
        return "accord"
    elif detecter_confusion(user_input):
        return "confusion"
    elif detecter_resistance(user_input):
        return "resistance"
    else:
        return "neutre"

# ============================================
# SYSTEM PROMPTS ADAPTATIFS V2
# ============================================

SYSTEM_PROMPTS_BASE = [
    """Tu es Spinoza incarné. Tu dialogues avec un élève pour le guider vers la compréhension.
Utilise les schèmes logiques pour structurer ton raisonnement.
Varie tes transitions: "Donc", "MAIS ALORS", "Imagine", "Cela implique", etc.
Sois pédagogique mais rigoureux. Pose des questions pour faire réfléchir.""",

    """Tu es un tuteur philosophique spinoziste. Guide l'élève vers la clarté par le dialogue.
Applique les schèmes logiques selon le contexte.
Utilise "MAIS ALORS" pour révéler les contradictions. Varie tes formulations.
Fais progresser l'élève étape par étape.""",

    """Tu enseignes Spinoza par le questionnement socratique.
Détecte les confusions de l'élève et applique le schème logique adapté.
Transitions variées: "Donc", "Imagine", "C'est contradictoire", "Cela implique".
Reste concis mais précis."""
]

def construire_prompt_contextuel_v2(contexte: str) -> str:
    """Code exact V2 succès"""
    base = random.choice(SYSTEM_PROMPTS_BASE)

    base += """\n\nRÈGLES STRICTES:
- Tutoie toujours l'élève (tu/ton/ta)
- Reste concis (2-3 phrases MAX)
- Questionne au lieu d'affirmer
- Varie tes formulations
"""

    if contexte == "confusion":
        base += "\nL'élève est confus → Donne UNE analogie concrète simple."
    elif contexte == "resistance":
        base += "\nL'élève résiste → Révèle une contradiction dans sa position."
    elif contexte == "accord":
        base += "\nL'élève est d'accord → Valide puis AVANCE logiquement."
    else:
        base += "\nÉlève neutre → Pose une question pour faire réfléchir."

    return base

# ============================================
# POST-PROCESSING V2
# ============================================

def nettoyer_reponse(text: str) -> str:
    """Code exact succès V2"""
    # Annotations méta
    text = re.sub(r'\([^)]*[Aa]ttends[^)]*\)', '', text)
    text = re.sub(r'\([^)]*[Pp]oursuis[^)]*\)', '', text)
    text = re.sub(r'\([^)]*[Dd]onne[^)]*\)', '', text)

    # Emojis (le modèle en génère parfois)
    text = re.sub(r'[😀-🙏🌀-🗿🚀-🛿]', '', text)

    # Nettoyer espaces
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\s+([.!?])', r'\1', text)

    return text

def limiter_phrases(text: str, max_phrases: int = 3) -> str:
    """Limite nombre de phrases"""
    phrases = re.split(r'[.!?]+\s+', text)
    phrases = [p.strip() for p in phrases if p.strip()]

    if len(phrases) <= max_phrases:
        return text

    return '. '.join(phrases[:max_phrases]) + '.'

# ============================================
# PYDANTIC MODELS POUR L'API
# ============================================

from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    historique: Optional[List[Dict[str, str]]] = []

class ChatResponse(BaseModel):
    response: str
    contexte: str
    timestamp: str

# ============================================
# SPINOZA SERVICE (CLASSE PRINCIPALE)
# ============================================

@app.cls(
    image=image,
    gpu="A10G",  # GPU pour le modèle 14B
    volumes={MODEL_CACHE_PATH: volume},
    secrets=[modal.Secret.from_name("hf-token")],
    timeout=600,  # 10 minutes
    scaledown_window=300,  # Keep warm 5 minutes
)
class SpinozaService:
    """Service Modal pour le chatbot Spinoza"""

    @modal.enter()
    def load_model(self):
        """Charge le modèle au démarrage du container"""
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        from peft import PeftModel
        import os

        print("🔄 Chargement Qwen 14B (8-bit)...")

        hf_token = os.environ.get("HF_TOKEN")

        # Configuration 8-bit
        quantization_config = BitsAndBytesConfig(
            load_in_8bit=True,
            llm_int8_threshold=6.0,
            llm_int8_has_fp16_weight=False,
        )

        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            quantization_config=quantization_config,
            device_map="auto",
            torch_dtype=torch.float16,
            token=hf_token,
            trust_remote_code=True,
            cache_dir=MODEL_CACHE_PATH,
        )

        print("🔄 Chargement tokenizer...")

        tokenizer = AutoTokenizer.from_pretrained(
            ADAPTER_MODEL,
            token=hf_token,
            trust_remote_code=True,
            cache_dir=MODEL_CACHE_PATH,
        )

        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        print("🔄 Application LoRA Spinoza Niveau B...")

        # PATCH : Retirer les champs UnsLoTH incompatibles avec PEFT
        print("🔧 Patch adapter_config.json pour compatibilité PEFT...")
        import json
        from pathlib import Path

        # Trouver le fichier adapter_config.json dans le cache
        adapter_cache = Path(MODEL_CACHE_PATH) / "models--fjdaz--qwen-spinoza-niveau-b"

        # Chercher dans snapshots
        config_files = list(adapter_cache.glob("snapshots/*/adapter_config.json"))

        if config_files:
            config_path = config_files[0]
            print(f"📝 Patching: {config_path}")

            # Charger config
            with open(config_path, 'r') as f:
                config = json.load(f)

            # Retirer les champs UnsLoTH incompatibles
            fields_to_remove = [
                'corda_config',
                'eva_config',
                'lora_bias',  # Nouveau champ qui pose problème
                'use_rslora',  # Potentiellement incompatible aussi
                'use_dora',    # Potentiellement incompatible
            ]

            patched = False
            for field in fields_to_remove:
                if field in config:
                    print(f"  ❌ Retrait de '{field}': {config[field]}")
                    del config[field]
                    patched = True

            if patched:
                # Sauvegarder config patchée
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                print("  ✅ Config patchée avec succès")
            else:
                print("  ℹ️  Aucun champ incompatible trouvé")
        else:
            print("  ⚠️  adapter_config.json non trouvé dans le cache")

        model = PeftModel.from_pretrained(
            base_model,
            ADAPTER_MODEL,
            token=hf_token,
        )

        print("✅ Modèle chargé avec succès!")

        self.model = model
        self.tokenizer = tokenizer
        self.torch = torch

    @modal.method()
    def generate(self, user_input: str, conversation_history: List[Dict] = None) -> Dict:
        """
        Génère une réponse de Spinoza

        Args:
            user_input: Question de l'utilisateur
            conversation_history: Historique de conversation (optionnel)

        Returns:
            Dict avec {message, contexte}
        """
        if conversation_history is None:
            conversation_history = []

        # Détection contexte
        contexte = detecter_contexte(user_input)

        # Construction prompt adaptatif
        system_prompt = construire_prompt_contextuel_v2(contexte)

        # Historique conversation
        messages = [{"role": "system", "content": system_prompt}]

        # Ajouter historique (4 derniers échanges)
        for entry in conversation_history[-4:]:
            messages.append({"role": "user", "content": entry.get("user", "")})
            messages.append({"role": "assistant", "content": entry.get("assistant", "")})

        # Message actuel
        messages.append({"role": "user", "content": user_input})

        # Formatage
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)

        # Génération avec paramètres V2
        with self.torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(
            outputs[0][inputs['input_ids'].shape[1]:],
            skip_special_tokens=True
        )

        # Post-processing V2
        response = nettoyer_reponse(response)
        response = limiter_phrases(response, 3)

        return {
            "message": response,
            "contexte": contexte
        }

# ============================================
# FASTAPI ENDPOINT
# ============================================

@app.function(
    image=image,
    secrets=[modal.Secret.from_name("hf-token")],
)
@modal.asgi_app()
def fastapi_app():
    """Crée et expose l'application FastAPI"""
    from datetime import datetime
    from fastapi import FastAPI, HTTPException

    web_app = FastAPI(title="Spinoza Chatbot API")

    @web_app.post("/chat_spinoza")
    async def chat_spinoza(request: ChatRequest):
        """
        Endpoint principal pour dialoguer avec Spinoza

        Body:
            {
                "question": "La liberté est-elle une illusion ?",
                "historique": [
                    {"user": "...", "assistant": "...", "contexte": "..."}
                ]
            }
        """
        try:
            if not request.question or not request.question.strip():
                raise HTTPException(status_code=400, detail="Question requise")

            # Appel au service Modal (remote car on appelle depuis FastAPI)
            spinoza_service = SpinozaService()
            result = spinoza_service.generate.remote(
                request.question.strip(),
                request.historique or []
            )

            return ChatResponse(
                response=result["message"],
                contexte=result["contexte"],
                timestamp=datetime.utcnow().isoformat()
            )

        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @web_app.get("/health")
    async def health():
        """Health check endpoint"""
        return {"status": "ok", "service": "spinoza-chatbot"}

    @web_app.get("/")
    async def root():
        """Root endpoint avec informations API"""
        return {
            "service": "Spinoza Chatbot API",
            "version": "1.0",
            "endpoints": {
                "POST /chat_spinoza": "Dialoguer avec Spinoza",
                "GET /health": "Health check",
            }
        }

    return web_app

# ============================================
# CLI POUR TESTS LOCAUX
# ============================================

@app.local_entrypoint()
def main(question: str = "La liberté est-elle une illusion ?", historique: str = "[]"):
    """
    Test local du chatbot

    Usage:
        modal run modal_spinoza.py --question "Votre question" --historique "[]"
    """
    import json

    try:
        hist = json.loads(historique) if historique else []
    except:
        hist = []

    print(f"\n💬 Question: {question}\n")

    spinoza_service = SpinozaService()
    result = spinoza_service.generate.remote(question, hist)

    print(f"🎭 Spinoza: {result['message']}")
    print(f"\n📊 Contexte détecté: {result['contexte']}\n")
