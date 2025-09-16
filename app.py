#!/usr/bin/env python3
"""
APP.PY - INTERFACE GRADIO MULTI-PHILOSOPHES
Adaptation pour HuggingFace Spaces avec interface à onglets
Architecture: Reset à chaque switch + logging invisible + système d'alerte
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
        
        # Écriture log
        log_entry = f"""[{timestamp}] {philosophe.upper()} | Q:{len(question.split())}mots({question_hash}) | R:{len(reponse.split())}mots | {temps_reponse:.1f}s | {mode_rag.upper()}{symptoms_str}
Q: {question[:100]}{'...' if len(question) > 100 else ''}
R: {reponse[:150]}{'...' if len(reponse) > 150 else ''}
---
"""
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Erreur logging: {e}")
    
    def generer_stats_resume(self):
        """Génère un résumé des statistiques"""
        total_interactions = sum(self.stats['usage_philosophe'].values())
        if total_interactions == 0:
            return "Aucune interaction enregistrée"
        
        temps_moyen = sum(self.stats['temps_reponse']) / len(self.stats['temps_reponse']) if self.stats['temps_reponse'] else 0
        
        resume = f"""
RÉSUMÉ DEMO - {datetime.now().strftime("%Y-%m-%d %H:%M")}
=====================================
Total interactions: {total_interactions}
Temps de réponse moyen: {temps_moyen:.1f}s
Usage par philosophe:
  - Bergson: {self.stats['usage_philosophe']['bergson']} ({self.stats['usage_philosophe']['bergson']/total_interactions*100:.1f}%)
  - Kant: {self.stats['usage_philosophe']['kant']} ({self.stats['usage_philosophe']['kant']/total_interactions*100:.1f}%)
  - Spinoza: {self.stats['usage_philosophe']['spinoza']} ({self.stats['usage_philosophe']['spinoza']/total_interactions*100:.1f}%)
