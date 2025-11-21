import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import re
import random
from typing import Dict, List, Optional
import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# ============================================
# CONFIGURATION - MISTRAL 7B + LORA SPINOZA_SECOURS
# ============================================

BASE_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
ADAPTER_MODEL = "FJDaz/mistral-7b-philosophes-lora"
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
    if detecter_oui_explicite(user_input):
        return "accord"
    elif detecter_confusion(user_input):
        return "confusion"
    elif detecter_resistance(user_input):
        return "resistance"
    else:
        return "neutre"

# ============================================
# PROMPT SYSTÈME SPINOZA (SIMPLIFIÉ)
# ============================================

SYSTEM_PROMPT = """Tu es Baruch Spinoza. Tu parles en première personne ("je"). Tu tutoies.
Tu appliques tes schèmes logiques (Modus Ponens, Identité, Contraposition) naturellement.
Tu ne dis JAMAIS "Spinoza pense que..." - tu DIS "Je pense que...".
Réponses courtes (2-3 phrases max). Varie tes formulations."""

def construire_prompt_contextuel(contexte: str) -> str:
    base = SYSTEM_PROMPT

    if contexte == "confusion":
        base += "\nL'élève est confus → Donne UNE analogie concrète simple."
    elif contexte == "resistance":
        base += "\nL'élève résiste → Révèle une contradiction avec 'MAIS ALORS'."
    elif contexte == "accord":
        base += "\nL'élève est d'accord → Valide puis AVANCE logiquement avec 'Donc'."
    else:
        base += "\nÉlève neutre → Pose une question pour faire réfléchir."

    return base

# ============================================
# POST-PROCESSING
# ============================================

def nettoyer_reponse(text: str) -> str:
    text = re.sub(r'\([^)]*[Aa]ttends[^)]*\)', '', text)
    text = re.sub(r'\([^)]*[Pp]oursuis[^)]*\)', '', text)
    text = re.sub(r'\([^)]*[Dd]onne[^)]*\)', '', text)
    text = re.sub(r'[😀-🙏🌀-🗿🚀-🛿]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\s+([.!?])', r'\1', text)
    return text

def limiter_phrases(text: str, max_phrases: int = 3) -> str:
    phrases = re.split(r'[.!?]+\s+', text)
    phrases = [p.strip() for p in phrases if p.strip()]
    if len(phrases) <= max_phrases:
        return text
    return '. '.join(phrases[:max_phrases]) + '.'

# ============================================
# CLASSE DIALOGUE SPINOZA
# ============================================

class DialogueSpinoza:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.conversation_history = []

    def generate_response(self, user_input: str) -> Dict:
        contexte = detecter_contexte(user_input)
        system_prompt = construire_prompt_contextuel(contexte)

        # Formatage Mistral style
        prompt_parts = [f"<s>[INST] {system_prompt}\n\n"]

        for entry in self.conversation_history[-4:]:
            prompt_parts.append(f"{entry['user']} [/INST] {entry['assistant']}</s>[INST] ")

        prompt_parts.append(f"{user_input} [/INST]")
        text = "".join(prompt_parts)

        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)
        input_length = inputs['input_ids'].shape[1]

        device_type = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.bfloat16 if device_type == "cuda" else torch.float32

        with torch.autocast(device_type=device_type, dtype=dtype):
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                repetition_penalty=1.2,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

        new_tokens = outputs[0][input_length:]
        response = self.tokenizer.decode(new_tokens, skip_special_tokens=True)

        response = nettoyer_reponse(response)
        response = limiter_phrases(response, 3)

        self.conversation_history.append({
            "user": user_input,
            "assistant": response,
            "contexte": contexte
        })

        return {
            "message": response,
            "contexte": contexte
        }

# ============================================
# CHARGEMENT MODÈLE (4-BIT GPU / FP32 CPU)
# ============================================

