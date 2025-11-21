# 📋 Résumé Complet des Issues Rencontrées - Bergson and Friends

**Date de synthèse :** Novembre 2025  
**Projet :** Bergson and Friends - Système RAG + SNB (Spinoza Niveau B)

---

## 🎯 Architecture Initiale et Évolution

### Architecture Cible
```
Frontend (fjdaz.com/bergsonandfriends)
    ↓
Netlify Functions (philosopher_rag.js)
    ↓
Hugging Face Space (SNB Backend)
    ↓
Modèle Qwen 14B + LoRA Spinoza
```

### Pourquoi un Space Orchestral ?

**Option initiale :** `SNB_orchestrator` - Un Space HF qui fait proxy vers plusieurs Spaces
- **Idée :** Centraliser les appels pour 3 philosophes (Spinoza, Bergson, Kant)
- **Avantage théorique :** Un seul point d'entrée, gestion simplifiée
- **Problème rencontré :** Complexité inutile, latence supplémentaire, coût multiplié
- **Décision :** Abandonné au profit d'un Space unique avec injection de style dans le prompt

**Solution finale :** Space `bergsonAndFriends` unique
- Un seul Space avec A10G (24GB VRAM)
- Injection du style du philosophe dans le message (pas de system prompt séparé)
- RAG géré côté Netlify Functions (pas dans le Space)

---

## 💰 Problèmes de Coût

### 1. Hugging Face Spaces - Coûts Variables

**Problème :**
- **ZeroGPU (gratuit)** : Insuffisant pour Qwen 14B 8-bit (~14GB VRAM)
- **T4 Small ($0.40/h)** : VRAM insuffisante, modèle dispatché sur CPU/disk
- **A10G Small ($1.00/h)** : Fonctionne mais coûteux pour usage continu

**Impact :**
- Space `spinoza_NB` (T4) ne démarre plus → Runtime error
- Migration vers `bergsonAndFriends` (A10G) nécessaire
- Risque de suspension si impayés

**Solution :**
- Utiliser A10G uniquement pour démos ponctuelles
- Plan de repli RunPod/Vast.ai préparé (pay-per-use)

### 2. Coûts RunPod (Solution de Repli)

**Estimation pour démo 3h :**
- **A10G :** $1.00/h × 3h = **$3.00** (+ chargement ~$0.20) = **~$3.20**
- **T4 :** $0.30/h × 3h = **$0.90** (+ chargement ~$0.05) = **~$0.95**

**Avantage :** Pay-per-use, arrêt immédiat après usage

---

## 📤 Problèmes d'Upload

### 1. Upload `app.js` sur fjdaz.com

**Problème :**
- Fichier `app.js` doit être sur `fjdaz.com/bergson/statics/app.js`
- Version serveur obsolète (20 oct) vs version locale (17 nov)
- Erreur 404 si fichier manquant ou mauvais chemin

**Solutions tentées :**
- ✅ Correction du chemin dans `index.html` : `https://fjdaz.com/bergson/statics/app.js`
- ⚠️ Upload manuel requis (FTP/SCP/SFTP)
- ⚠️ Problème de cache navigateur (hard refresh nécessaire)

**Fichiers concernés :**
- `static/app.js` (local)
- `fjdaz.com/bergson/statics/app.js` (serveur)
- `index.html` (chemin corrigé)

### 2. Upload `index.html` sur fjdaz.com

**Problème :**
- `index.html` sur serveur utilise ancien chemin `/static/app.js`
- Doit pointer vers `https://fjdaz.com/bergson/statics/app.js`

**Solution :**
- ✅ Correction locale effectuée
- ⚠️ Upload manuel requis

### 3. Problèmes FTP/SFTP

**Difficultés rencontrées :**
- Accès SSH/FTP non documenté
- Chemins serveur à déterminer
- Permissions fichiers à vérifier
- Uploads incomplets (fichier tronqué à 196 bytes au lieu de 13KB)

**Solutions :**
- Guides créés : `GUIDE_UPLOAD_APP_JS.md`, `GUIDE_UPLOAD_INDEX_HTML.md`
- Vérification après upload : `curl` pour vérifier taille et contenu

---

## 🔧 Problèmes fjdaz.com

### 1. Configuration API_BASE_URL

**Problème :**
- `app.js` doit détecter si on est sur `fjdaz.com` ou Netlify
- Si `fjdaz.com` → utiliser URL complète Netlify
- Si Netlify → utiliser chemin relatif

**Solution :**
```javascript
const API_BASE_URL = window.location.hostname === 'fjdaz.com' 
    ? 'https://chimerical-kashata-65179e.netlify.app/.netlify/functions'
    : '/.netlify/functions';
```

### 2. CORS (Cross-Origin Resource Sharing)

**Problème :**
- Appels depuis `fjdaz.com` vers `chimerical-kashata-65179e.netlify.app` bloqués par CORS

