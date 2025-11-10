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

    if contexte == "confusion":
        base += "\n\nL'élève est confus. Utilise une ANALOGIE concrète pour clarifier."
    elif contexte == "resistance":
        base += "\n\nL'élève résiste. Révèle la CONTRADICTION de sa position."
    elif contexte == "accord":
        base += "\n\nL'élève accepte. AVANCE vers la prochaine étape logique."
    else:
        base += "\n\nPose une question pour faire réfléchir l'élève."

    return base

# ============================================
# POST-PROCESSING V2
# ============================================

def nettoyer_reponse(text: str) -> str:
    """Code exact succès V2"""
    # Annotations méta (problème identifié dans tests)
    text = re.sub(r'\([^)]*[Aa]ttends[^)]*\)', '', text)
    text = re.sub(r'\([^)]*[Pp]oursuis[^)]*\)', '', text)
    text = re.sub(r'\([^)]*[Dd]onne[^)]*\)', '', text)
    
    # Emojis inappropriés
    text = re.sub(r'[😀-🙏🌀-🗿🚀-🛿]', '', text)
    
    # Nettoyer espaces
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\s+([.!?])', r'\1', text)
    
    return text

def limiter_phrases(text: str, max_phrases: int = 3) -> str:
    """Limite verbosité (problème identifié)"""
    phrases = re.split(r'[.!?]+\s+', text)
    phrases = [p.strip() for p in phrases if p.strip()]
    
    if len(phrases) <= max_phrases:
        return text
    
    return '. '.join(phrases[:max_phrases]) + '.'

# ============================================
# CLASSE DIALOGUE V2 (CODE SUCCÈS)
# ============================================

class DialogueSpinozaV2:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.conversation_history = []
        
    def generate_response(self, user_input: str) -> Dict:
        """Génère réponse avec adaptation contextuelle V2"""
        
        # Détection contexte
        contexte = detecter_contexte(user_input)
        
        # Construction prompt adaptatif
        system_prompt = construire_prompt_contextuel_v2(contexte)
        
        # Historique conversation (limité pour éviter surcharge)
        messages = [{"role": "system", "content": system_prompt}]
        
        # Ajouter derniers échanges
        for entry in self.conversation_history[-4:]:  # 4 derniers échanges max
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
        
        # Génération avec paramètres V2 optimisés
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=150,  # Concis pour éviter verbosité
                temperature=0.7,     # Variété sans chaos
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
        
        # Sauvegarde historique
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
# QUESTIONS BAC (AMORCES SPINOZA)
# ============================================

QUESTIONS_BAC_SPINOZA = [
    "La liberté est-elle une illusion ?",
    "Suis-je esclave de mes désirs ?", 
    "Puis-je maîtriser mes émotions ?",
    "La joie procure-t-elle un pouvoir ?",
    "Peut-on désirer sans souffrir ?",
    "Sommes-nous responsables de nos actes ?",
    "La raison suffit-elle à nous guider ?",
    "Peut-on vivre sans passions ?",
    "Qu'est-ce que la vérité ?",
    "Que puis-je savoir du monde ?",
    "Dieu et Nature sont-ils identiques ?",
    "Pourquoi souffrons-nous ?",
    "La connaissance rend-elle libre ?",
    "Peut-on être heureux sans être libre ?",
    "L'homme est-il naturellement social ?"
]

def choisir_question_amorce() -> str:
    """Choisit une question aléatoire du bac"""
    return random.choice(QUESTIONS_BAC_SPINOZA)

# ============================================
# CHARGEMENT MODÈLE (8-BIT CRITIQUE)
# ============================================

@torch.no_grad()
def load_model():
    """Chargement avec quantization 8-bit (FIX EOS CRITIQUE)"""
    
    # Configuration 8-bit (CORRECTION CRITIQUE IDENTIFIÉE)
    quantization_config = BitsAndBytesConfig(
        load_in_8bit=True,  # CRITIQUE: 8-bit au lieu de 4-bit
        llm_int8_threshold=6.0,
        llm_int8_has_fp16_weight=False,
    )
    
    print("🔄 Chargement Qwen 14B base (8-bit)...")
    
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
        ADAPTER_MODEL,
        token=HF_TOKEN,
        trust_remote_code=True
    )
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    print("🔄 Application adaptateurs LoRA Spinoza Niveau B...")
    
    model = PeftModel.from_pretrained(
        base_model,
        ADAPTER_MODEL,
        token=HF_TOKEN
    )
    
    print("✅ Spinoza Niveau B V1 chargé avec succès!")
    
    return model, tokenizer

# ============================================
# INTERFACE GRADIO SIMPLE
# ============================================

def create_interface():
    """Interface Gradio pour HF Space"""
    
    print("🔄 Initialisation Spinoza Niveau B V1...")
    model, tokenizer = load_model()
    dialogue = DialogueSpinozaV2(model, tokenizer)
    
    def initialiser_conversation():
        """Spinoza démarre avec question bac"""
        question = choisir_question_amorce()
        return [[None, f"🎭 **Spinoza** : Bonjour ! Explorons ensemble cette question :\n\n**{question}**\n\nQu'en penses-tu ?"]]
    
    def chat_function(message, history):
        """Fonction chat principale"""
        if not message.strip():
            return "", history
            
        try:
            result = dialogue.generate_response(message)
            response = result["message"]
            contexte = result["contexte"]
            
            # Format avec contexte pour debug
            response_formatted = f"🎭 **Spinoza** : {response}\n\n*[Contexte détecté: {contexte}]*"
            
            history = history or []
            history.append([message, response_formatted])
            
            return "", history
            
        except Exception as e:
            error_msg = f"❌ Erreur: {str(e)}"
            history = history or []
            history.append([message, error_msg])
            return "", history
    
    # Interface Gradio
    with gr.Blocks(title="Spinoza Niveau B V1") as interface:
        gr.Markdown("# 🎭 Spinoza - Dialogue Philosophique Niveau B")
        gr.Markdown("*Modèle fine-tuné avec détection contextuelle - Code Colab V1 fonctionnel*")
        
        chatbot = gr.Chatbot(
            value=initialiser_conversation(),
            elem_id="chatbot",
            bubble_full_width=False,
            height=600,
            show_label=False
        )
        
        with gr.Row():
            msg = gr.Textbox(
                placeholder="Réponds à Spinoza ou pose une question...",
                container=False,
                scale=8
            )
            nouveau_btn = gr.Button("🎲 Nouvelle question", scale=2)
            clear_btn = gr.Button("🗑️ Effacer", scale=1)
        
        msg.submit(chat_function, [msg, chatbot], [msg, chatbot])
        nouveau_btn.click(lambda: initialiser_conversation(), None, chatbot)
        clear_btn.click(lambda: ([], ""), None, [chatbot, msg])
        
        gr.Markdown("---")
        gr.Markdown("**🎯 Contextes détectés :** accord, confusion, résistance, neutre")
        gr.Markdown("**📚 Questions bac :** 15 sujets philosophiques authentiques Spinoza")
        gr.Markdown("**⚙️ Modèle :** Qwen 14B + LoRA Spinoza Niveau B (quantization 8-bit)")
    
    return interface

# ============================================
# LANCEMENT
# ============================================

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )