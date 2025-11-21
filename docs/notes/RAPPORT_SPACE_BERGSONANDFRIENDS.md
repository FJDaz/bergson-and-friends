# 📊 Rapport d'Analyse - Space HF `bergsonAndFriends`

**Date :** Novembre 2025  
**Space URL :** https://huggingface.co/spaces/FJDaz/bergsonAndFriends/tree/main  
**Status :** ⏸️ Paused (selon la page HF)

---

## 📁 Fichiers Présents sur le Space

### Fichiers Principaux

| Fichier | Taille | Description | Dernière Modif |
|---------|--------|-------------|----------------|
| `app.py` | 12.2 KB | **Application principale Python** (360 lignes) | 1 jour (Enable API) |
| `index.html` | 9.83 KB | Interface frontend HTML (252 lignes) | 4 jours |
| `requirements.txt` | 132 Bytes | Dépendances Python | 2 jours |
| `README.md` | 293 Bytes | Description du Space | 2 mois |

### Fichiers de Données (Corpus)

| Fichier | Taille | Description |
|---------|--------|-------------|
| `01_esthetique_transcendantale.txt` | 12.2 KB | Corpus Kant - Esthétique transcendantale |
| `02_analytique_des_concepts.txt` | 2.52 KB | Corpus Kant - Analytique des concepts |
| `03_antinomies_selection.txt` | 5.22 KB | Corpus Kant - Antinomies |
| `Éthique_(Saisset,_1861)_Partie_I_clean.txt` | 92.6 KB | Corpus Spinoza - Éthique Partie I |
| `essai_conscience.txt` | 364 KB | Corpus Bergson - Essai sur la conscience |

### Fichiers de Test

| Fichier | Taille | Description |
|---------|--------|-------------|
| `test-bergson-debug.html` | 1.12 KB | Page de test/debug |
| `test-bergson.html` | 1.1 KB | Page de test |

### Dossier `netlify/functions/`

| Fichier | Description |
|---------|-------------|
| `bergson.js` | Fonction Netlify pour Bergson |
| `kant.js` | Fonction Netlify pour Kant |
| `spinoza.js` | Fonction Netlify pour Spinoza (version principale) |
| `spinoza.js.backup` | Backup de spinoza.js |
| `spinoza.js.together_ai_backup` | Backup Together AI |

### Dossier `static/`

- **Fonts :** 14 fichiers `.woff` et `.woff2` (GrotesqueMTStd, LetterGothicStd)
- **Images :** 5 fichiers PNG (Bergson.png, Kant.png, Spinoza.png, LOGO, Submit.png)
- **CSS :** `style.css`, `responsive.css`
- **JS :** `app.js` (non présent dans le Space, hébergé sur fjdaz.com)

---

## 🐍 Système Python (`app.py`)

### Architecture

**Lignes de code :** 360  
**Langage :** Python 3  
**Framework :** Gradio 4.44.0+

### Modèle Utilisé

```python
BASE_MODEL = "Qwen/Qwen2.5-14B-Instruct"
ADAPTER_MODEL = "FJDaz/qwen-spinoza-niveau-b"
```

- **Modèle de base :** Qwen 2.5 14B Instruct
- **Fine-tuning :** LoRA Spinoza Niveau B (adapter)
- **Quantization :** 8-bit (BitsAndBytesConfig)
- **Hardware requis :** A10G (24GB VRAM) - confirmé fonctionnel

### Fonctionnalités Implémentées

#### 1. **Détection Contextuelle V2** (lignes 22-58)
- Détection de 4 contextes :
  - `accord` : Oui explicite
  - `confusion` : Incompréhension
  - `resistance` : Opposition
  - `neutre` : Par défaut

#### 2. **Prompts Système Adaptatifs V2** (lignes 64-101)
- **3 variantes de prompts Spinoza** (choix aléatoire)
- Adaptation selon contexte détecté
- Règles strictes : tutoiement, concision (2-3 phrases max), questionnement

#### 3. **Post-Processing V2** (lignes 107-131)
- Nettoyage annotations méta
- Suppression emojis
- Limitation phrases (max 3)

#### 4. **Classe DialogueSpinozaV2** (lignes 137-203)
- Gestion historique conversation (4 derniers échanges)
- Génération avec paramètres optimisés :
  - `max_new_tokens=150` (concis)
  - `temperature=0.7`
  - `top_p=0.9`

