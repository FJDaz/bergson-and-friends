# 📊 État Projet - Session 18 Nov 2025 (Synthèse Claude Code)

**Date**: 18 novembre 2025, 23h00
**Session**: Déploiement Spinoza + RAG + tentative intégration HF Space

---

## ✅ CE QUI FONCTIONNE (Production Ready)

### 1. Frontend Spinoza - OPÉRATIONNEL
- **Fichier**: `/index_spinoza.html`
- **URL Production**: https://fjdaz.com/bergson/index_spinoza.html
- **Backend**: Railway Mock + RAG
- **Features**:
  - ✅ Interface responsive (desktop + mobile)
  - ✅ Submit sur Enter (Shift+Enter nouvelle ligne)
  - ✅ Question du bac au démarrage
  - ✅ Historique conversation
  - ✅ Markdown rendering (**bold**)
  - ✅ RAG passages en console

### 2. Backend Railway Mock + RAG - STABLE
- **URL**: https://bergson-api-production.up.railway.app
- **Fichier**: `snb_api_mock.py`
- **Status**: ✅ Déployé et fonctionnel
- **Endpoints**:
  - `/health` → `{"status":"ok","mode":"mock"}`
  - `/init/spinoza` → Question du bac + greeting
  - `/chat/spinoza` → Réponse mock + RAG (3 passages)
- **RAG Actif**:
  - Corpus Spinoza 18k (Éthique II-IV)
  - Glossaire 12 concepts
  - Score relevance sur concepts extraits

### 3. HF Space Qwen 14B - RUNNING
- **URL**: https://fjdaz-bergsonandfriends.hf.space
- **Modèle**: Qwen 2.5 14B + LoRA Spinoza
- **GPU**: A10G-small (24GB VRAM)
- **Status**: ✅ Running (redémarré ce soir)
- **API Gradio**: `//chat_function` disponible
- **Coût**: ~$1/h

---

## ⚠️ CE QUI NE FONCTIONNE PAS

### 1. Intégration HF Space → Railway - BLOQUÉ
**Problème**: Railway ne peut pas déployer avec `gradio-client`

**Causes**:
- GitHub erreurs 500 persistantes (infrastructure GitHub instable)
- Railway mise/pyenv ne peut pas accéder à GitHub pour installer Python
- `runtime.txt` (python-3.11.9) échoue systématiquement

**Fichiers créés mais non déployés**:
- `snb_api_hf.py` (code prêt, non déployé)
- `requirements.txt` avec `gradio-client>=0.7.0`

**Logs Railway**:
```
✖ Failed to run mise command 'python@3.11.9'
mise ERROR error sending request for url (https://github.com/pyenv/pyenv.git)
```

### 2. Netlify Deployment - CRASH
**Problème**: GitHub instable → Netlify ne peut pas pull le repo

**Fichiers créés**:
- `netlify/functions/spinoza_hf.js` (fonction bridge HF Space)
- `netlify.toml` (config)

**Status**: Push réussi vers GitHub, mais Netlify crash au pull

---

## 🗂️ STRUCTURE ACTUELLE (Post-session)

### Fichiers Production (À GARDER)

```
/index_spinoza.html          ← Frontend actif (fjdaz.com)
/package.json                ← Deps Node.js (@gradio/client)
/netlify.toml                ← Config Netlify
/netlify/functions/
  └─ spinoza_hf.js           ← Function HF Space (non déployé)

/snb_api_mock.py             ← Backend Railway ACTIF
/snb_api_hf.py               ← Backend HF Space (non déployé)
/rag_system.py               ← RAG Python
/requirements.txt            ← Deps Python

/data/RAG/
  ├─ Corpus Spinoza 18k.md   ← Source RAG
  └─ Glossaire Spinoza.md

/docs/                       ← Documentation complète
  ├─ notes/
  ├─ tutos/
  ├─ references/
  └─ logs/
```

### Fichiers Obsolètes (Confirmé par session)

**Doublons majeurs** (rapport Cursor correct):
- `/bergson-and-friends/` (6.3M) → Ancien frontend
- `/bergsonAndFriends/` (2.1M) → À garder SI backend HF, sinon obsolète
- `/static/static/` → Doublon imbriqué

**Archives**:
- `/spinoza_NB_archive/`
- `/spinoza_NB_backup_mirror/`
- `/spinoza_NB_fastapi/`
- `/RAG/` (racine, fichiers .bak uniquement)

**Fichiers test session**:
- `app_local.js`
- `index_local.html` (version test localhost)
- `index_netlify.html` (tentative adaptation Netlify)
- `railway_deploy.log`, `railway_deploy_hf.log`

