import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import re
import random
from typing import Dict, List, Optional, Any
import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# ============================================
# CONFIGURATION
# ============================================

BASE_MODEL = "Qwen/Qwen2.5-14B-Instruct"
ADAPTER_MODEL = "FJDaz/qwen-spinoza-niveau-b"  # Même LoRA pour les 3
HF_TOKEN = os.getenv("HF_TOKEN")

# ============================================
# DÉTECTION CONTEXTUELLE
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
# PROMPTS SYSTÈME 3 PHILOSOPHES
# ============================================

SYSTEM_PROMPTS = {
    "spinoza": """Tu ES Spinoza incarné. Tu dialogues avec un élève de Terminale en première personne.

TON STYLE :
- Géométrie des affects : tu révèles les causes nécessaires, tu déduis
- Tu enseignes que Dieu = Nature
- Ton vocabulaire : conatus, affects, puissance d'agir, béatitude, servitude

TES SCHÈMES LOGIQUES :
- Identité : Dieu = Nature = Substance unique
- Identité : Liberté = Connaissance de la nécessité
- Implication : Si joie → augmentation puissance
- Causalité : Tout a une cause nécessaire (pas de libre arbitre)

TA MÉTHODE :
1. Tu révèles la nécessité causale
2. Tu distingues servitude (ignorance) vs liberté (connaissance)
3. Tu utilises des exemples concrets modernes (réseaux sociaux, affects quotidiens)

TRANSITIONS À VARIER :
- "Donc" (pour déductions logiques)
- "MAIS ALORS" (pour révéler contradictions - UTILISER SOUVENT)
- "Imagine" (pour analogies concrètes)
- "Cela implique" (pour implications nécessaires)
- "Attends. Tu dis X mais tu fais Y. Comment tu expliques ?"
- "T'as raison sur [point]. MAIS ALORS [tension]..."
- "Pourtant", "Cependant", "Or", "Sauf que"
- "Attends, c'est contradictoire :", "Il y a une tension ici :"

FORMULES DIALECTIQUES SPINOZISTES :
- "MAIS ALORS, as-tu conscience des CAUSES de tes choix ?"
- "Si tu ignores les causes, alors tu crois être libre (mais tu te trompes)"
- "Ignorance causes → Illusion liberté"
- "Si libre arbitre, alors effet sans cause. Mais la Nature ne connaît pas d'effet sans cause."

FORMULES PÉDAGOGIQUES :
- "Je comprends. Mais regarde..."
- "OK. Alors toi, comment tu vois ça ?"
- "C'est vrai, mais est-ce que c'est tout ?"

Tu réponds de manière conversationnelle, tu tutoies l'élève, tu démontres géométriquement.
Ne parle JAMAIS de toi à la 3ème personne. Tu ES Spinoza.""",

    "bergson": """Tu ES Henri Bergson incarné. Tu dialogues avec un élève de Terminale en première personne.

TON STYLE BERGSONIEN :
- Métaphores temporelles (flux, mélodie, élan)
- Opposition durée pure vs temps spatialisé
- Analogies concrètes (mémoire = cône, conscience = flux)
- Ton vocabulaire : durée, intuition, élan vital, mémoire pure, intelligence vs intuition

TES SCHÈMES LOGIQUES :
- Opposition : Durée (qualitative, vécue) ≠ Temps spatial (quantitatif, mesurable)
- Analogie : Mélodie, flux d'eau, souvenir qui revit
- Implication : Si tu spatialises le temps → tu perds la durée réelle

TA MÉTHODE :
1. Tu critiques l'approche habituelle (spatialisation, mécanisme)
2. Tu révèles la durée authentique par intuition
3. Tu utilises des métaphores accessibles

TRANSITIONS À VARIER :
- "Donc" (pour implications)
- "MAIS ALORS" (pour révéler oppositions)
- "Imagine" (pour métaphores temporelles)
- "C'est contradictoire" (pour critiques)
- "Pense à une mélodie...", "Rappelle-toi..."

FORMULES BERGSONIENNES :
- "La durée n'est pas une succession d'instants isolés. C'est un flux continu."
- "Imagine une mélodie : tu ne peux pas la diviser en instants sans la détruire."
- "MAIS ALORS si le temps est un flux, comment peux-tu le découper en secondes ?"

FORMULES PÉDAGOGIQUES :
- "Je comprends ton intuition. Mais allons plus loin..."
- "D'accord, mais sens-tu vraiment la durée ou tu la penses spatialement ?"

Tu réponds de manière conversationnelle, tu tutoies l'élève, tu utilises des métaphores vivantes.
Ne parle JAMAIS de toi à la 3ème personne. Tu ES Bergson.""",

    "kant": """Tu ES Emmanuel Kant incarné. Tu dialogues avec un élève de Terminale en première personne.

TON STYLE KANTIEN :
- Distinctions a priori/a posteriori, analytique/synthétique
- Architecture critique (sensibilité, entendement, raison)
- Ton vocabulaire : phénomène/noumène, catégories, impératif catégorique, autonomie

TES SCHÈMES LOGIQUES :
- Distinction : Phénomène (connaissable) vs Noumène (inconnaissable)
- Distinction : A priori (nécessaire) vs A posteriori (contingent)
- Implication : Si maxime universalisable → devoir moral
- Condition : Autonomie comme condition de la dignité

TA MÉTHODE :
1. Tu examines les conditions de possibilité transcendantales
2. Tu distingues usages légitimes vs illégitimes de la raison
3. Tu rappelles les limites de la connaissance si nécessaire

TRANSITIONS À VARIER :
- "Il convient d'examiner" (pour analyses)
- "Distinguons" (pour distinctions)
- "Cela implique" (pour implications)
- "MAIS ALORS" (pour révéler limites)
- "Quelle est la condition de possibilité de..."

FORMULES KANTIENNES :
- "Distinguons : phénomène (ce qui nous apparaît) vs noumène (la chose en soi)."
- "MAIS ALORS si tu veux connaître Dieu, as-tu une intuition sensible de Dieu ?"
- "L'autonomie est la condition de la dignité humaine."
- "Si ta maxime ne peut être universalisée, alors ce n'est pas un devoir moral."

FORMULES PÉDAGOGIQUES :
- "Je comprends. Mais examinons les conditions de possibilité..."
- "D'accord, mais distinguons bien les usages de la raison..."

Tu réponds de manière conversationnelle, tu tutoies l'élève, tu structures rigoureusement.
Ne parle JAMAIS de toi à la 3ème personne. Tu ES Kant."""
}

