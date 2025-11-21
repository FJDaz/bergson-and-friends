# 📁 Arborescence du Repository bergsonAndFriends

**Date :** 21 novembre 2025  
**Repository local :** `/Users/francois-jeandazin/bergsonAndFriends/`  
**Repository distant :** `https://github.com/FJDaz/bergsonAndFriends` (si configuré)

---

## 🌳 Structure Locale

```
bergsonAndFriends/
│
├── 📂 3_PHI_HF/                    # Space HF Principal (Qwen 14B, 3 philosophes)
│   ├── app.py                      # Application FastAPI + Gradio
│   ├── requirements.txt            # Dépendances Python
│   ├── README.md                   # Documentation Space
│   └── Prompts/
│       ├── INTEGRATION_RAG_INTELLIGENTE.md
│       ├── Schemes Bergson.json
│       ├── Schemes Kant.json
│       └── VARIATIONS_FORMULATIONS.md
│
├── 📂 Spinoza_Secours_HF/          # Space HF Secours (Mistral 7B, Spinoza seul)
│   ├── index_spinoza.html          # Frontend HTML
│   ├── prompt_systeme_hybride.py   # Prompt optimisé (~250 tokens)
│   ├── RAPPORT_PROMPT_SYS_RAG.md   # Analyse prompts + RAG
│   └── ARBORESCENCE_REPO.md        # Ce fichier
│
├── 📂 bergsonAndFriends_HF/         # Ancien Space HF (archive ?)
│   ├── app.py                      # Application principale
│   ├── app_with_api.py             # Version avec API
│   ├── index.html                  # Interface frontend (à trois philos ?)
│   ├── requirements.txt
│   ├── static/                     # Assets (fonts, images, CSS)
│   ├── netlify/functions/          # Functions Netlify
│   └── *.txt                       # Corpus textes (Kant, Spinoza, Bergson)
│
├── 📂 data/
│   ├── FT/                         # Fine-tuning datasets
│   │   ├── Dataset Niveau A Schemes.txt
│   │   └── processed/
│   │       ├── schemes_levelA_base.jsonl
│   │       └── schemes_levelA_augmented.jsonl
│   │
│   ├── RAG/                        # Corpus RAG
│   │   ├── Corpus Spinoza Dialogique 18k - Éthique II-IV.md
│   │   ├── corpus_bergson_27k_dialogique.md
│   │   ├── corpus_kant_20k.txt.md
│   │   ├── Glossaire Conversationnel Spinoza - 12 Concepts.md
│   │   ├── glossaire_bergson_conversationnel.md
│   │   └── glossaire_kant_conversationnel.md
│   │
│   └── raw/txt/                    # Textes sources bruts
│
├── 📂 docs/
│   ├── notes/                      # Notes de développement
│   ├── references/                 # Documents de référence
│   ├── supports/                   # Guides de support
│   └── tutos/                      # Tutoriels
│
├── 📂 scripts/                     # Scripts utilitaires
│   ├── prepare_schemes_dataset.py
│   └── test_*.{js,html,sh}
│
├── 📂 garbage/                     # Archives/obsolètes
│
├── 📂 NUX_FT/                      # Repository Fine-tuning (séparé)
│   └── bergsonAndFriends/
│       ├── data/FT/
│       └── notebooks/
│
├── app.py                          # Application racine (legacy ?)
├── app.js                          # JavaScript racine (legacy ?)
├── rag_system.py                   # Système RAG principal
├── requirements.txt                # Dépendances racine
├── README.md
└── LICENSE
```

---

## 🌐 Structure Distante (GitHub)

### Repository Principal : `bergsonAndFriends`
- **URL :** `https://github.com/FJDaz/bergsonAndFriends` (si configuré)
- **Branche :** `main`
- **Contenu :** Code source principal

### Repository Fine-tuning : `NUX_FT`
- **URL :** `https://github.com/FJDaz/NUX_FT`
- **Branche :** `main`
- **Contenu :**
  - Datasets fine-tuning
  - Notebooks Colab
  - Scripts de préparation

