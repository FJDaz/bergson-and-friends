#!/usr/bin/env python3
"""
APP.PY - INTERFACE GRADIO MULTI-PHILOSOPHES
Adaptation pour HuggingFace Spaces avec interface à onglets
Architecture: Reset à chaque switch + logging invisible + système d'alerte + API REST
"""

import gradio as gr
import torch
import time
import gc
import hashlib
from datetime import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# =============================================================================
# 0. CHARGEMENT CSS PERSONNALISÉ
# =============================================================================

def load_custom_css():
    """Charge le CSS personnalisé depuis le fichier static/style.css"""
    try:
        with open("static/style.css", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"⚠️ Erreur chargement CSS: {e}")
        return ""

# =============================================================================
# 1. SYSTÈME DE LOGGING INVISIBLE
# =============================================================================

class DemoLogger:
    """Logger invisible pour métriques de démonstration"""
    
    def __init__(self):
        self.log_file = "philosophes_demo_stats.txt"
        self.session_start = datetime.now()
        self.stats = {
            'usage_philosophe': {'bergson': 0, 'kant': 0, 'spinoza': 0},
            'temps_reponse': [],
            'mode_rag': {'rag': 0, 'fallback': 0},
            'crashes_detectes': 0,
            'echanges_par_session': []
        }
    
    def log_interaction(self, philosophe, question, reponse, temps_reponse, mode_rag, crash_symptoms=None):
        """Log d'une interaction complète"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Hash de la question pour patterns
        question_hash = hashlib.md5(question.lower().encode()).hexdigest()[:8]
        
        # Détection symptômes crash
        symptoms_str = ""
        if crash_symptoms:
            symptoms_str = f" | CRASH:{','.join(crash_symptoms)}"
        
        # Mise à jour stats
        self.stats['usage_philosophe'][philosophe] += 1
        self.stats['temps_reponse'].append(temps_reponse)
        self.stats['mode_rag'][mode_rag] += 1
        
        if crash_symptoms:
            self.stats['crashes_detectes'] += 1
        
        # Log discret
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{timestamp} | {philosophe} | {question_hash} | {temps_reponse:.1f}s | {mode_rag}{symptoms_str}\n")
        except:
            pass  # Ignore silencieusement

# =============================================================================
# 2. SYSTÈME FALLBACK ENRICHI
# =============================================================================

class PhilosopheFallback:
    """Système de fallback intelligent par philosophe"""
    
    def __init__(self):
        self.responses_bergson = {
            'durée': "La durée, c'est le temps vécu de l'intérieur. Quand vous écoutez une mélodie, vous ne comptez pas les notes - vous les vivez dans leur continuité...",
            'temps': "Le temps de l'horloge découpe, mais la durée vraie unit. Votre conscience tisse le passé et le présent dans un élan créateur...",
            'conscience': "Ma conscience n'est pas un miroir, mais un prisme qui décompose et recompose le réel selon ses besoins vitaux...",
            'mémoire': "Votre mémoire n'est pas un grenier poussiéreux, mais une force agissante qui colore chaque instant présent...",
            'intuition': "L'intuition nous fait pénétrer dans l'élan vital même. Là où l'intelligence découpe, l'intuition saisit la mobilité créatrice...",
            'default': "Je réfléchis à votre question avec cette intuition qui me permet de saisir la durée créatrice de la conscience..."
        }
        
        self.responses_kant = {
            'devoir': "Le devoir moral ne se négocie pas avec les circonstances. 'Agis seulement selon cette maxime dont tu peux vouloir qu'elle devienne une loi universelle.'",
            'raison': "Ma raison pure pose les limites de la connaissance : nous connaissons les phénomènes, jamais les choses en soi...",
            'liberté': "La liberté n'est pas faire ce qu'on veut, mais vouloir ce que la raison pratique nous commande comme universel...",
            'morale': "L'impératif catégorique vous élève au-dessus de vos inclinations particulières vers l'humanité en vous...",
            'connaissance': "Nos intuitions sans concepts sont aveugles, nos concepts sans intuitions sont vides...",
            'default': "J'examine votre question selon les exigences de la raison critique qui pose les limites de toute connaissance possible..."
        }
        
        self.responses_spinoza = {
            'substance': "Il n'existe qu'une seule substance, que j'appelle Dieu ou la Nature - Deus sive Natura. Tout le reste n'est que modes de cette substance infinie...",
            'liberté': "Vous êtes libre quand vous agissez selon votre nature propre, et non sous la contrainte des causes extérieures...",
            'affects': "Vos affects sont des augmentations ou diminutions de votre puissance d'agir. La joie vous élève, la tristesse vous diminue...",
            'conatus': "Chaque être s'efforce de persévérer dans son être. C'est votre conatus - votre force vitale d'affirmation...",
            'nécessité': "Tout arrive selon des lois nécessaires. Comprendre cette nécessité, c'est accéder à la béatitude...",
            'default': "Je considère votre question selon l'ordre géométrique de la Nature, où tout s'enchaîne par nécessité..."
        }
    
    def get_response(self, question, philosophe):
        """Génère une réponse fallback intelligente"""
        question_lower = question.lower()
        
        if philosophe == 'bergson':
            responses = self.responses_bergson
        elif philosophe == 'kant':
            responses = self.responses_kant
        elif philosophe == 'spinoza':
            responses = self.responses_spinoza
        else:
            return "Je médite sur votre question..."
        
        # Recherche de mots-clés
        for key, response in responses.items():
            if key != 'default' and key in question_lower:
                return f"🎭 **{philosophe.capitalize()}** : {response}"
        
        # Réponse par défaut
        return f"🎭 **{philosophe.capitalize()}** : {responses['default']}"

# =============================================================================
# 3. GESTIONNAIRE PRINCIPAL
# =============================================================================

class PhilosophesManager:
    """Gestionnaire principal avec IA et fallback"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.embedder = None
        self.index = None
        self.chunks = []
        self.fallback = PhilosopheFallback()
        self.crash_detector = {"consecutive_failures": 0, "last_failure_time": 0}
        
        # Chargement automatique
        try:
            self.load_model()
            self.load_rag_system()
            print("✅ Système IA chargé avec succès")
        except Exception as e:
            print(f"⚠️ Chargement IA échoué: {e}")
            print("→ Mode fallback uniquement")
    
    def load_model(self):
        """Chargement modèle avec gestion d'erreur"""
        try:
            # Configuration quantization 8-bit (FIX: passage de 4-bit à 8-bit)
            bnb_config = BitsAndBytesConfig(
                load_in_8bit=True,  # ← CHANGEMENT CRITIQUE
                llm_int8_threshold=6.0,
                llm_int8_has_fp16_weight=False
            )
            
            model_id = "mistralai/Mistral-7B-Instruct-v0.2"
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                quantization_config=bnb_config,
                device_map="auto",
                torch_dtype=torch.float16
            )
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
        except Exception as e:
            print(f"Erreur chargement modèle: {e}")
            raise
    
    def load_rag_system(self):
        """Chargement système RAG"""
        try:
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Simulation chunks - remplace par ton vrai corpus
            self.chunks = [
                "La durée bergsonienne est le temps vécu de l'intérieur...",
                "L'impératif catégorique kantien commande universellement...", 
                "La substance spinoziste est unique et infinie...",
                # ... ton corpus complet ici
            ]
            
            # Index FAISS
            if self.chunks:
                embeddings = self.embedder.encode(self.chunks)
                self.index = faiss.IndexFlatIP(embeddings.shape[1])
                self.index.add(embeddings.astype('float32'))
                
        except Exception as e:
            print(f"Erreur RAG: {e}")
            raise
    
    def generer_reponse(self, question, philosophe):
        """Génération avec fallback automatique"""
        start_time = time.time()
        
        try:
            # Tentative IA
            if self.model and self.tokenizer:
                
                # RAG
                context = self.get_rag_context(question)
                
                # Prompt système
                system_prompts = {
                    'bergson': "Tu es Henri Bergson. Tu parles à la première personne de tes concepts : durée, élan vital, intuition.",
                    'kant': "Tu es Emmanuel Kant. Tu parles à la première personne de tes concepts : impératif catégorique, raison pure, morale.",
                    'spinoza': "Tu es Baruch Spinoza. Tu parles à la première personne de tes concepts : substance, conatus, affects."
                }
                
                prompt = f"<s>[INST] {system_prompts.get(philosophe, '')}\n\nContext: {context}\n\nQuestion: {question} [/INST]"
                
                # Génération
                inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=1024, truncation=True)
                
                with torch.no_grad():
                    outputs = self.model.generate(
                        inputs,
                        max_new_tokens=300,
                        temperature=0.7,
                        top_p=0.9,
                        do_sample=True,
                        eos_token_id=self.tokenizer.eos_token_id,
                        pad_token_id=self.tokenizer.eos_token_id
                    )
                
                response = self.tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
                response = response.strip()
                
                if response and len(response) > 10:
                    # Reset crash detector
                    self.crash_detector["consecutive_failures"] = 0
                    temps_reponse = time.time() - start_time
                    return response, context[:100], "rag", False, {"temps": temps_reponse}
            
        except Exception as e:
            print(f"Erreur génération: {e}")
        
        # Fallback
        self.crash_detector["consecutive_failures"] += 1
        response = self.fallback.get_response(question, philosophe)
        temps_reponse = time.time() - start_time
        
        crash_probable = self.crash_detector["consecutive_failures"] >= 3
        crash_info = {
            "temps": temps_reponse,
            "echanges": self.crash_detector["consecutive_failures"],
            "derniers_symptomes": ["generation_failed"]
        }
        
        return response, "fallback", "fallback", crash_probable, crash_info
    
    def get_rag_context(self, question):
        """Recherche RAG simple"""
        try:
            if self.index and self.embedder and self.chunks:
                query_embedding = self.embedder.encode([question])
                D, I = self.index.search(query_embedding.astype('float32'), k=3)
                context = " ".join([self.chunks[i] for i in I[0] if i < len(self.chunks)])
                return context[:500]
        except:
            pass
        return ""

# =============================================================================
# 4. INTERFACE GRADIO AVEC API
# =============================================================================

# Chargement CSS personnalisé
custom_css = load_custom_css()

# Initialisation globale
print("🚀 Initialisation application...")
manager = PhilosophesManager()
logger = DemoLogger()

# Historiques par philosophe
historiques = {'bergson': [], 'kant': [], 'spinoza': []}

def chat_philosophe(question, philosophe_nom, historique_actuel=""):
    """Fonction de chat pour Gradio avec historique"""
    if not question or not question.strip():
        return historique_actuel, "Veuillez poser une question.", ""
    
    # Génération réponse
    reponse, chunks, mode, crash_probable, crash_info = manager.generer_reponse(
        question.strip(), philosophe_nom
    )
    
    # Logging
    symptomes = crash_info.get('derniers_symptomes', []) if crash_probable else []
    logger.log_interaction(
        philosophe_nom, question, reponse, 
        crash_info.get('temps', 0), mode, symptomes
    )
    
    # Ajout à l'historique
    nouvel_echange = f"**Vous :** {question}\n\n**{philosophe_nom.capitalize()} :** {reponse}\n\n---\n\n"
    historique_mis_a_jour = historique_actuel + nouvel_echange
    
    # Gestion alerte crash
    alert_msg = ""
    if crash_probable:
        alert_msg = f"⚠️ Le philosophe semble fatiguer (échange {crash_info['echanges']}). Voulez-vous continuer la conversation ?"
    
    return historique_mis_a_jour, reponse, alert_msg