**Solution :**
- Headers CORS ajoutés dans `philosopher_rag.js` :
  ```javascript
  'Access-Control-Allow-Origin': '*'
  'Access-Control-Allow-Headers': 'Content-Type'
  'Access-Control-Allow-Methods': 'POST, OPTIONS'
  ```

### 3. Cache Navigateur

**Problème :**
- Ancienne version de `app.js` en cache
- Modifications non visibles immédiatement

**Solution :**
- Hard refresh : `Cmd+Shift+R` (Mac) ou `Ctrl+Shift+R` (Windows)
- Vérification avec `curl` pour voir version serveur

---

## 🌐 Problèmes Netlify / Chimerical

### 1. Timeout Netlify Functions

**Problème :**
- **Plan Free :** Timeout de 10s
- **Space HF :** Cold start de 30-60s
- Résultat : Timeout avant réponse du Space

**Solutions :**
- Garder le Space actif (éviter cold start)
- Passer au plan Pro Netlify (26s timeout) - coût supplémentaire
- Utiliser RunPod avec latence plus faible

### 2. Variable USE_MOCK

**Problème :**
- Si `USE_MOCK=true` dans Netlify → toujours réponse mock
- Pas d'appel réel au Space HF

**Solution :**
- Vérifier variables Netlify : `USE_MOCK` doit être `false` ou non défini
- Guide : `FIX_MOCK_NETLIFY.md`

### 3. Configuration SNB_BACKEND_URL

**Problème :**
- URL du Space HF doit être configurable
- Par défaut : `https://fjdaz-bergsonandfriends.hf.space`
- Repli possible vers RunPod/Vast.ai

**Solution :**
- Variable d'environnement Netlify : `SNB_BACKEND_URL`
- Code : `process.env.SNB_BACKEND_URL || "https://fjdaz-bergsonandfriends.hf.space"`

### 4. @gradio/client dans Netlify Functions

**Problème initial :**
- `@gradio/client` nécessite environnement navigateur
- Ne fonctionne pas dans Netlify Functions (Node.js)

**Solution :**
- Utilisation de `fetch` avec API Gradio HTTP directe
- Guide : `FIX_GRADIO_CLIENT.md`

---

## 🤗 Problèmes Hugging Face Spaces

### 1. Space `spinoza_NB` ne démarre plus

**Problème :**
- **Hardware :** T4 (16GB VRAM)
- **Modèle :** Qwen 14B 8-bit (~14GB VRAM)
- **Erreur :** Runtime error - modèles dispatchés sur CPU/disk
- **Cause :** VRAM insuffisante

**Solution :**
- Migration vers Space `bergsonAndFriends` avec A10G (24GB VRAM)
- ✅ Fonctionne correctement

### 2. Cold Start HF Spaces

**Problème :**
- Space inactif → démarrage 30-60s
- Netlify timeout 10s → échec

**Solution :**
- Garder le Space actif (coût continu)
- Ou accepter latence initiale (première requête lente)

### 3. Suspension pour Impayés

**Risque :**
- HF peut suspendre le Space si facture impayée
- Impact : Démo impossible

**Solution de repli :**
- RunPod/Vast.ai prêt en 25-30 minutes
- Guide : `REPLI_RUNPOD.md`, `REPLI_BACKEND.md`

### 4. API Gradio

**Problème :**
- API Gradio non activée par défaut
- Endpoint `/chat_function` non disponible

**Solution :**
- Activation dans `app.py` :
  ```python
  demo.queue()
  demo.launch(show_api=True)
  ```
- Commit `e867af8` sur Space `bergsonAndFriends`

---

## 🚀 Spaces Encore en Place

### 1. Space `bergsonAndFriends` ✅ ACTIF

**URL :** `https://fjdaz-bergsonandfriends.hf.space`  
**Hardware :** A10G-small (24GB VRAM, 46GB RAM)  
**Status :** ✅ Running  
**API :** ✅ Activée (`/chat_function`)  
**Version :** V2 fonctionnelle (Spinoza seul, sans RAG côté Space)  
**Coût :** ~$1.00/h

**Utilisation :**
- Backend principal actuel
- Appelé depuis Netlify Functions
- Injection style philosophe dans le message

### 2. Space `spinoza_NB` ⚠️ INACTIF

**URL :** `https://fjdaz-spinoza-nb.hf.space`  
**Hardware :** T4 (16GB VRAM)  
**Status :** ❌ Ne démarre plus (VRAM insuffisante)  
**Problème :** Qwen 14B 8-bit ne tient pas dans 16GB VRAM

**Historique :**
- Version fonctionnelle avant (commit `fda24ba`)
- Abandonné au profit de `bergsonAndFriends`

### 3. Space `SNB_orchestrator` ❓ STATUT INCONNU

**Objectif initial :** Proxy vers plusieurs Spaces  
**Status :** Probablement abandonné (complexité inutile)  
**Code :** Présent dans `SNB_orchestrator/` mais non utilisé

---

## 🔄 Solutions de Repli

