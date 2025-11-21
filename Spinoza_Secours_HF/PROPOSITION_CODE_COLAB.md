# 📝 Proposition : Code Colab pour Spinoza Secours

**Date :** 21 novembre 2025  
**Status :** ⏸️ **PROPOSITION** - En attente validation  
**⚠️ NE PAS MODIFIER LE CODE COLAB SANS VALIDATION**

---

## 🎯 Objectif

Créer un code Colab complet qui utilise le **prompt système hybride optimisé** pour Spinoza Secours.

---

## 📋 Contenu Proposé

### 1. **Installation Dépendances**
```python
!pip install -q pyngrok fastapi uvicorn transformers peft accelerate bitsandbytes torch
```

### 2. **Imports**
```python
from pyngrok import ngrok
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading, uvicorn, random, time, re, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
```

### 3. **Configuration ngrok**
```python
NGROK_TOKEN = "TON_TOKEN_ICI"
ngrok.set_auth_token(NGROK_TOKEN)
!lsof -ti:8000 | xargs kill -9 2>/dev/null; sleep 1
```

### 4. **Prompt Système Hybride** (depuis `prompt_systeme_hybride.py`)
- `SYSTEM_PROMPT_SPINOZA` (~250 tokens)
- `INSTRUCTIONS_CONTEXTUELLES` (accord/confusion/résistance/neutre)
- `INSTRUCTION_RAG` (optionnel)
- `construire_prompt_complet(contexte, use_rag_instruction=True)`

### 5. **Détection Contexte**
```python
def detecter_contexte(user_input: str) -> str:
    # Retourne "accord", "confusion", "resistance", "neutre"
```

### 6. **Post-Processing**
- `nettoyer_reponse(text)` - Nettoie annotations, emojis, espaces
- `limiter_phrases(text, max_phrases=3)` - Limite à 3 phrases

### 7. **Chargement Modèle**
```python
@torch.no_grad()
def load_model():
    # Charge Mistral 7B + LoRA
    # Device: CUDA (T4 sur Colab) avec quantization 4-bit
    # Adapter: "FJDaz/mistral-7b-philosophes-lora"
    return model, tokenizer
```

### 8. **Fonction `spinoza_repond(message)`**
- Détecte contexte
- Construit prompt adaptatif
- Génère réponse avec modèle
- Post-processe
- Retourne réponse nettoyée

### 9. **API FastAPI**
- `/health` - Vérification état
- `/init` - Initialisation conversation
- `/chat` - POST avec message utilisateur
- CORS configuré

### 10. **Lancement Serveur + ngrok**
- Thread background pour FastAPI
- Tunnel ngrok sur port 8000
- Affichage URL publique

---

## ⚙️ Paramètres Configurables