# Fonctions spécifiques par philosophe pour l'API
def chat_bergson(question, historique=""):
    return chat_philosophe(question, "bergson", historique)

def chat_kant(question, historique=""):
    return chat_philosophe(question, "kant", historique)

def chat_spinoza(question, historique=""):
    return chat_philosophe(question, "spinoza", historique)

# =============================================================================
# 5. CONSTRUCTION INTERFACE
# =============================================================================

def create_philosopher_tab(philosophe, chat_fn, description, examples):
    """Créé un onglet pour un philosophe"""
    with gr.Column():
        gr.Markdown(f"## {description}")
        
        with gr.Row():
            with gr.Column(scale=3):
                question = gr.Textbox(
                    label="Votre question",
                    placeholder=f"Posez votre question à {philosophe}...",
                    lines=2
                )
                submit = gr.Button("Poser la question", variant="primary")
                
            with gr.Column(scale=1):
                clear = gr.Button("Effacer", variant="secondary")
        
        # Exemples
        gr.Markdown("### Exemples de questions :")
        example_buttons = []
        for example in examples:
            btn = gr.Button(example, variant="secondary", size="sm")
            example_buttons.append((btn, example))
        
        # Historique et réponses
        historique = gr.Textbox(
            label=f"Conversation avec {philosophe}",
            value="",
            lines=10,
            max_lines=20,
            interactive=False
        )
        
        derniere_reponse = gr.Textbox(
            label="Dernière réponse",
            value="",
            lines=5,
            interactive=False
        )
        
        alerte = gr.Textbox(
            label="Alertes système",
            value="",
            lines=2,
            visible=False
        )
        
        # Événements
        submit.click(
            chat_fn,
            inputs=[question, historique],
            outputs=[historique, derniere_reponse, alerte]
        )
        
        clear.click(
            lambda: ("", "", ""),
            outputs=[historique, derniere_reponse, alerte]
        )
        
        # Exemples clickables
        for btn, example_text in example_buttons:
            btn.click(
                lambda x=example_text: x,
                outputs=[question]
            )