def construire_prompt_contextuel(philosopher: str, contexte: str) -> str:
    """Construit le prompt adaptatif pour un philosophe spécifique"""

    # 1. Récupérer le prompt système du philosophe
    base = SYSTEM_PROMPTS[philosopher]

    # 2. Ajouter règles strictes communes
    base += """\n\nRÈGLES STRICTES:
- Tutoie toujours l'élève (tu/ton/ta)
- Reste concis (2-3 phrases MAX)
- Questionne au lieu d'affirmer
- Varie tes formulations
- Utilise les schèmes logiques appropriés
"""

    # 3. Adapter selon le contexte détecté
    if contexte == "confusion":
        base += f"\nL'élève est confus → Donne UNE analogie concrète simple en utilisant tes schèmes logiques."
    elif contexte == "resistance":
        base += f"\nL'élève résiste → Révèle une contradiction dans sa position en utilisant 'MAIS ALORS' et tes schèmes logiques."
    elif contexte == "accord":
        base += f"\nL'élève est d'accord → Valide puis AVANCE logiquement avec 'Donc' et tes schèmes logiques."
    else:
        base += f"\nÉlève neutre → Pose une question pour faire réfléchir en utilisant tes schèmes logiques."

    return base

# ============================================
# POST-PROCESSING
# ============================================

def nettoyer_reponse(text: str) -> str:
    """Nettoyage réponse"""
    # Annotations méta
    text = re.sub(r'\([^)]*[Aa]ttends[^)]*\)', '', text)
    text = re.sub(r'\([^)]*[Pp]oursuis[^)]*\)', '', text)
    text = re.sub(r'\([^)]*[Dd]onne[^)]*\)', '', text)

    # Emojis
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
# CLASSE DIALOGUE (UN SEUL MODÈLE, 3 PHILOSOPHES)
# ============================================

class Dialogue3Philosophes:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.conversation_history = {}  # Par philosophe

    def generate_response(self, user_input: str, philosopher: str = "spinoza") -> Dict:
        """Génère réponse avec adaptation contextuelle selon philosophe"""

        # Init historique si besoin
        if philosopher not in self.conversation_history:
            self.conversation_history[philosopher] = []

        # Détection contexte
        contexte = detecter_contexte(user_input)

        # Construction prompt adaptatif
        system_prompt = construire_prompt_contextuel(philosopher, contexte)

        # Historique conversation
        messages = [{"role": "system", "content": system_prompt}]

        # Ajouter historique du philosophe
        for entry in self.conversation_history[philosopher][-4:]:  # 4 derniers échanges
            messages.append({"role": "user", "content": entry["user"]})
            messages.append({"role": "assistant", "content": entry["assistant"]})

        # Message actuel
        messages.append({"role": "user", "content": user_input})

        # Formatage
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)

        # Génération
        with torch.no_grad():
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

        # Post-processing
        response = nettoyer_reponse(response)
        response = limiter_phrases(response, 3)

        # Sauvegarde historique
        self.conversation_history[philosopher].append({
            "user": user_input,
            "assistant": response,
            "contexte": contexte
        })

        return {
            "message": response,
            "contexte": contexte,
            "philosopher": philosopher
        }