#### 5. **Questions BAC** (lignes 258-278)
- **15 questions authentiques** du baccalauréat
- Sélection aléatoire pour amorce conversation

#### 6. **Interface Gradio** (lignes 284-347)
- Chatbot avec historique
- Bouton "Nouvelle question"
- Bouton "Effacer"
- **API activée :** `show_api=True`, `api_name="/chat_function"`

### ⚠️ **IMPORTANT : Philosophes Implémentés**

**Dans `app.py` : UN SEUL PHILOSOPHE = SPINOZA**

- ❌ **Bergson :** Non implémenté dans le code Python
- ❌ **Kant :** Non implémenté dans le code Python
- ✅ **Spinoza :** Seul philosophe implémenté

**Conséquence :** Le Space HF `bergsonAndFriends` ne gère que Spinoza, même si l'interface frontend montre 3 philosophes.

---

## 🌐 Système JavaScript/Frontend (`index.html`)

### Architecture Frontend

**Lignes de code :** 252  
**Framework :** Vanilla JavaScript (pas de framework)

### Philosophes Affichés

**3 philosophes dans l'interface :**
1. **Henri Bergson** (`#bergson`)
2. **Immanuel Kant** (`#kant`)
3. **Baruch Spinoza** (`#spinoza`)

### Fonctionnalités Frontend

#### 1. **Version Desktop**
- 3 philosophes affichés côte à côte
- Dialogue individuel par philosophe
- Historique conversation par philosophe

#### 2. **Version Mobile**
- Sélection philosophe
- Conversation dédiée
- Navigation entre philosophes

#### 3. **Système Adaptatif** (lignes 174-195)
- Historique conversation stocké par philosophe
- Transmission historique aux fonctions Netlify
- Questions BAC Spinoza intégrées (15 questions)

### Appels API

**Frontend → Netlify Functions :**
```javascript
fetch(`/.netlify/functions/${philosopherId}`, {
    method: 'POST',
    body: JSON.stringify({
        question: question,
        history: conversationHistories[philosopherId] || []
    })
})
```

**Problème identifié :**
- Frontend appelle `/.netlify/functions/bergson`, `/.netlify/functions/kant`, `/.netlify/functions/spinoza`
- Mais le Space HF ne gère que Spinoza
- Les fonctions Netlify doivent gérer la redirection vers le Space HF avec injection de style

---

## 🎭 Prompts Système

### Définition (dans `src/prompts.js`)

**3 prompts système complets :**

#### 1. **Bergson** (lignes 8-26)
- Style : Métaphores temporelles, opposition durée/temps spatialisé
- Schèmes : Opposition, Analogie, Implication
- Méthode : Critique → Révélation → Métaphores

#### 2. **Kant** (lignes 28-46)
- Style : Distinctions a priori/a posteriori, architecture critique
- Schèmes : Distinction, Implication, Condition
- Méthode : Conditions transcendantales → Distinctions → Limites

#### 3. **Spinoza** (lignes 48-66)
- Style : Géométrie des affects, identification Dieu=Nature
- Schèmes : Identité, Implication, Causalité
- Méthode : Nécessité causale → Distinction servitude/liberté → Exemples

### Injection dans le Message

**Problème technique :** Gradio ne supporte pas les system prompts séparés.

**Solution actuelle :** Injection du prompt système dans le message utilisateur :

```python
# Dans app.py, le Space reçoit :
enrichedMessage = f"{systemPrompt}\n\nContexte RAG:\n{ragContext}\n\nQuestion: {userMessage}"
```

**Dans `src/prompts.js` (Netlify) :**
```javascript
const enrichedMessage = `${systemPrompt}

Contexte pertinent (extraits de la littérature) :
${ragContext}

Question de l'élève : ${userMessage}`;
```

---

## 🔄 Architecture Globale

### Flux Complet

```
Frontend (fjdaz.com/bergsonandfriends)
    ↓ index.html (3 philosophes affichés)
    ↓
Netlify Functions (philosopher_rag.js)
    ↓ Détection philosophe + RAG lookup
    ↓
Space HF (bergsonAndFriends)
    ↓ app.py (Spinoza uniquement)
    ↓ Qwen 14B + LoRA Spinoza
    ↓
