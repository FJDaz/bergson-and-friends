# ⚙️ Configuration Minimale - Qwen 14B

**Modèle :** Qwen/Qwen2.5-14B-Instruct  
**Fine-tuning :** LoRA Spinoza Niveau B (adapter)

---

## 📊 Besoins en VRAM par Quantization

| Quantization | VRAM Modèle | VRAM + Overhead | GPU Minimum | Status |
|--------------|-------------|-----------------|-------------|--------|
| **FP16** (sans quant) | ~28GB | ~30GB | A100 (40GB) | ❌ Trop lourd |
| **8-bit** | ~14GB | ~16GB | **A10G (24GB)** ✅ | ⚠️ T4 limite |
| **4-bit** | ~7GB | ~9GB | **T4 (16GB)** ✅ | ✅ Recommandé T4 |

---

## ✅ Configuration 8-bit (Actuelle)

### VRAM Requise
- **Modèle :** ~14GB
- **Overhead :** ~2GB (activations, cache)
- **Total :** ~16GB minimum

### GPU Compatibles

#### ✅ **A10G (24GB VRAM)** - RECOMMANDÉ
- **VRAM disponible :** 24GB
- **Marge :** 8GB (confortable)
- **Status :** ✅ Fonctionne parfaitement
- **Coût HF :** ~$1.00/h
- **Coût RunPod :** ~$1.00/h

#### ⚠️ **T4 Small (16GB VRAM)** - LIMITE
- **Spécifications :** 4 vCPU, 15GB RAM, 16GB VRAM
- **VRAM disponible :** 16GB
- **Marge :** 0GB (juste suffisant théoriquement)
- **Status :** ❌ **Ne fonctionne PAS en 8-bit** (expérience confirmée)
- **Problème :** Modèle dispatché sur CPU/disk → Runtime error
- **Raison :** Overhead système + activations = dépassement
- **Note RAM :** 15GB RAM peut être limite si offload CPU nécessaire
- **Solution :** Utiliser 4-bit (passe avec marge)

#### ⚠️ **T4 Medium (16GB VRAM)** - LIMITE
- **Spécifications :** 8 vCPU, 30GB RAM, 16GB VRAM
- **VRAM disponible :** 16GB
- **Marge :** 0GB (juste suffisant théoriquement)
- **Status :** ❌ **Ne fonctionne PAS en 8-bit** (expérience confirmée)
- **Problème :** Modèle dispatché sur CPU/disk → Runtime error
- **Raison :** Overhead système + activations = dépassement
- **Note RAM :** 30GB RAM largement suffisante
- **Solution :** Utiliser 4-bit (passe avec marge)

### Code Configuration 8-bit

```python
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0,
    llm_int8_has_fp16_weight=False,
)

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-14B-Instruct",
    quantization_config=quantization_config,
    device_map="auto",
    torch_dtype=torch.float16,
)
```

---

## ✅ Configuration 4-bit (Minimale pour T4)

### VRAM Requise
- **Modèle :** ~7GB
- **Overhead :** ~2GB
- **Total :** ~9GB minimum

### GPU Compatibles