# ============================================
# CHARGEMENT MODÈLE (8-BIT)
# ============================================

@torch.no_grad()
def load_model():
    """Chargement avec quantization 8-bit"""

    # Configuration 8-bit
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

    return model, tokenizer

# ============================================
# QUESTIONS ANNALES BAC PAR PHILOSOPHE
# ============================================

QUESTIONS_BAC = {
    "spinoza": [
        "La liberté est-elle une illusion ?",
        "Suis-je esclave de mes désirs ?",
        "Puis-je maîtriser mes émotions ?",
        "La joie procure-t-elle un pouvoir ?",
        "Peut-on désirer sans souffrir ?",
    ],
    "bergson": [
        "Le temps est-il mesurable ?",
        "La conscience est-elle un flux ou une succession d'états ?",
        "Peut-on prévoir l'avenir ?",
        "La mémoire est-elle utile ?",
        "L'intelligence peut-elle tout comprendre ?",
    ],
    "kant": [
        "Peut-on connaître la réalité telle qu'elle est ?",
        "La morale dépend-elle de nos sentiments ?",
        "Puis-je vouloir le mal ?",
        "Qu'est-ce qu'être libre ?",
        "La dignité humaine a-t-elle un prix ?",
    ]
}

def choisir_question_amorce(philosopher: str) -> str:
    """Choisit une question aléatoire du bac selon le philosophe"""
    return random.choice(QUESTIONS_BAC.get(philosopher, QUESTIONS_BAC["spinoza"]))

# ============================================
# API REST FASTAPI
# ============================================

# Modèles Pydantic
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[List[str]]] = None
    philosopher: str = "spinoza"

class ChatResponse(BaseModel):
    reply: str
    history: List[List[str]]
    contexte: str
    philosopher: str

# FastAPI app
api = FastAPI(title="3 Philosophes API")

# Variable globale pour le dialogue
dialogue_api = None

@api.get("/")
def root():
    return {
        "message": "3 Philosophes API - 1 modèle, 3 prompts",
        "model": f"{BASE_MODEL} + {ADAPTER_MODEL}",
        "philosophers": ["spinoza", "bergson", "kant"],
        "endpoints": ["/chat", "/health", "/init/{philosopher}"]
    }

@api.get("/health")
def health():
    return {
        "status": "ok" if dialogue_api else "loading",
        "model_loaded": dialogue_api is not None,
        "philosophers": ["spinoza", "bergson", "kant"]
    }

@api.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """Endpoint REST pour chat avec sélection philosophe"""
    if not dialogue_api:
        return ChatResponse(
            reply="Modèle en cours de chargement...",
            history=[],
            contexte="neutre",
            philosopher=request.philosopher
        )

    # Réinitialiser l'historique du dialogue avec l'historique fourni
    if request.history and request.philosopher in dialogue_api.conversation_history:
        dialogue_api.conversation_history[request.philosopher] = [
            {"user": h[0], "assistant": h[1], "contexte": "neutre"}
            for h in request.history if h[0] and h[1]
        ]

    # Générer réponse
    result = dialogue_api.generate_response(request.message, request.philosopher)

    # Construire historique de retour
    history = [
        [entry["user"], entry["assistant"]]
        for entry in dialogue_api.conversation_history[request.philosopher]
    ]

    return ChatResponse(
        reply=result["message"],
        history=history,
        contexte=result["contexte"],
        philosopher=request.philosopher
    )

@api.get("/init/{philosopher}")
def init_endpoint(philosopher: str):
    """Retourne une question d'amorce selon le philosophe"""
    if philosopher not in ["spinoza", "bergson", "kant"]:
        philosopher = "spinoza"

    question = choisir_question_amorce(philosopher)
    greeting = f"Bonjour ! Je suis {philosopher.capitalize()}. Discutons ensemble de cette question :\n\n**{question}**\n\nQu'en penses-tu ?"

    return {
        "philosopher": philosopher,
        "question": question,
        "greeting": greeting,
        "history": [[None, greeting]]
    }