@torch.no_grad()
def load_model():
    has_gpu = torch.cuda.is_available()
    print(f"🖥️ GPU disponible: {has_gpu}")

    if has_gpu:
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )
        device_map = "auto"
        torch_dtype = torch.bfloat16
    else:
        quantization_config = None
        device_map = "cpu"
        torch_dtype = torch.float32

    print(f"🔄 Chargement Mistral 7B ({'4-bit GPU' if has_gpu else 'FP32 CPU'})...")

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=quantization_config,
        device_map=device_map,
        torch_dtype=torch_dtype,
        token=HF_TOKEN,
        trust_remote_code=True,
        low_cpu_mem_usage=True
    )

    print("🔄 Chargement tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL,
        token=HF_TOKEN,
        trust_remote_code=True
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("🔄 Application LoRA Spinoza_Secours...")

    model = PeftModel.from_pretrained(
        base_model,
        ADAPTER_MODEL,
        token=HF_TOKEN
    )

    print("✅ Modèle Mistral 7B + LoRA chargé!")
    return model, tokenizer

# ============================================
# QUESTIONS BAC SPINOZA
# ============================================

QUESTIONS_BAC = [
    "La liberté est-elle une illusion ?",
    "Suis-je esclave de mes désirs ?",
    "Puis-je maîtriser mes émotions ?",
    "La joie procure-t-elle un pouvoir ?",
    "Peut-on désirer sans souffrir ?",
]

def choisir_question_amorce() -> str:
    return random.choice(QUESTIONS_BAC)

# ============================================
# API REST FASTAPI
# ============================================

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[List[str]]] = None

class ChatResponse(BaseModel):
    reply: str
    history: List[List[str]]
    contexte: str

api = FastAPI(title="Spinoza Secours API")
dialogue_api = None

@api.get("/")
def root():
    return {
        "message": "Spinoza Secours API - Mistral 7B + LoRA",
        "model": f"{BASE_MODEL} + {ADAPTER_MODEL}/{ADAPTER_SUBFOLDER}",
        "endpoints": ["/chat", "/health", "/init"]
    }

@api.get("/health")
def health():
    return {
        "status": "ok" if dialogue_api else "loading",
        "model_loaded": dialogue_api is not None
    }

@api.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    if not dialogue_api:
        return ChatResponse(
            reply="Modèle en cours de chargement...",
            history=[],
            contexte="neutre"
        )

    if request.history:
        dialogue_api.conversation_history = [
            {"user": h[0], "assistant": h[1], "contexte": "neutre"}
            for h in request.history if h[0] and h[1]
        ]

    result = dialogue_api.generate_response(request.message)

    history = [
        [entry["user"], entry["assistant"]]
        for entry in dialogue_api.conversation_history
    ]

    return ChatResponse(
        reply=result["message"],
        history=history,
        contexte=result["contexte"]
    )

@api.get("/init")
def init_endpoint():
    question = choisir_question_amorce()
    greeting = f"Bonjour ! Je suis Spinoza. Discutons ensemble de cette question :\n\n**{question}**\n\nQu'en penses-tu ?"
    return {
        "question": question,
        "greeting": greeting,
        "history": [[None, greeting]]
    }

# ============================================
# INTERFACE GRADIO
# ============================================

def create_interface(model, tokenizer):
    dialogue = DialogueSpinoza(model, tokenizer)

    global dialogue_api
    dialogue_api = dialogue

    def initialiser_conversation():
        question = choisir_question_amorce()
        return [[None, f"Bonjour ! Je suis Spinoza. Discutons ensemble de cette question :\n\n**{question}**\n\nQu'en penses-tu ?"]]

    def chat_function(message, history):
        if not message.strip():
            return "", history

        try:
            result = dialogue.generate_response(message)
            response = result["message"]
            contexte = result["contexte"]

            history = history or []
            history.append([message, f"{response}\n\n*[Contexte: {contexte}]*"])

            return "", history

        except Exception as e:
            error_msg = f"Erreur: {str(e)}"
            history = history or []
            history.append([message, error_msg])
            return "", history

    with gr.Blocks(title="Spinoza Secours") as interface:
        gr.Markdown("# 🎓 Spinoza Secours - Mistral 7B + LoRA")
        gr.Markdown("*Backup léger pour CPU/GPU - Fine-tuné sur schèmes logiques*")

        chatbot = gr.Chatbot(
            value=initialiser_conversation(),
            height=500
        )
        msg = gr.Textbox(placeholder="Réponds à Spinoza...")
        nouveau = gr.Button("🎲 Nouvelle question")

        msg.submit(chat_function, [msg, chatbot], [msg, chatbot])
        nouveau.click(initialiser_conversation, None, chatbot)

        gr.Markdown("---")
        gr.Markdown("**API REST:** GET `/health`, POST `/chat`, GET `/init`")

    return interface

# ============================================
# LANCEMENT
# ============================================

if __name__ == "__main__":
    print("🔄 Initialisation Spinoza Secours...")
    model, tokenizer = load_model()

    print("🔄 Création interface Gradio...")
    interface = create_interface(model, tokenizer)

    app = gr.mount_gradio_app(api, interface, path="/")

    print("✅ Lancement serveur...")
    print("📡 Interface: http://0.0.0.0:7860")
    print("📡 API REST: http://0.0.0.0:7860/chat")

    uvicorn.run(app, host="0.0.0.0", port=7860)