### Repository Spinoza Secours : `Spinoza_secours`
- **URL :** `https://github.com/FJDaz/Spinoza_secours`
- **Branche :** `main`
- **Contenu :**
  - Code Space HF secours
  - Frontend `index_spinoza.html`
  - Prompts optimisés

---

## 🔗 Dépendances et Liens

### Hugging Face Spaces

1. **`FJDaz/bergsonAndFriends`** (3_PHI_HF)
   - **Modèle :** Qwen 2.5 14B + LoRA
   - **GPU :** L4 (24GB VRAM)
   - **Status :** ⏸️ Paused (à vérifier)
   - **Code source :** `3_PHI_HF/`

2. **`FJDaz/Spinoza_secours`** (Spinoza_Secours_HF)
   - **Modèle :** Mistral 7B + LoRA
   - **GPU :** ZeroGPU (on-demand)
   - **Status :** 🟢 Actif
   - **Code source :** `Spinoza_Secours_HF/`
   - **Lien GitHub :** `https://github.com/FJDaz/Spinoza_secours`

### Modèles Hugging Face

1. **`FJDaz/qwen-spinoza-niveau-b`**
   - **Base :** Qwen 2.5 14B
   - **LoRA :** Spinoza fine-tuned
   - **Usage :** Space `bergsonAndFriends`

2. **`FJDaz/mistral-7b-philosophes-lora`**
   - **Base :** Mistral 7B Instruct
   - **LoRA :** Schemes Niveau A
   - **Usage :** Space `Spinoza_secours`

### Services Externes

1. **Colab + ngrok** (Spinoza Secours)
   - **Backend :** FastAPI sur Colab
   - **Tunnel :** ngrok (URL publique)
   - **Frontend :** `fjdaz.com/bergsonandfriends/index_spinoza.html`

2. **Netlify** (legacy ?)
   - **Functions :** `/netlify/functions/`
   - **Status :** ⚠️ Crash récent (à investiguer)

3. **Railway** (legacy ?)
   - **URL :** `https://bergson-api-production.up.railway.app`
   - **Status :** ⚠️ À vérifier

---

## 📦 Dépendances Python

### Principales (requirements.txt)

```
torch
transformers
peft
bitsandbytes
gradio
fastapi
uvicorn
```

### Pour RAG

```
# Actuellement : recherche simple (pas de Whoosh)
# Potentiel : whoosh (moteur recherche full-text)
```

### Pour Fine-tuning

```
trl
datasets
accelerate
```

---

## 🔄 Flux de Données

### 1. Fine-tuning (NUX_FT)
```
Dataset Niveau A Schemes.txt
    ↓
prepare_schemes_dataset.py
    ↓
schemes_levelA_augmented.jsonl
    ↓
Colab (train_mistral_7b_lora_CLEAN.ipynb)
    ↓
Hugging Face Model Hub
    (FJDaz/mistral-7b-philosophes-lora)
```

### 2. Inference (Spinoza Secours)
```
Frontend (index_spinoza.html)
    ↓
API ngrok (Colab FastAPI)
    ↓
Modèle Mistral 7B + LoRA
    ↓
Prompt système hybride
    ↓
Réponse générée
```

### 3. RAG (si activé)
```
Corpus RAG (data/RAG/)
    ↓
rag_system.py
    ↓
Recherche passages pertinents
    ↓
Extraction idées + reformulation
    ↓
Injection dans prompt
```

---

## 📝 Notes Importantes

### Doublons Identifiés
- ⚠️ `bergson-and-friends/` vs `bergsonAndFriends/` (à nettoyer)
- ⚠️ Multiples `index.html` (à clarifier)
- ⚠️ Multiples `static/` (à clarifier)

### Fichiers Actifs
- ✅ `3_PHI_HF/app.py` : Space principal
- ✅ `Spinoza_Secours_HF/index_spinoza.html` : Frontend secours
- ✅ `Spinoza_Secours_HF/prompt_systeme_hybride.py` : Prompt optimisé
- ✅ `data/RAG/` : Corpus RAG
- ✅ `rag_system.py` : Système RAG

### Archives
- 📦 `garbage/` : Code obsolète
- 📦 `bergsonAndFriends_HF/` : Ancien Space (à vérifier)

---

**Dernière mise à jour :** 21 novembre 2025

