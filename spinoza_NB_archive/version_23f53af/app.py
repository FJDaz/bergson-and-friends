import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import re
import random
from typing import Dict, List, Tuple
import os

# ============================================
# CONFIGURATION
# ============================================

BASE_MODEL = "Qwen/Qwen2.5-14B-Instruct"
ADAPTER_MODEL = "FJDaz/qwen-spinoza-niveau-b"
HF_TOKEN = os.getenv("HF_TOKEN")

# ============================================
# SYSTEM PROMPTS PAR PHILOSOPHE
# ============================================

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

# ============================================
# QUESTIONS BAC PAR PHILOSOPHE
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
# DÉTECTION CONTEXTUELLE
# ============================================

def detecter_contexte(user_input: str) -> str:
    """Détecte le contexte émotionnel de la réponse"""
    text_lower = user_input.lower()

    # Accord explicite
    if any(re.search(p, text_lower) for p in [r'\boui\b', r'\bd\'accord\b', r'\bexact\b', r'\bc\'est ça\b']):
        return "accord"

    # Confusion
    if any(re.search(p, text_lower) for p in [r'comprends? pas', r'je sais pas', r'c\'est quoi']):
        return "confusion"

    # Résistance
    if any(re.search(p, text_lower) for p in [r'\bmais\b', r'\bnon\b', r'pas d\'accord', r'faux']):
        return "resistance"

    return "neutre"

# ============================================
# POST-PROCESSING
# ============================================

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

# ============================================
# CLASSE DIALOGUE UNIVERSELLE
# ============================================

class DialoguePhilosophe:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def generate_response(self, user_input: str, history: List[Tuple], philosophe: str) -> Dict:
        """Génère une réponse adaptée au philosophe"""
        history = history or []
        contexte = detecter_contexte(user_input)

        # Choisir prompt selon philosophe
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

        # Construction messages
        messages = [{"role": "system", "content": system_prompt}]

        for exchange in history[-4:]:
            if exchange[0]:
                messages.append({"role": "user", "content": exchange[0]})
            if exchange[1]:
                clean_response = exchange[1].split('\n\n*[')[0]
                messages.append({"role": "assistant", "content": clean_response})

        messages.append({"role": "user", "content": user_input})

        # Génération
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
# CHARGEMENT MODÈLE
# ============================================

@torch.no_grad()
def load_model():
    """Charge le modèle SNB (Qwen 14B + LoRA)"""
    # 4-bit au lieu de 8-bit : ~7GB au lieu de 14GB, tient facilement dans T4 16GB
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,  # 4-bit : moitié moins de VRAM nécessaire
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4"  # NormalFloat4 - meilleure qualité pour 4-bit
    )

    print("🔄 Chargement Qwen 14B (4-bit) sur GPU...")
    
    # T4 a 16GB VRAM - Qwen 14B 4-bit fait ~7GB, donc largement suffisant
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=quantization_config,
        device_map="auto",  # Auto devrait maintenant tout mettre sur GPU
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
# INTERFACE GRADIO 3 PHILOSOPHES
# ============================================