# Interface principale
with gr.Blocks(css=custom_css, title="🧠 Bergson & Friends") as demo:
    
    gr.HTML("""
    <div style="text-align: center; padding: 20px;">
        <h1>🧠 Bergson & Friends</h1>
        <p><em>Dialoguez avec les grands philosophes</em></p>
    </div>
    """)
    
    with gr.Tabs():
        with gr.TabItem("🌊 Henri Bergson"):
            create_philosopher_tab(
                "Bergson",
                chat_bergson,
                "**Henri Bergson (1859-1941)** - Philosophe de la durée et de l'élan vital",
                [
                    "Qu'est-ce que la durée pure ?",
                    "Quelle différence entre temps et durée ?",
                    "Comment fonctionne la mémoire ?",
                    "Qu'est-ce que l'élan vital ?"
                ]
            )
        
        with gr.TabItem("⚖️ Emmanuel Kant"):
            create_philosopher_tab(
                "Kant",
                chat_kant,
                "**Emmanuel Kant (1724-1804)** - Philosophe de l'impératif catégorique",
                [
                    "Qu'est-ce que l'impératif catégorique ?",
                    "Comment agir moralement ?",
                    "Quelle est la limite de la connaissance ?",
                    "Qu'est-ce que l'autonomie ?"
                ]
            )
        
        with gr.TabItem("🌀 Baruch Spinoza"):
            create_philosopher_tab(
                "Spinoza",
                chat_spinoza,
                "**Baruch Spinoza (1632-1677)** - Philosophe de la substance et des affects",
                [
                    "Qu'est-ce que la substance ?",
                    "Comment être libre ?",
                    "Que sont les affects ?",
                    "Qu'est-ce que le conatus ?"
                ]
            )
    
    gr.HTML("""
    <div style="text-align: center; padding: 10px; font-size: 12px; color: #666;">
        <p>Projet pédagogique - François-Jean Dazin</p>
    </div>
    """)

# =============================================================================
# 6. LANCEMENT AVEC API ACTIVÉE
# =============================================================================

# CRUCIAL: Configuration qui active l'API REST
demo.queue(
    api_open=True,          # ← Active l'API REST
    max_size=50,            # Limite queue  
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_api=True,         # ← Documentation API visible sur /docs
        inbrowser=False
    )