| Paramètre | Valeur Proposée | Alternative |
|-----------|----------------|-------------|
| `max_new_tokens` | 150 | 100-200 selon besoin |
| `temperature` | 0.7 | 0.5-0.9 |
| `top_p` | 0.9 | 0.8-0.95 |
| `use_rag_instruction` | `True` | ✅ Instructions seulement (pas d'injection) |
| `device` | `"cuda"` | T4 sur Colab |
| `adapter_name` | `"FJDaz/mistral-7b-philosophes-lora"` | ✅ Confirmé |

---

## 📊 Estimation Tokens

| Composant | Tokens |
|-----------|--------|
| Prompt système base | ~250 |
| Instruction contextuelle | ~30-50 |
| Instruction RAG | ~50 |
| **Total prompt** | **~330-350** |
| Historique (4 échanges) | ~300 |
| Message utilisateur | ~50 |
| **Total par requête** | **~680-700** |

---

## ✅ Avantages

1. **Prompt optimisé** : ~250 tokens (vs ~400 pour version complète)
2. **Adaptatif** : S'adapte au contexte (accord/confusion/résistance/neutre)
3. **Première personne** : Explicite dans le prompt
4. **Schèmes logiques** : Intégrés dans le prompt
5. **Économie tokens** : RAG par instructions (pas d'injection)

---

## ⚠️ Points d'Attention

1. **Token ngrok** : À remplacer par le vrai token
2. **Adapter LoRA** : Vérifier le nom exact de l'adapter
3. **Device** : CPU par défaut (changer en CUDA si GPU)
4. **RAG** : Actuellement par instructions (pas d'injection passages)

---

## 🔄 Modifications Possibles

### Option A : RAG Disabled (Économie Max)
```python
# Dans spinoza_repond()
system_prompt = construire_prompt_complet(contexte, use_rag_instruction=False)
```
**Économie :** ~50 tokens

### Option B : Prompt Minimal (Économie Max)
```python
# Utiliser version minimaliste (~80 tokens)
SYSTEM_PROMPT_MINIMAL = """Tu ES Spinoza. Première personne. Tutoie l'élève..."""
```
**Économie :** ~170 tokens

### Option C : RAG Sélectif (Si besoin)
```python
# Ajouter recherche RAG si contexte confusion/accord
if contexte in ["confusion", "accord"]:
    # Recherche RAG + injection passages
```

---

## 📝 Structure Fichier Proposée

```
colab_spinoza_secours_complet.py
├── Installation dépendances
├── Imports
├── Config ngrok
├── Prompt système hybride
├── Détection contexte
├── Post-processing
├── Chargement modèle
├── Fonction spinoza_repond()
├── API FastAPI
└── Lancement serveur + ngrok
```

---

## 🔧 Script Supplémentaire Proposé

### Objectif
Script séparé pour tester/valider le prompt système **SANS toucher** au chargement du modèle ni à l'API.

### Contenu Proposé

#### Option 1 : Script de Test Prompt (✅ CHOISI)

```python
# test_prompt_systeme.py
# - Teste le prompt système avec différents contextes
# - Affiche le prompt généré (sans génération modèle)
# - Valide la structure du prompt
# - Estime les tokens
```

**Fonctions :**
- `test_prompt_contextes()` - Teste tous les contextes (accord/confusion/résistance/neutre)
- `afficher_prompt(contexte)` - Affiche le prompt généré
- `estimer_tokens(prompt)` - Estime le nombre de tokens
- `valider_structure(prompt)` - Vérifie que le prompt contient les éléments requis

**Avantages :**
- ✅ Teste le prompt sans charger le modèle
- ✅ Rapide (pas d'inference)
- ✅ Permet de valider avant utilisation réelle
- ✅ **Indépendant du frontend** (teste juste le prompt)

**Note BM25 :** Le test BM25 (Lunr.js) nécessite le frontend. Workflow :
1. **Colab (Option 1)** → Test prompt système → Validation prompt
2. **Frontend + API** → Test BM25 (Lunr.js) → Validation RAG côté client

#### Option 2 : Script Utilitaires (Si besoin)
```python
# utils_prompt.py
# - Fonctions utilitaires pour le prompt
# - Formatage, validation, etc.
```

**Fonctions possibles :**
- `formater_prompt(prompt, contexte)` - Formatage avancé
- `valider_premiere_personne(prompt)` - Vérifie première personne
- `extraire_schemes(prompt)` - Extrait les schèmes logiques mentionnés

**⚠️ Suggestion :** Seulement si vraiment nécessaire

---

## ✅ Réponses Validation

1. **Adapter LoRA** : `"FJDaz/mistral-7b-philosophes-lora"` (trouvé dans `app.py`)
2. **Device** : **CUDA** (T4 sur Colab) - Utiliser `device="cuda"` avec quantization 4-bit
3. **RAG** : **Instructions seulement** (pas d'injection passages)
4. **Tokens** : **Priorité qualité** (pas d'économie maximale)
5. **Paramètres génération** : `max_new_tokens=150` pour démarrer, ajustable selon tests
6. **Script supplémentaire** : **Option 1 (Test Prompt)** - Tests en Colab avant frontend

### 📝 Clarification BM25 (Lunr.js)

**Question :** Besoin de frontend pour tester BM25 en même temps ?

**Réponse :**
- **Script Option 1 (Test Prompt)** : Teste le prompt système **sans modèle ni frontend** (rapide, validation structure)
- **Test BM25 (Lunr.js)** : Nécessite le **frontend** (`index_spinoza.html`) car c'est côté client (JavaScript)
- **Recommandation** : 
  1. D'abord tester le prompt en Colab (Option 1) - validation prompt
  2. Ensuite tester BM25 avec frontend - validation RAG côté client

**Workflow proposé :**
```
Colab (Option 1) → Test prompt système → ✅ Prompt validé
    ↓
Frontend + API → Test BM25 (Lunr.js) → ✅ RAG validé
```

---

**Status :** ⏸️ En attente validation avant implémentation