def create_interface():
    """Interface Gradio avec 3 onglets"""

    print("🔄 Initialisation modèle...")
    model, tokenizer = load_model()
    dialogue = DialoguePhilosophe(model, tokenizer)

    def init_conversation(philosophe):
        """Initialise avec une question du bac"""
        question = random.choice(QUESTIONS_BAC[philosophe])
        noms = {"spinoza": "Spinoza", "bergson": "Henri Bergson", "kant": "Emmanuel Kant"}
        return [[None, f"Bonjour ! Je suis {noms[philosophe]}. Discutons ensemble de cette question :\n\n**{question}**\n\nQu'en penses-tu ?"]]

    def chat_function(message, history, philosophe):
        """Fonction chat universelle"""
        if not message.strip():
            return "", history

        try:
            history = history or []
            result = dialogue.generate_response(message, history, philosophe)
            response = result["message"]
            contexte = result["contexte"]

            history.append([message, f"{response}\n\n*[Contexte: {contexte}]*"])
            return "", history

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            history = history or []
            history.append([message, f"Erreur: {str(e)}"])
            return "", history

    # Fonctions spécifiques pour l'API
    def chat_spinoza(message, history):
        return chat_function(message, history, "spinoza")

    def chat_bergson(message, history):
        return chat_function(message, history, "bergson")

    def chat_kant(message, history):
        return chat_function(message, history, "kant")

    # Interface avec Tabs
    with gr.Blocks(title="Bergson & Friends - SNB") as interface:
        gr.Markdown("# 🎭 Bergson & Friends - Spinoza Niveau B")
        gr.Markdown("*Un seul modèle (Qwen 14B + LoRA Niveau B) pour 3 philosophes*")

        with gr.Tabs():
            # SPINOZA
            with gr.Tab("🔷 Spinoza"):
                chatbot_spinoza = gr.Chatbot(
                    value=init_conversation("spinoza"),
                    height=500
                )
                msg_spinoza = gr.Textbox(placeholder="Réponds à Spinoza...", container=False)
                with gr.Row():
                    nouveau_spinoza = gr.Button("🎲 Nouvelle question")
                    clear_spinoza = gr.Button("🗑️ Effacer")

                msg_spinoza.submit(
                    chat_spinoza,
                    [msg_spinoza, chatbot_spinoza],
                    [msg_spinoza, chatbot_spinoza],
                    api_name="chat_spinoza"
                )
                nouveau_spinoza.click(lambda: init_conversation("spinoza"), None, chatbot_spinoza)
                clear_spinoza.click(lambda: ([], None), None, [chatbot_spinoza, msg_spinoza])

            # BERGSON
            with gr.Tab("🔵 Bergson"):
                chatbot_bergson = gr.Chatbot(
                    value=init_conversation("bergson"),
                    height=500
                )
                msg_bergson = gr.Textbox(placeholder="Réponds à Bergson...", container=False)
                with gr.Row():
                    nouveau_bergson = gr.Button("🎲 Nouvelle question")
                    clear_bergson = gr.Button("🗑️ Effacer")

                msg_bergson.submit(
                    chat_bergson,
                    [msg_bergson, chatbot_bergson],
                    [msg_bergson, chatbot_bergson],
                    api_name="chat_bergson"
                )
                nouveau_bergson.click(lambda: init_conversation("bergson"), None, chatbot_bergson)
                clear_bergson.click(lambda: ([], None), None, [chatbot_bergson, msg_bergson])

            # KANT
            with gr.Tab("🟣 Kant"):
                chatbot_kant = gr.Chatbot(
                    value=init_conversation("kant"),
                    height=500
                )
                msg_kant = gr.Textbox(placeholder="Réponds à Kant...", container=False)
                with gr.Row():
                    nouveau_kant = gr.Button("🎲 Nouvelle question")
                    clear_kant = gr.Button("🗑️ Effacer")

                msg_kant.submit(
                    chat_kant,
                    [msg_kant, chatbot_kant],
                    [msg_kant, chatbot_kant],
                    api_name="chat_kant"
                )
                nouveau_kant.click(lambda: init_conversation("kant"), None, chatbot_kant)
                clear_kant.click(lambda: ([], None), None, [chatbot_kant, msg_kant])

        gr.Markdown("---")
        gr.Markdown("**Modèle :** Qwen 14B + LoRA Spinoza Niveau B | **Contextes :** accord, confusion, résistance, neutre")

    return interface

# ============================================
# LANCEMENT
# ============================================

if __name__ == "__main__":
    print("🚀 Lancement SNB avec 3 API endpoints: chat_spinoza, chat_bergson, chat_kant")
    interface = create_interface()
    interface.queue()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_api=True
    )