### Option 1 : RunPod ⭐ RECOMMANDÉ

**Avantages :**
- Pay-per-use (~$0.30-1.00/h)
- Setup rapide (25-30 min)
- Contrôle total
- Compatible Docker (même stack que HF Spaces)

**Coût pour démo 3h :**
- A10G : ~$3.20
- T4 : ~$0.95

**Guide :** `REPLI_RUNPOD.md`

**Plan d'urgence (si HF suspend) :**
1. Créer compte RunPod (5 min)
2. Déployer template Docker (10 min)
3. Attendre chargement modèle (10 min)
4. Tester API (2 min)
5. Mettre à jour Netlify (2 min)
6. Redéployer Netlify (2 min)
**Total : 25-30 minutes**

### Option 2 : Vast.ai

**Similaire à RunPod :**
- Pay-per-use
- GPU à la demande
- Setup rapide

### Option 3 : Replicate

**Avantages :**
- API REST simple
- Gestion automatique infrastructure

**Inconvénients :**
- Setup initial long (publier modèle)
- Coût par requête (~$0.002-0.01)

### Option 4 : Serveur GPU Dédié (OVH, Scaleway, Hetzner)

**Avantages :**
- Contrôle total
- Performance garantie
- Moins cher si utilisation intensive

**Inconvénients :**
- Setup complexe
- Engagement mensuel
- Coût : ~$50-100/mois

**Note :** OVH Perso non adapté (pas de processus long, pas de SSH root)

---

## 📊 Récapitulatif des Problèmes par Catégorie

### 🔴 Critiques (Bloquants)

1. **Space `spinoza_NB` ne démarre plus** → Migration vers `bergsonAndFriends`
2. **Timeout Netlify 10s vs Cold Start HF 30-60s** → Garder Space actif ou repli
3. **Upload `app.js` sur fjdaz.com** → Action manuelle requise

### 🟡 Importants (Impact UX)

1. **Cache navigateur** → Hard refresh nécessaire
2. **CORS** → Headers configurés mais à vérifier
3. **USE_MOCK activé** → Vérifier variables Netlify

### 🟢 Mineurs (Documentation/Process)

1. **Chemins serveur non documentés** → Guides créés
2. **FTP/SFTP accès** → Guides créés
3. **Versioning fichiers** → Vérification avec `curl`

---

## ✅ Solutions Mises en Place

### Documentation Créée

1. **`REPLI_RUNPOD.md`** - Guide complet repli RunPod (30 min)
2. **`REPLI_BACKEND.md`** - Stratégie générale de repli
3. **`CONTEXTE_SESSION_17NOV.md`** - Résumé session 17 novembre
4. **`GUIDE_UPLOAD_APP_JS.md`** - Guide upload app.js
5. **`GUIDE_UPLOAD_INDEX_HTML.md`** - Guide upload index.html
6. **`FIX_MOCK_NETLIFY.md`** - Désactiver mock
7. **`FIX_GRADIO_CLIENT.md`** - Fix @gradio/client
8. **`DEBUG_FJDAZ.md`** - Debug fjdaz.com
9. **`FIX_API_URL.md`** - Configuration API URL

### Code Modifié

1. **`src/prompts.js`** - URL configurable, logs détaillés
2. **`netlify/functions/philosopher_rag.js`** - Headers CORS, logs
3. **`static/app.js`** - Détection fjdaz.com, API_BASE_URL
4. **`index.html`** - Chemin app.js corrigé

### Spaces HF

1. **`bergsonAndFriends`** - A10G, API activée, fonctionnel
2. **`spinoza_NB`** - T4, inactif (VRAM insuffisante)

---

## 🎯 État Actuel (Novembre 2025)

### ✅ Fonctionnel

- Space `bergsonAndFriends` tourne avec A10G
- API Gradio activée (`/chat_function`)
- Code Netlify Functions prêt
- RAG système opérationnel
- Guides de repli préparés

### ⚠️ En Attente

- Upload `app.js` sur fjdaz.com (version locale plus récente)
- Upload `index.html` corrigé sur fjdaz.com
- Vérification variables Netlify (`USE_MOCK`, `SNB_BACKEND_URL`)
- Test flux complet depuis fjdaz.com

### 📋 Prochaines Étapes

1. Uploader fichiers sur fjdaz.com
2. Vérifier variables Netlify
3. Tester flux complet
4. Préparer repli RunPod (optionnel, préventif)

---

## 🔗 URLs Importantes

- **Space HF actif :** https://fjdaz-bergsonandfriends.hf.space
- **API Info :** https://fjdaz-bergsonandfriends.hf.space/gradio_api/info
- **Frontend :** https://fjdaz.com/bergsonandfriends
- **Netlify :** https://chimerical-kashata-65179e.netlify.app
- **Netlify Dashboard :** https://app.netlify.com → Site → Functions → Logs

---

**Dernière mise à jour :** Novembre 2025  
**Status global :** 🟡 Fonctionnel mais optimisations nécessaires