#### ✅ **T4 Small (16GB VRAM)** - FONCTIONNE (avec précaution)
- **Spécifications :** 4 vCPU, 15GB RAM, 16GB VRAM
- **VRAM disponible :** 16GB
- **Marge :** 7GB (confortable avec 4-bit)
- **Status :** ✅ Devrait fonctionner en 4-bit (version testée dans archive)
- **Coût HF :** ~$0.40/h
- **Coût RunPod :** ~$0.30/h
- **Note RAM :** 15GB RAM peut être limite si offload CPU nécessaire (éviter)
- **Recommandation :** Forcer tout sur GPU (pas d'offload CPU)

#### ✅ **T4 Medium (16GB VRAM)** - FONCTIONNE
- **Spécifications :** 8 vCPU, 30GB RAM, 16GB VRAM
- **VRAM disponible :** 16GB
- **Marge :** 7GB (confortable avec 4-bit)
- **Status :** ✅ Devrait fonctionner en 4-bit (version testée dans archive)
- **Coût HF :** ~$0.40/h
- **Coût RunPod :** ~$0.30/h
- **Note :** RAM (30GB) largement suffisante pour le modèle

#### ✅ **A10G (24GB VRAM)** - SURDIMENSIONNÉ
- **VRAM disponible :** 24GB
- **Marge :** 15GB (très confortable)
- **Status :** ✅ Fonctionne (mais 8-bit préférable pour qualité)

### Code Configuration 4-bit

```python
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,  # 4-bit au lieu de 8-bit
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,  # Double quantization pour meilleure qualité
    bnb_4bit_quant_type="nf4",  # NormalFloat4 - meilleure qualité
)

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-14B-Instruct",
    quantization_config=quantization_config,
    device_map="auto",
    torch_dtype=torch.float16,
)
```

**Note :** Version 4-bit trouvée dans `spinoza_NB_archive/version_23f53af/app.py` (non déployée)

---

## 🎯 Recommandations par Cas d'Usage

### Cas 1 : Budget Limité (T4 Small/Medium)

**Configuration :** 4-bit  
**GPU :** 
- **T4 Small :** 4 vCPU, 15GB RAM, 16GB VRAM (⚠️ RAM limite)
- **T4 Medium :** 8 vCPU, 30GB RAM, 16GB VRAM (✅ Recommandé)  
**Coût :** ~$0.30-0.40/h  
**Qualité :** Légèrement inférieure à 8-bit (acceptable)

**Code :**
```python
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)
```

### Cas 2 : Qualité Optimale (A10G)

**Configuration :** 8-bit  
**GPU :** A10G (24GB)  
**Coût :** ~$1.00/h  
**Qualité :** Meilleure (moins de perte de précision)

**Code :**
```python
quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0,
    llm_int8_has_fp16_weight=False,
)
```

### Cas 3 : Usage Ponctuel (Démos)

**Configuration :** 4-bit sur T4  
**Avantage :** Coût réduit (~$0.30/h vs $1.00/h)  
**Qualité :** Suffisante pour démos

---

## ⚠️ Limitations Connues

### 8-bit sur T4 : ❌ Ne Fonctionne PAS

**Expérience confirmée :**
- Space `spinoza_NB` (T4) → Runtime error
- Modèle dispatché sur CPU/disk
- Cause : VRAM insuffisante (14GB + overhead > 16GB)

**Solution :** Utiliser 4-bit ou passer à A10G

### 4-bit : Qualité Légèrement Inférieure

**Trade-off :**
- ✅ Moins de VRAM (passe sur T4)
- ✅ Moins cher (~$0.30/h vs $1.00/h)
- ⚠️ Légère perte de qualité (acceptable pour la plupart des cas)

---

## 📋 Comparaison Rapide

| Critère | 8-bit (A10G) | 4-bit (T4 Small) | 4-bit (T4 Medium) |
|---------|-------------|------------------|-------------------|
| **VRAM** | ~16GB | ~9GB | ~9GB |
| **GPU** | A10G (24GB) | T4 Small (16GB VRAM) | T4 Medium (16GB VRAM) |
| **CPU/RAM** | - | 4 vCPU, 15GB RAM | 8 vCPU, 30GB RAM |
| **Coût/h** | $1.00 | $0.30-0.40 | $0.30-0.40 |
| **Qualité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Status** | ✅ Fonctionne | ⚠️ Fonctionne (RAM limite) | ✅ Devrait fonctionner |
| **Recommandé pour** | Production | Budget très limité | Budget limité |

---

## 🔧 Migration 8-bit → 4-bit

### Modifications à Apporter

**Fichier :** `app.py` (ou `bergsonAndFriends/app.py`)

**Avant (8-bit) :**
```python
quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0,
    llm_int8_has_fp16_weight=False,
)
```

**Après (4-bit) :**
```python
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)

# Pour T4 Small (RAM limite) : Forcer tout sur GPU
model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=quantization_config,
    device_map="auto",  # Ou device_map={0: "15GiB", "cpu": "0GiB"} pour forcer GPU
    torch_dtype=torch.float16,
    max_memory={0: "15GiB", "cpu": "0GiB"},  # Forcer GPU uniquement (T4 Small)
)
```

**Aucune autre modification nécessaire** (le reste du code reste identique)

---

## 💡 Conclusion

### Configuration Minimale Recommandée

**Pour T4 Small (4 vCPU, 15GB RAM, 16GB VRAM) :**
- ✅ **4-bit** : ~7GB VRAM → Passe avec marge
- ⚠️ **Attention RAM :** 15GB peut être limite (forcer GPU uniquement)
- ❌ **8-bit** : ~14GB VRAM → Ne passe PAS (confirmé)

**Pour T4 Medium (8 vCPU, 30GB RAM, 16GB VRAM) :**
- ✅ **4-bit** : ~7GB VRAM → Passe avec marge (recommandé)
- ✅ **RAM :** 30GB largement suffisante
- ❌ **8-bit** : ~14GB VRAM → Ne passe PAS (confirmé)

**Pour A10G (24GB VRAM) :**
- ✅ **8-bit** : ~14GB VRAM → Passe avec marge (recommandé)
- ✅ **4-bit** : ~7GB VRAM → Passe mais surdimensionné

### Recommandation Finale

- **Budget très limité :** 4-bit sur T4 Small (~$0.30/h) ⚠️ RAM limite
- **Budget limité :** 4-bit sur T4 Medium (~$0.30-0.40/h) ✅ Recommandé
- **Qualité optimale :** 8-bit sur A10G (~$1.00/h)
- **Usage actuel :** 8-bit sur A10G (fonctionne parfaitement)

---

**Dernière mise à jour :** Novembre 2025  
**Source :** Analyse code + expérience Space `spinoza_NB` (T4) vs `bergsonAndFriends` (A10G)

