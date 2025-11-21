# 🏗️ Architecture Actuelle - Bergson and Friends avec Modal

**Date :** 18 novembre 2025  
**Stack :** Modal + Render + Netlify + Hugging Face

---

## 🎯 Modal : Qu'est-ce que c'est ?

### Type de Service

**Modal = Serverless ML Platform** (Plateforme ML Serverless)

**PAS vraiment un BaaS classique**, mais plutôt :
- **ML/AI Serverless Platform** - Plateforme serverless spécialisée ML/IA
- **GPU Serverless Platform** - Plateforme serverless avec GPU
- **Function-as-a-Service (FaaS) spécialisé ML** - FaaS pour machine learning

### Caractéristiques Modal

1. **Serverless ML** : Exécute du code ML/IA à la demande
2. **GPU à la demande** : Alloue GPU automatiquement (A10G, A100, etc.)
3. **Cold start** : Peut prendre 30-60s au premier appel (chargement modèle)
4. **Pay-per-use** : Paye seulement quand utilisé
5. **Volumes persistants** : Stockage de modèles (Modal Volumes)

### Comparaison avec BaaS

| Critère | BaaS Classique | Modal |
|---------|---------------|-------|
| **Type** | Backend général | ML/IA spécialisé |
| **GPU** | ❌ Non | ✅ Oui (automatique) |
| **Modèles ML** | ❌ Non | ✅ Oui (optimisé) |
| **Cold start** | ⚠️ Rapide | ⚠️ Lent (30-60s) |
| **Use case** | API générales | Modèles ML/IA |

**Verdict :** Modal est un **ML Serverless Platform**, pas un BaaS classique.

---

## 🏗️ Architecture Actuelle Complète

### Flux Complet

```
┌─────────────────────────────────────────┐
│    UTILISATEUR (Navigateur)             │
│    fjdaz.com/bergson/index_spinoza.html │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│    NETLIFY (Frontend + Functions)       │
│    - index_spinoza.html (hébergé)       │
│    - Functions serverless (si utilisé)   │
└─────────────────┬───────────────────────┘
                  │
                  │ Appel API
                  ▼
┌─────────────────────────────────────────┐
│    RENDER (Backend API)                 │
│    - snb_api_modal.py                   │
│    - Gère RAG + appelle Modal           │
│    URL: [render-url].onrender.com       │
└─────────────────┬───────────────────────┘
                  │
                  │ Appel API Modal
                  ▼
┌─────────────────────────────────────────┐
│    MODAL (Serverless ML)                │
│    - modal_spinoza_api.py               │
│    - Qwen 14B + LoRA Spinoza            │
│    - GPU A10G (à la demande)            │
│    URL: fjdaz--spinoza-api-chat.modal.run│
└─────────────────────────────────────────┘
                  │
                  │ (Optionnel)
                  ▼
┌─────────────────────────────────────────┐
│    HUGGING FACE SPACES (Backup)         │
│    - bergsonAndFriends Space             │
│    - Qwen 14B + LoRA Spinoza            │
│    - GPU A10G (24/7 si actif)           │
│    URL: fjdaz-bergsonandfriends.hf.space │
└─────────────────────────────────────────┘
```

---

## 📋 Rôle de Chaque Service

### 1. **Netlify** - Frontend + Functions (Optionnel)

**Rôle :**
- ✅ Héberge `index_spinoza.html` (frontend)
- ✅ Netlify Functions (si utilisé pour RAG)
- ✅ CDN global (rapide partout)

**Type :** JAMstack Hosting + Serverless Functions

**URL :** `https://[site].netlify.app` ou `fjdaz.com/bergson/`

---

### 2. **Render** - Backend API (PaaS)

**Rôle :**
- ✅ Héberge `snb_api_modal.py` (FastAPI)
- ✅ Gère RAG (extraction concepts, lookup)
- ✅ Appelle Modal API pour génération
- ✅ Gère historique conversation

**Type :** PaaS (Platform as a Service)

**Fichier :** `snb_api_modal.py`
- Endpoints : `/health`, `/init/spinoza`, `/chat/spinoza`
- Appelle : `https://fjdaz--spinoza-api-chat.modal.run`

**URL :** `https://[app].onrender.com`

---

### 3. **Modal** - Serverless ML (ML Platform)

**Rôle :**
- ✅ Exécute `modal_spinoza_api.py` (serverless)
- ✅ Charge Qwen 14B + LoRA Spinoza
- ✅ Génère réponses philosophiques
- ✅ GPU A10G (alloué automatiquement)

**Type :** ML Serverless Platform

**Fichier :** `modal_spinoza_api.py`
- Classe `SpinozaModel` avec GPU A10G
- Volume Modal : `spinoza-models` (stockage modèles)
- Endpoints : `/chat` (POST), `/health` (GET)

**URL :** `https://fjdaz--spinoza-api-chat.modal.run`

**Caractéristiques :**
- ⚠️ **Cold start** : 30-60s au premier appel
- ✅ **Pay-per-use** : Paye seulement quand utilisé
- ✅ **GPU automatique** : A10G alloué à la demande
- ✅ **Scaling** : Automatique selon trafic

---