**Config obsolète**:
- `Procfile` → Railway (backend non utilisé en prod)
- `runtime.txt` → Supprimé (causait erreurs)
- `requirements_mock.txt`

---

## 🎯 RECOMMANDATIONS

### Option A: Garder Mock + RAG (Stable)
**Architecture actuelle qui fonctionne**:
```
Frontend (fjdaz.com)
    ↓
Railway (snb_api_mock.py)
    ↓ RAG lookup
Mock responses + RAG
```

**Avantages**:
- ✅ Stable, déployé, fonctionnel
- ✅ Gratuit (Railway tier free)
- ✅ RAG actif (3 passages pertinents)
- ✅ Réponses cohérentes (mocks bien écrits)

**Inconvénients**:
- ❌ Pas d'IA générative (réponses pré-écrites)
- ❌ Limité à ~10 réponses différentes

### Option B: Attendre stabilité GitHub + déployer HF Space
**Quand GitHub sera stable** (1-2 jours ?):

1. **Railway re-déploie** `snb_api_hf.py`
   ```
   Frontend → Railway → HF Space (Qwen 14B)
   ```

2. **OU Netlify Function**
   ```
   Frontend → Netlify Function → HF Space (Qwen 14B)
   ```

**Avantage**: Vraies réponses IA de Qwen 14B + LoRA Spinoza

**Inconvénient**: Coût HF Space ~$1/h

### Option C: Nettoyage puis déploiement
**Plan** (après stabilité GitHub):

1. **Nettoyer repo** (plan Cursor):
   - Supprimer `/bergson-and-friends/` (6.3M)
   - Supprimer archives Spinoza
   - Fix submodules Git

2. **Re-tester Netlify** avec repo propre

3. **Déployer HF Space bridge**

---

## 📋 ACTIONS IMMÉDIATES

### Ce soir (FAIT)
- ✅ Frontend Spinoza en production (fjdaz.com)
- ✅ Backend Railway Mock + RAG stable
- ✅ HF Space Qwen 14B running
- ✅ Code HF Space bridge prêt (non déployé)
- ✅ Push vers GitHub (stable maintenant)

### Demain (quand GitHub stable)
- [ ] Vérifier si Netlify peut pull le repo
- [ ] Tester déploiement Netlify Function
- [ ] OU retry Railway avec `snb_api_hf.py`

### Semaine prochaine (si besoin)
- [ ] Nettoyage repo (plan Cursor)
- [ ] Optimiser `netlify.toml` (publish directory)
- [ ] Tests complets Frontend → HF Space

---

## 💰 COÛTS ACTUELS

**Production actuelle (Mock + RAG)**:
- Railway: $0 (tier free)
- HF Space: **$1/h** (~$720/mois si 24/7)
- **Total**: $0 si Space en pause

**Recommandation**: Pause le Space HF quand pas utilisé

---

## 🔍 DIAGNOSTIC INFRASTRUCTURE

### GitHub
- ⚠️ **Erreurs 500 intermittentes** (18h-23h ce soir)
- Impact: Push échoue, Netlify crash, Railway mise fail
- **Cause**: Infrastructure GitHub (hors contrôle)

### Railway
- ✅ **Mock backend fonctionne**
- ❌ **Build Python avec gradio-client échoue** (besoin GitHub)
- Solution temporaire: Retrait `runtime.txt` (fait)

### Netlify
- ⚠️ **Crash au pull GitHub**
- Code prêt: `netlify/functions/spinoza_hf.js`
- Attente: Stabilité GitHub

### HF Space
- ✅ **Opérationnel** (A10G running)
- API Gradio testée et fonctionnelle
- Prêt à être appelé

---

## 📊 VERDICT SESSION

### Réussite
1. ✅ **Système fonctionnel en prod** : Frontend + Mock + RAG
2. ✅ **Code HF Space prêt** : `snb_api_hf.py` + `spinoza_hf.js`
3. ✅ **HF Space actif** : Qwen 14B running
4. ✅ **Push GitHub réussi** (après multiples tentatives)

### Blocages Externes
1. ⚠️ **GitHub infrastructure** : Erreurs 500 (hors contrôle)
2. ⚠️ **Railway/Netlify dépendants** de GitHub

### Décision Recommandée
**Garder Mock + RAG en production** jusqu'à stabilité GitHub, puis déployer HF Space bridge.

Le système actuel est **déjà utile et fonctionnel** avec RAG actif.

---

**Dernière mise à jour**: 18 nov 2025, 23h05
**Statut global**: ✅ Prod Mock OK | ⏳ HF Space bridge en attente GitHub