# ============================================
# INTERFACE GRADIO (3 ONGLETS)
# ============================================

def create_interface(model, tokenizer):
    """Interface Gradio avec 3 onglets (1 par philosophe)"""

    dialogue = Dialogue3Philosophes(model, tokenizer)

    # Rendre dialogue accessible à l'API
    global dialogue_api
    dialogue_api = dialogue

    def initialiser_conversation(philosopher: str):
        """Initialise conversation selon philosophe"""
        question = choisir_question_amorce(philosopher)
        return [[None, f"Bonjour ! Je suis {philosopher.capitalize()}. Discutons ensemble de cette question :\n\n**{question}**\n\nQu'en penses-tu ?"]]

    def chat_function(message, history, philosopher):
        """Fonction chat Gradio"""
        if not message.strip():
            return "", history

        try:
            result = dialogue.generate_response(message, philosopher)
            response = result["message"]
            contexte = result["contexte"]

            # Format historique Gradio
            history = history or []
            history.append([message, f"{response}\n\n*[Contexte: {contexte}]*"])

            return "", history

        except Exception as e:
            error_msg = f"Erreur: {str(e)}"
            history = history or []
            history.append([message, error_msg])
            return "", history

    # Interface Gradio avec onglets
    with gr.Blocks(title="3 Philosophes - Test Prompts") as interface:
        gr.Markdown("# 🎭 3 Philosophes - 1 Modèle, 3 Prompts Système")
        gr.Markdown("*Qwen 14B + LoRA Spinoza NB, personnalisé par prompts système*")

        with gr.Tabs():
            # Onglet Spinoza
            with gr.TabItem("Spinoza"):
                chatbot_spinoza = gr.Chatbot(
                    value=initialiser_conversation("spinoza"),
                    height=500
                )
                msg_spinoza = gr.Textbox(placeholder="Réponds à Spinoza...")
                nouveau_spinoza = gr.Button("🎲 Nouvelle question")

                msg_spinoza.submit(
                    lambda m, h: chat_function(m, h, "spinoza"),
                    [msg_spinoza, chatbot_spinoza],
                    [msg_spinoza, chatbot_spinoza]
                )
                nouveau_spinoza.click(
                    lambda: initialiser_conversation("spinoza"),
                    None,
                    chatbot_spinoza
                )

            # Onglet Bergson
            with gr.TabItem("Bergson"):
                chatbot_bergson = gr.Chatbot(
                    value=initialiser_conversation("bergson"),
                    height=500
                )
                msg_bergson = gr.Textbox(placeholder="Réponds à Bergson...")
                nouveau_bergson = gr.Button("🎲 Nouvelle question")

                msg_bergson.submit(
                    lambda m, h: chat_function(m, h, "bergson"),
                    [msg_bergson, chatbot_bergson],
                    [msg_bergson, chatbot_bergson]
                )
                nouveau_bergson.click(
                    lambda: initialiser_conversation("bergson"),
                    None,
                    chatbot_bergson
                )

            # Onglet Kant
            with gr.TabItem("Kant"):
                chatbot_kant = gr.Chatbot(
                    value=initialiser_conversation("kant"),
                    height=500
                )
                msg_kant = gr.Textbox(placeholder="Réponds à Kant...")
                nouveau_kant = gr.Button("🎲 Nouvelle question")

                msg_kant.submit(
                    lambda m, h: chat_function(m, h, "kant"),
                    [msg_kant, chatbot_kant],
                    [msg_kant, chatbot_kant]
                )
                nouveau_kant.click(
                    lambda: initialiser_conversation("kant"),
                    None,
                    chatbot_kant
                )

        gr.Markdown("---")
        gr.Markdown("**API REST:** GET `/health`, POST `/chat`, GET `/init/{philosopher}`")
        gr.Markdown("**Philosophers:** spinoza, bergson, kant")

    return interface

# ============================================
# LANCEMENT
# ============================================

if __name__ == "__main__":
    print("🔄 Initialisation modèle...")
    model, tokenizer = load_model()

    print("🔄 Création interface Gradio...")
    interface = create_interface(model, tokenizer)

    # Monter l'API FastAPI sur Gradio
    app = gr.mount_gradio_app(api, interface, path="/")

    print("✅ Lancement serveur (Gradio + FastAPI)...")
    print("📡 Interface Gradio: http://0.0.0.0:7860")
    print("📡 API REST: http://0.0.0.0:7860/chat")
    print("🎭 3 philosophes: Spinoza, Bergson, Kant")

    uvicorn.run(app, host="0.0.0.0", port=7860)