### 4. **Hugging Face Spaces** - Backup (Optionnel)

**Rôle :**
- ✅ Backup du modèle (si Modal échoue)
- ✅ Alternative avec GPU 24/7
- ✅ API Gradio disponible

**Type :** ML/AI Model Hosting Platform

**URL :** `https://fjdaz-bergsonandfriends.hf.space`

**Statut :** Optionnel (backup si Modal indisponible)

---

## 🔄 Flux de Données Détaillé

### 1. Initialisation Conversation

```
Utilisateur ouvre index_spinoza.html
    ↓
Frontend appelle Render: GET /init/spinoza
    ↓
Render retourne question du bac + greeting
    ↓
Frontend affiche question
```

### 2. Chat (Question Utilisateur)

```
Utilisateur pose question
    ↓
Frontend appelle Render: POST /chat/spinoza
    ↓
Render:
  1. Extract concepts (RAG)
  2. Lookup passages RAG
  3. Format contexte RAG
  4. Appelle Modal: POST /chat
    ↓
Modal:
  1. Cold start? (30-60s si premier appel)
  2. Charge modèle (si pas déjà chargé)
  3. Génère réponse (Qwen 14B + LoRA)
  4. Retourne réponse
    ↓
Render:
  1. Reçoit réponse Modal
  2. Format réponse
  3. Retourne à frontend
    ↓
Frontend affiche réponse
```

---

## 📊 Comparaison Services

| Service | Type | Rôle | GPU | Coût | Cold Start |
|---------|------|------|-----|------|------------|
| **Netlify** | JAMstack | Frontend | ❌ | Gratuit | Rapide |
| **Render** | PaaS | Backend API | ❌ | Gratuit/Payant | Rapide |
| **Modal** | ML Serverless | Génération IA | ✅ A10G | Pay-per-use | ⚠️ 30-60s |
| **HF Spaces** | ML Platform | Backup | ✅ A10G | ~$1/h | ⚠️ 30-60s |

---

## 💰 Coûts

### Modal
- **Pay-per-use** : Paye seulement quand appelé
- **GPU A10G** : ~$0.50-1.00/h d'utilisation
- **Cold start** : Pas de coût si pas utilisé
- **Volume** : Stockage modèles (gratuit ou payant selon taille)

### Render
- **Plan gratuit** : Limité (veille après inactivité)
- **Plan payant** : ~$7-25/mois (selon ressources)

### Netlify
- **Plan gratuit** : 100GB bande passante/mois
- **Functions** : 100k invocations/mois gratuites

### HF Spaces
- **A10G** : ~$1.00/h (24/7 si actif)
- **Total/mois** : ~$720 si 24/7

---

## ✅ Avantages Architecture Actuelle

### 1. **Coût Optimisé**
- Modal : Pay-per-use (pas de coût si pas utilisé)
- Render : Gratuit ou payant selon usage
- Netlify : Gratuit pour sites simples
- **Total** : Beaucoup moins cher que HF Spaces 24/7

### 2. **Flexibilité**
- Modal : Scaling automatique
- Render : Facile à déployer
- Netlify : CDN global

### 3. **Performance**
- Modal : GPU A10G (même que HF Spaces)
- Render : Backend rapide
- Netlify : CDN rapide

### 4. **Backup**
- HF Spaces : Disponible si Modal échoue

---

## ⚠️ Points d'Attention

### 1. **Cold Start Modal**
- **Problème** : 30-60s au premier appel
- **Solution** : Keep-alive ou warmup (si payant)

### 2. **Timeout Render**
- **Problème** : Timeout si Modal prend trop de temps
- **Solution** : Timeout configuré à 120s dans `snb_api_modal.py`

### 3. **Dépendance Modal**
- **Problème** : Si Modal down, tout le système down
- **Solution** : HF Spaces en backup

---

## 🔧 Configuration Actuelle

### Fichiers Clés

1. **`snb_api_modal.py`** (Render)
   - Backend API FastAPI
   - Appelle Modal API
   - Gère RAG

2. **`modal_spinoza_api.py`** (Modal)
   - Code Modal serverless
   - Charge modèle Qwen 14B + LoRA
   - Expose API `/chat`

3. **`Procfile`** (Render)
   - `web: python3 snb_api_modal.py`

4. **`index_spinoza.html`** (Netlify/fjdaz.com)
   - Frontend interface
   - Appelle Render API

---

## 📝 URLs Actuelles

- **Frontend** : `fjdaz.com/bergson/index_spinoza.html`
- **Render API** : `https://[app].onrender.com` (à vérifier)
- **Modal API** : `https://fjdaz--spinoza-api-chat.modal.run`
- **HF Space** : `https://fjdaz-bergsonandfriends.hf.space` (backup)

---

## 🎯 Résumé Architecture

**Stack :**
1. **Netlify** → Frontend (JAMstack)
2. **Render** → Backend API (PaaS)
3. **Modal** → Génération IA (ML Serverless)
4. **HF Spaces** → Backup (ML Platform)

**Flux :**
```
Frontend → Render → Modal → Réponse IA
```

**Modal = ML Serverless Platform** (pas BaaS classique)

---

**Dernière mise à jour :** 18 novembre 2025