Réponse adaptée au philosophe
```

### Système RAG

**Fichiers corpus (dans `data/RAG/`) :**
- `corpus_bergson_27k_dialogique.md` (27k tokens)
- `corpus_kant_20k.txt.md` (20k tokens)
- `Corpus Spinoza Dialogique 18k - Éthique II-IV.md` (18k tokens)

**Glossaires :**
- `glossaire_bergson_conversationnel.md`
- `glossaire_kant_conversationnel.md`
- `Glossaire Conversationnel Spinoza - 12 Concepts.md`

**Fonctionnement :**
1. Extraction concepts de la question
2. Lookup RAG dans corpus + glossaire
3. Formatage contexte RAG
4. Injection dans message enrichi

---

## 📊 Résumé Technique

### Technologies

| Composant | Technologie | Version |
|-----------|------------|---------|
| **Backend** | Python | 3.10+ |
| **Framework** | Gradio | ≥4.44.0 |
| **Modèle** | Qwen 2.5 14B | Instruct |
| **Fine-tuning** | LoRA (PEFT) | ≥0.10.0 |
| **Quantization** | BitsAndBytes | 8-bit |
| **Frontend** | HTML/CSS/JS | Vanilla |
| **API** | Netlify Functions | Node.js |

### Dépendances Python (`requirements.txt`)

```
gradio>=4.44.0
torch
transformers>=4.30.0
sentence-transformers
faiss-cpu
bitsandbytes
accelerate
huggingface-hub
peft>=0.10.0
numpy
```

### Configuration Hardware

- **GPU :** A10G-small (24GB VRAM, 46GB RAM)
- **Status :** ✅ Fonctionnel (confirmé)
- **Coût :** ~$1.00/h

---

## ⚠️ Points d'Attention

### 1. **Décalage Frontend/Backend**

**Problème :**
- Frontend affiche 3 philosophes (Bergson, Kant, Spinoza)
- Backend Space HF ne gère que Spinoza
- Les fonctions Netlify doivent injecter le style du philosophe dans le message

**Solution actuelle :**
- `philosopher_rag.js` injecte le prompt système du philosophe dans le message
- Le Space HF reçoit un message enrichi avec le style du philosophe
- Le modèle Spinoza répond "comme" le philosophe demandé

**Limitation :**
- Le modèle n'est fine-tuné que sur Spinoza
- Les réponses Bergson/Kant sont générées par prompt engineering uniquement
- Qualité potentiellement inférieure pour Bergson/Kant vs Spinoza

### 2. **Status Space : Paused**

**Selon la page HF :** Le Space est marqué "Paused"
- Possiblement arrêté manuellement
- Ou suspendu pour impayés
- Nécessite redémarrage pour fonctionner

### 3. **API Activée**

**Configuration :**
```python
interface.queue()
interface.launch(
    show_api=True,  # ✅ API activée
    api_name="/chat_function"  # ✅ Endpoint défini
)
```

**Endpoint disponible :**
- `/chat_function` (double slash dans Gradio)
- Format : `{message: str, history: List[List[str, str]]}`

---

## 📈 Statistiques

### Code

- **Python :** 360 lignes (`app.py`)
- **HTML :** 252 lignes (`index.html`)
- **JavaScript :** ~200 lignes (dans `index.html` + `app.js` externe)
- **Total :** ~800 lignes de code

### Données

- **Corpus total :** ~65k tokens (Bergson 27k + Kant 20k + Spinoza 18k)
- **Questions BAC :** 15 questions Spinoza
- **Fichiers texte :** 5 fichiers corpus

### Philosophes

- **Affichés frontend :** 3 (Bergson, Kant, Spinoza)
- **Implémentés backend :** 1 (Spinoza uniquement)
- **Prompts système :** 3 (tous définis dans `src/prompts.js`)

---

## 🎯 Conclusion

### État Actuel

✅ **Fonctionnel :**
- Space HF avec modèle Spinoza opérationnel
- Interface frontend complète (3 philosophes)
- Système RAG intégré
- API Gradio activée

⚠️ **Limitations :**
- Backend ne gère que Spinoza (pas de fine-tuning Bergson/Kant)
- Style Bergson/Kant généré par prompt engineering uniquement
- Space actuellement "Paused" sur HF

### Recommandations

1. **Redémarrer le Space** si suspendu
2. **Considérer fine-tuning** pour Bergson et Kant (si budget)
3. **Documenter** le décalage frontend/backend
4. **Tester** la qualité des réponses Bergson/Kant vs Spinoza

---

**Dernière mise à jour :** Novembre 2025  
**Source :** Analyse du Space HF + fichiers locaux