Mode RAG: {self.stats['mode_rag']['rag']}/{self.stats['mode_rag']['fallback']} (RAG/Fallback)
Crashes détectés: {self.stats['crashes_detectes']}
=====================================
"""
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(resume)
        except Exception:
            pass
        
        return resume

# =============================================================================
# 2. DÉTECTION CRASH AMÉLIORÉE
# =============================================================================

class CrashDetector:
    """Détection de symptômes de crash avec seuils révisés"""
    
    def __init__(self):
        self.reset_session()
    
    def reset_session(self):
        """Reset pour nouvelle session philosophe"""
        self.echange_count = 0
        self.violations_incarnation = 0
        self.symptomes_detectes = []
        self.historique_reponses = []
    
    def analyser_reponse(self, reponse, philosophe):
        """Analyse une réponse et détecte les symptômes de crash"""
        self.echange_count += 1
        self.historique_reponses.append(reponse)
        
        symptomes = []
        
        # 1. Violations incarnation (critiques avec pondération)
        violations = 0
        
        # Manque de "je" = léger (0.5)
        if not any(marker in reponse.lower() for marker in ['je ', 'mon ', 'ma ', 'mes ', "j'ai", "j'affirme"]):
            violations += 0.5
            symptomes.append("depersonnalisation")
        
        # "Selon X" = rédhibitoire (3.0)
        if any(marker in reponse.lower() for marker in ['selon bergson', 'kant dit', 'spinoza affirme']):
            violations += 3.0
            symptomes.append("3e_personne")
        
        # "Je suis X" = assez grave (2.0)
        if f"je suis {philosophe}" in reponse.lower() or "en tant que" in reponse.lower():
            violations += 2.0
            symptomes.append("meta_exposition")
        
        self.violations_incarnation += violations
        
        # 2. Chute dans l'anglais
        mots_anglais = ['the', 'and', 'that', 'this', 'with', 'from', 'they', 'have', 'been', 'their']
        ratio_anglais = sum(1 for mot in mots_anglais if mot in reponse.lower()) / len(reponse.split()) * 100
        if ratio_anglais > 15:  # Plus de 15% de mots anglais suspects
            symptomes.append("chute_anglais")
        
        # 3. Répétitions avec historique
        if len(self.historique_reponses) > 1:
            for precedente in self.historique_reponses[-3:]:  # 3 dernières
                if self._similitude_texte(reponse, precedente) > 0.6:
                    symptomes.append("repetition")
                    break
        
        # 4. Réponse anormalement courte
        if len(reponse.split()) < 10:
            symptomes.append("reponse_courte")
        
        # 5. Incohérence (réponse qui ne correspond pas du tout)
        if len(reponse.split()) > 200 or "..." in reponse:
            symptomes.append("incoherence")
        
        self.symptomes_detectes.extend(symptomes)
        
        return symptomes
    
    def _similitude_texte(self, texte1, texte2):
        """Calcule similitude entre deux textes"""
        mots1 = set(texte1.lower().split())
        mots2 = set(texte2.lower().split())
        intersection = len(mots1.intersection(mots2))
        union = len(mots1.union(mots2))
        return intersection / union if union > 0 else 0
    
    def detecter_crash(self):
        """Détecte si un crash est probable"""
        # Seuils révisés basés sur les tests réels
        seuil_echanges = 10  # Premier avertissement à 10 échanges
        seuil_violations = 6  # Plus tolérant que les 3-5 originaux
        
        # Comptage symptômes récents (3 derniers échanges)
        symptomes_recents = len([s for s in self.symptomes_detectes[-6:]])  # 6 = 2 symptômes/échange max
        
        crash_probable = (
            (self.echange_count >= seuil_echanges and symptomes_recents >= 4) or
            (self.violations_incarnation >= seuil_violations) or
            (self.echange_count >= 15)  # Seuil absolu basé sur les tests
        )
        
        return crash_probable, {
            'echanges': self.echange_count,
            'violations': self.violations_incarnation,
            'symptomes_recents': symptomes_recents,
            'derniers_symptomes': self.symptomes_detectes[-3:] if self.symptomes_detectes else []
        }

# =============================================================================
# 3. MANAGER PHILOSOPHES SIMPLIFIÉ
# =============================================================================

class PhilosophesManager:
    """Manager simplifié pour démo Gradio"""
    
    def __init__(self):
        print("🚀 Initialisation manager philosophes...")
        
        # Chargement modèle
        self.model, self.tokenizer, self.device = self._charger_mistral()
        if not self.model:
            raise Exception("Échec chargement Mistral")
        
        # Encoder pour RAG
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Corpus et RAG
        self._initialiser_corpus()
        self._initialiser_rag()
        
        # État session
        self.philosophe_actif = None
        self.crash_detector = CrashDetector()
        
        print("✅ Manager philosophes prêt")
    
    def _charger_mistral(self):
        """Chargement Mistral 7B optimisé pour HF Spaces"""
        try:
            model_id = "mistralai/Mistral-7B-Instruct-v0.2"
            
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4"
            )
            
            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                quantization_config=quantization_config,
                device_map="auto",
                torch_dtype=torch.float16
            )
            
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            tokenizer.pad_token = tokenizer.eos_token
            
            device = next(model.parameters()).device
            
            print(f"✅ Mistral chargé sur {device}")
            return model, tokenizer, device
            
        except Exception as e:
            print(f"❌ Erreur chargement Mistral: {e}")
            return None, None, None
    
    def _initialiser_corpus(self):
        """Chargement corpus philosophiques depuis fichiers"""
        print("📚 Chargement corpus philosophiques...")
        
        # Fichiers corpus correspondants
        fichiers_corpus = {
            'bergson': 'essai_conscience.txt',
            'kant': ['01_esthetique_transcendantale.txt', '02_analytique_des_concepts.txt', '03_antinomies_selection.txt'],
            'spinoza': 'Éthique_(Saisset,_1861)_Partie_I_clean.txt'
        }
        
        self.corpus_philosophes = {}
        
        for philo, fichiers in fichiers_corpus.items():
            if isinstance(fichiers, list):
                # Kant : multiple fichiers
                chunks = []
                for fichier in fichiers:
                    chunks.extend(self._charger_et_chunker(fichier))
                self.corpus_philosophes[philo] = chunks
            else:
                # Bergson, Spinoza : fichier unique
                self.corpus_philosophes[philo] = self._charger_et_chunker(fichiers)
        
        # Vérification chargement
        for philo, chunks in self.corpus_philosophes.items():
            print(f"✅ {philo}: {len(chunks)} chunks chargés")
    
    def _charger_et_chunker(self, filename):
        """Charge un fichier et le découpe en chunks"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                texte = f.read()
            
            # Nettoyage basique
            texte = texte.replace('\n', ' ').replace('\r', ' ')
            texte = ' '.join(texte.split())  # Normalise espaces
            
            # Chunking par paragraphes/phrases longues
            chunks = []
            phrases = texte.split('. ')
            
            chunk_actuel = ""
            for phrase in phrases:
                if len(chunk_actuel) + len(phrase) < 400:  # Chunks ~400 chars
                    chunk_actuel += phrase + ". "
                else:
                    if chunk_actuel:
                        chunks.append(chunk_actuel.strip())
                    chunk_actuel = phrase + ". "
            
            # Dernier chunk
            if chunk_actuel:
                chunks.append(chunk_actuel.strip())
            
            return chunks[:50] if chunks else []  # Limite à 50 chunks par philosophe
            
        except FileNotFoundError:
            print(f"❌ Fichier {filename} non trouvé")
            return []
        except Exception as e:
            print(f"❌ Erreur lecture {filename}: {e}")
            return []
    
    def _initialiser_rag(self):
        """Initialisation RAG pour tous les philosophes"""
        print("⚙️ Initialisation RAG...")
        self.rag_indexes = {}
        
        for philosophe, corpus in self.corpus_philosophes.items():
            try:
                embeddings = self.encoder.encode(corpus, convert_to_numpy=True)
                
                dimension = embeddings.shape[1]
                index = faiss.IndexFlatIP(dimension)
                
                faiss.normalize_L2(embeddings)
                index.add(embeddings.astype('float32'))
                
                self.rag_indexes[philosophe] = {
                    'index': index,
                    'corpus': corpus,
                    'embeddings': embeddings
                }
                
                print(f"✅ RAG {philosophe}: {len(corpus)} chunks")
                
            except Exception as e:
                print(f"❌ Erreur RAG {philosophe}: {e}")
    
    def switch_philosophe(self, nouveau_philosophe):
        """Switch avec reset session"""
        if nouveau_philosophe != self.philosophe_actif:
            self.philosophe_actif = nouveau_philosophe
            self.crash_detector.reset_session()
            
            # Nettoyage mémoire
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            print(f"🎭 Switch vers {nouveau_philosophe}")
        
        return nouveau_philosophe in self.corpus_philosophes
    
    def generer_reponse(self, question, philosophe):
        """Génération de réponse avec détection crash"""
        if not self.switch_philosophe(philosophe):
            return "Philosophe non disponible", [], "error", False, {}
        
        start_time = time.time()
        
        # Recherche RAG
        chunks = self._rechercher_rag(question, philosophe)
        seuil_pertinence = 0.4
        
        # Décision RAG vs Vanilla
        if chunks and chunks[0]['score'] > seuil_pertinence:
            mode = "rag"
            contexte = "\n\n".join([chunk['texte'] for chunk in chunks[:2]])
            
            prompt = f"""Tu es {philosophe.capitalize()}. Réponds à la première personne en t'appuyant sur tes œuvres.

Contexte de tes écrits:
{contexte}

Question: {question}
Réponse (en tant que {philosophe.capitalize()}):"""
            
        else:
            mode = "fallback"
            concepts_cles = {
                'bergson': "Durée pure, intuition vs intelligence, élan vital, mémoire créatrice",
                'kant': "Phénomène vs noumène, entendement, impératif catégorique, raison pure",
                'spinoza': "Substance unique, conatus, affects, Deus sive Natura"
            }
            
            prompt = f"""Tu es {philosophe.capitalize()}. Réponds à la première personne selon ta philosophie.

Concepts clés: {concepts_cles.get(philosophe, '')}

Question: {question}
Réponse (en tant que {philosophe.capitalize()}):"""
        
        # Génération
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1500)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=150,
                    do_sample=True,
                    temperature=0.7,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response[len(prompt):].strip()
            
            response_time = time.time() - start_time
            
            # Analyse crash
            symptomes = self.crash_detector.analyser_reponse(response, philosophe)
            crash_probable, crash_info = self.crash_detector.detecter_crash()
            
            return response, chunks, mode, crash_probable, crash_info
            
        except Exception as e:
            response_time = time.time() - start_time
            error_msg = f"Erreur génération: {str(e)}"
            return error_msg, [], "error", False, {}
    
    def _rechercher_rag(self, question, philosophe):
        """Recherche RAG pour un philosophe"""
        if philosophe not in self.rag_indexes:
            return []
        
        try:
            rag_data = self.rag_indexes[philosophe]
            
            query_embedding = self.encoder.encode([question], convert_to_numpy=True)
            faiss.normalize_L2(query_embedding)
            
            scores, indices = rag_data['index'].search(query_embedding.astype('float32'), 2)
            
            chunks = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(rag_data['corpus']):
                    chunks.append({
                        'texte': rag_data['corpus'][idx],
                        'score': float(score)
                    })
            
            return chunks
            
        except Exception as e:
            print(f"❌ Erreur recherche RAG: {e}")
            return []

