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
    # Device: CPU (ou CUDA si GPU)
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
| `use_rag_instruction` | `True` | `False` pour économie max |
| `device` | `"cpu"` | `"cuda"` si GPU |
| `adapter_name` | `"FJDaz/mistral-7b-philosophes-lora"` | À ajuster si différent |

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

## ❓ Questions pour Validation

1. **Adapter LoRA** : Quel est le nom exact de l'adapter à utiliser ?
2. **Device** : CPU ou CUDA (GPU disponible ?)
3. **RAG** : Instructions seulement ou injection passages ?
4. **Tokens** : Priorité économie ou qualité ?
5. **Paramètres génération** : `max_new_tokens=150` OK ?

---

**Status :** ⏸️ En attente validation avant implémentation