# =============================================================================
# 4. INTERFACE GRADIO PRINCIPALE
# =============================================================================

# Initialisation globale
print("🚀 Initialisation application...")
manager = PhilosophesManager()
logger = DemoLogger()

def chat_philosophe(question, philosophe_nom):
    """Fonction de chat pour Gradio"""
    if not question or not question.strip():
        return "Veuillez poser une question.", ""
    
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
    
    # Gestion alerte crash
    alert_msg = ""
    if crash_probable:
        alert_msg = f"\n\n⚠️ Le philosophe semble fatiguer (échange {crash_info['echanges']}). Voulez-vous continuer la conversation ?"
    
    return reponse, alert_msg

# Interface Gradio
with gr.Blocks(title="Bergson and Friends", theme=gr.themes.Soft()) as demo:
    
    # Header
    gr.Markdown("# Bergson and Friends")
    gr.Markdown("*Trois philosophes s'entretiennent avec vous*")
    
    # Onglets philosophes
    with gr.Tabs():
        
        # BERGSON
        with gr.TabItem("Henri Bergson"):
            gr.Markdown("### Henri Bergson")
            gr.Markdown("*Philosophe de la durée, de l'élan vital et de l'intuition*")
            
            with gr.Row():
                question_bergson = gr.Textbox(
                    label="Votre question à Bergson",
                    placeholder="Qu'est-ce que la durée pure ?",
                    lines=2
                )
            
            with gr.Row():
                submit_bergson = gr.Button("Poser la question", variant="primary")
                home_bergson = gr.Button("Retour accueil", variant="secondary")
            
            reponse_bergson = gr.Textbox(
                label="Bergson vous répond",
                lines=6,
                interactive=False
            )
            
            alerte_bergson = gr.Textbox(
                label="",
                visible=False,
                interactive=False
            )
        
        # KANT
        with gr.TabItem("Immanuel Kant"):
            gr.Markdown("### Immanuel Kant") 
            gr.Markdown("*Philosophe critique des limites de la raison*")
            
            with gr.Row():
                question_kant = gr.Textbox(
                    label="Votre question à Kant",
                    placeholder="Que pouvons-nous connaître ?",
                    lines=2
                )
            
            with gr.Row():
                submit_kant = gr.Button("Poser la question", variant="primary")
                home_kant = gr.Button("Retour accueil", variant="secondary")
            
            reponse_kant = gr.Textbox(
                label="Kant vous répond",
                lines=6,
                interactive=False
            )
            
            alerte_kant = gr.Textbox(
                label="",
                visible=False,
                interactive=False
            )
        
        # SPINOZA
        with gr.TabItem("Baruch Spinoza"):
            gr.Markdown("### Baruch Spinoza")
            gr.Markdown("*Philosophe de la substance unique et de la nécessité*")
            
            with gr.Row():
                question_spinoza = gr.Textbox(
                    label="Votre question à Spinoza",
                    placeholder="Qu'est-ce que le conatus ?",
                    lines=2
                )
            
            with gr.Row():
                submit_spinoza = gr.Button("Poser la question", variant="primary")
                home_spinoza = gr.Button("Retour accueil", variant="secondary")
            
            reponse_spinoza = gr.Textbox(
                label="Spinoza vous répond",
                lines=6,
                interactive=False
            )
            
            alerte_spinoza = gr.Textbox(
                label="",
                visible=False,
                interactive=False
            )
    
    # Fonctions de callback
    def process_bergson(question):
        reponse, alerte = chat_philosophe(question, "bergson")
        return reponse, alerte, ""  # Clear question
    
    def process_kant(question):
        reponse, alerte = chat_philosophe(question, "kant")
        return reponse, alerte, ""
    
    def process_spinoza(question):
        reponse, alerte = chat_philosophe(question, "spinoza")
        return reponse, alerte, ""
    
    def reset_home():
        return "", ""  # Clear question et réponse
    
    # Event handlers
    submit_bergson.click(
        process_bergson,
        inputs=question_bergson,
        outputs=[reponse_bergson, alerte_bergson, question_bergson]
    )
    
    question_bergson.submit(
        process_bergson,
        inputs=question_bergson,
        outputs=[reponse_bergson, alerte_bergson, question_bergson]
    )
    
    home_bergson.click(
        reset_home,
        outputs=[question_bergson, reponse_bergson]
    )
    
    submit_kant.click(
        process_kant,
        inputs=question_kant,
        outputs=[reponse_kant, alerte_kant, question_kant]
    )
    
    question_kant.submit(
        process_kant,
        inputs=question_kant,
        outputs=[reponse_kant, alerte_kant, question_kant]
    )
    
    home_kant.click(
        reset_home,
        outputs=[question_kant, reponse_kant]
    )
    
    submit_spinoza.click(
        process_spinoza,
        inputs=question_spinoza,
        outputs=[reponse_spinoza, alerte_spinoza, question_spinoza]
    )
    
    question_spinoza.submit(
        process_spinoza,
        inputs=question_spinoza,
        outputs=[reponse_spinoza, alerte_spinoza, question_spinoza]
    )
    
    home_spinoza.click(
        reset_home,
        outputs=[question_spinoza, reponse_spinoza]
    )

# Lancement
if __name__ == "__main__":
    print("🎭 Lancement Bergson and Friends...")
    demo.launch()