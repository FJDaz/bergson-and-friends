# 📋 Résumé de Contexte - Session 17 Novembre 2025

## 🎯 Objectif Principal
Configurer un système fonctionnel pour le 26 novembre : **Bergson and Friends** avec RAG + SNB (Spinoza Niveau B) pour 3 philosophes (Spinoza, Bergson, Kant).

---

## 🏗️ Architecture Actuelle

### Flux Complet
```
fjdaz.com/bergsonandfriends (index.html)
    ↓
Netlify Functions (philosopher_rag.js)
    ↓
Space HF: bergsonAndFriends (A10G) - https://fjdaz-bergsonandfriends.hf.space
```

**Fichiers clés :**
- `index.html` → Sur fjdaz.com (hébergement perso)
- `static/app.js` → Doit être uploadé sur fjdaz.com/bergson/statics/app.js
- `netlify/functions/philosopher_rag.js` → Netlify Functions
- `src/prompts.js` → Appelle le Space HF via @gradio/client
- `src/rag_system.js` → RAG (concepts + passages)

---

## ✅ Ce Qui Fonctionne

1. **Space `bergsonAndFriends`** (A10G-small, 24GB VRAM)
   - ✅ Tourne sur A10G
   - ✅ Version V2 fonctionnelle (Spinoza seul, sans RAG côté Space)
   - ✅ API activée : `show_api=True`, `queue()`, `api_name="/chat_function"`
   - ✅ Endpoint disponible : `//chat_function` (double slash)
   - ✅ URL : https://fjdaz-bergsonandfriends.hf.space

2. **Code Netlify**
   - ✅ `philosopher_rag.js` → Gère RAG + appelle SNB
   - ✅ `prompts.js` → Utilise `@gradio/client` (version qui fonctionnait)
   - ✅ `app.js` → Appelle `/.netlify/functions/philosopher_rag` correctement
   - ✅ Dépendance ajoutée : `@gradio/client` dans `package.json`

3. **Backup Complet**
   - ✅ Toutes les versions de `spinoza_NB` sauvegardées localement
   - ✅ Backup mirror Git : `spinoza_NB_backup_mirror/`
   - ✅ Document : `SPINOZA_NB_VERSIONS.md` avec toutes les versions

---

## ⚠️ Problèmes Actuels

### Problème 1 : `app.js` non accessible sur fjdaz.com
- **Symptôme** : "Failed to load data for app.js" sur fjdaz.com
- **Cause** : `app.js` doit être uploadé sur `fjdaz.com/bergson/statics/app.js`
- **Fichier local** : `/Users/francois-jeandazin/bergsonAndFriends/static/app.js`
- **Chemin dans index.html** : `https://fjdaz.com/bergson/statics/app.js` ✅ (corrigé)
- **Action requise** : Uploader `static/app.js` → `fjdaz.com/bergson/statics/app.js`

### Problème 2 : Fallback mock s'affiche immédiatement
- **Symptôme** : Réponse mock (pas de vrai appel au Space HF)
- **Cause probable** : `@gradio/client` ne peut pas se connecter au Space ou timeout
- **Solution testée** : Version restaurée avec `@gradio/client` (commande `72fa6ba`)
- **À vérifier** : Logs Netlify pour voir l'erreur exacte

### Problème 3 : Space `spinoza_NB` ne démarre plus
- **Symptôme** : Runtime error - modèles dispatchés sur CPU/disk malgré T4
- **Cause** : Qwen 14B 8-bit (~14GB) ne tient pas dans la VRAM disponible
- **Solutions proposées** :
  - ✅ Space `bergsonAndFriends` avec A10G (24GB) → fonctionne
  - ⏸️ Version 4-bit proposée (non déployée)
  - 📋 Guide RunPod créé pour repli : `REPLI_RUNPOD.md`

---

## 📁 Fichiers Modifiés (Session)

### Commits Poussés
1. **`72fa6ba`** - Restore working config: Use @gradio/client instead of manual HTTP/SSE
   - `src/prompts.js` → Version avec `@gradio/client` (qui fonctionnait)
   - `package.json` → Ajout dépendance `@gradio/client`

2. **`51434a4`** - Add detailed logging for SNB Space debugging
   - `src/prompts.js` → Logs détaillés
   - `netlify/functions/philosopher_rag.js` → Logs détaillés

3. **`0e62df8`** - Rebranch Netlify -> bergsonAndFriends Space (A10G) + Fix app.js calls
   - `static/app.js` → Appelle `/.netlify/functions/philosopher_rag`
   - `src/prompts.js` → URL vers `bergsonAndFriends`

### Modifications Non Committées
- `index.html` → Chemin `app.js` corrigé vers `https://fjdaz.com/bergson/statics/app.js`

### Space `bergsonAndFriends` Modifié
- Commit `e867af8` - Enable API: add show_api=True, queue() and api_name=/chat_function
- API activée et fonctionnelle

---

## 🔧 Configuration Actuelle

### Space HF `bergsonAndFriends`
- **Hardware** : A10G-small (24GB VRAM, 46GB RAM)
- **Status** : ✅ Running
- **API** : ✅ Exposée (`//chat_function`)
- **URL** : https://fjdaz-bergsonandfriends.hf.space
- **Code** : Version V2 fonctionnelle (Spinoza seul, sans RAG)

### Netlify Functions
- **Fonction** : `philosopher_rag.js`
- **Timeout** : 10s (plan free) ⚠️ Limite pour cold start
- **Variables** : `SNB_BACKEND_URL` (non défini = `bergsonAndFriends`)
- **USE_MOCK** : À vérifier (ne doit pas être `true`)

### Frontend (fjdaz.com)
- **index.html** : Sur fjdaz.com/bergsonandfriends
- **app.js** : Doit être sur `fjdaz.com/bergson/statics/app.js` ⚠️ À uploader
- **CSS/Images** : ✅ Déjà sur `fjdaz.com/bergson/statics/`

---

## 📝 Actions Requises (TODO)

### Urgent (pour que ça fonctionne)
1. **Upload `app.js` sur fjdaz.com**
   - Fichier : `/Users/francois-jeandazin/bergsonAndFriends/static/app.js`
   - Destination : `fjdaz.com/bergson/statics/app.js`
   - Vérifier : Accès HTTP direct à `https://fjdaz.com/bergson/statics/app.js`

2. **Push `index.html` corrigé**
   - Chemin `app.js` déjà corrigé
   - À committer et pousser

3. **Vérifier logs Netlify**
   - Dashboard Netlify → Functions → `philosopher_rag` → Logs
   - Chercher : `[SNB Error]`, `[RAG] Erreur SNB`
   - Vérifier : `USE_MOCK` n'est pas activé

### Pour le 26 novembre
4. **Tester le flux complet**
   - Depuis fjdaz.com/bergsonandfriends
   - Tester avec Spinoza (3 philosophes si possible)
   - Vérifier que le Space répond (pas de mock)

5. **Plan de repli RunPod** (si HF suspend)
   - Guide créé : `REPLI_RUNPOD.md`
   - Template RunPod à créer (optionnel préventif)
   - Temps de repli estimé : 25-30 minutes

---

## 🔍 Points de Debug

### Si fallback mock persiste
1. Vérifier `USE_MOCK` dans Netlify (doit être `false` ou non défini)
2. Consulter logs Netlify pour erreur exacte
3. Tester `@gradio/client` : peut nécessiter une version spécifique
4. Vérifier que le Space `bergsonAndFriends` répond bien :
   ```bash
   curl https://fjdaz-bergsonandfriends.hf.space/gradio_api/info
   ```

### Si `app.js` ne charge pas
1. Vérifier upload sur fjdaz.com : `https://fjdaz.com/bergson/statics/app.js`
2. Vérifier permissions du fichier (readable)
3. Vérifier cache navigateur (hard refresh : Cmd+Shift+R)

---

## 📚 Fichiers de Documentation Créés

1. **`REPLI_RUNPOD.md`** - Guide complet pour repli sur RunPod (30 min)
2. **`REPLI_BACKEND.md`** - Stratégie de repli backend (général)
3. **`SPINOZA_NB_VERSIONS.md`** - Archive toutes versions spinoza_NB
4. **`CONTEXTE_SESSION_17NOV.md`** - Ce document (résumé session)

---

## 🔄 Configuration Fonctionnelle (Version qui Marchait)

### Code `prompts.js` qui fonctionnait
```javascript
const { Client } = await import("@gradio/client");
const client = await Client.connect(SPACE_URL);
const result = await client.predict("/chat_function", {
    message: enrichedMessage,
    history: []
});
```

### Space qui fonctionnait
- **URL** : `https://fjdaz-spinoza-nb.hf.space` (ancien)
- **Version** : V2 avec `/chat_function` (commit `fda24ba`)
- **Status** : Non utilisé actuellement (on utilise `bergsonAndFriends`)

---

## 🎯 État Final de la Session

### ✅ Fait
- Space `bergsonAndFriends` tourne avec API activée
- Code restauré avec `@gradio/client` (version qui fonctionnait)
- `app.js` corrigé pour appeler `philosopher_rag`
- Backup complet de toutes les versions
- Guide RunPod créé

### ⚠️ En Attente
- Upload `app.js` sur fjdaz.com
- Push `index.html` corrigé
- Test du flux complet
- Vérification des logs Netlify

### 📋 Prochaines Étapes
1. Uploader `static/app.js` → `fjdaz.com/bergson/statics/app.js`
2. Committer et pusher `index.html` corrigé
3. Tester depuis fjdaz.com/bergsonandfriends
4. Consulter logs Netlify si problème persiste

---

## 🔗 URLs Importantes

- **Space HF** : https://fjdaz-bergsonandfriends.hf.space
- **API Info** : https://fjdaz-bergsonandfriends.hf.space/gradio_api/info
- **Frontend** : https://fjdaz.com/bergsonandfriends
- **Netlify** : Dashboard Netlify → Site → Functions → Logs

---

**Dernière modification** : 17 novembre 2025 - 15:45
**Status** : Code prêt, en attente d'upload `app.js` et test

---

## 📅 Mises à Jour - 18 Novembre 2025

### ✅ Actions Complétées

#### 1. Nettoyage Complet du Dépôt ✅

**Problème identifié :** Structure confuse avec doublons, archives obsolètes, submodules mal configurés

**Actions réalisées :**
- ✅ **Suppression doublons majeurs :**
  - `bergson-and-friends/` (6.3M) → Supprimé (doublon frontend)
  - `static/static/` → Supprimé (doublon imbriqué)
  - `RAG/` (racine) → Supprimé (fichiers .bak uniquement)
  - `bergson-and-friends/RAG/` → Supprimé (doublon)

- ✅ **Suppression archives obsolètes :**
  - `spinoza_NB_archive/` → Supprimé (archivé dans docs)
  - `spinoza_NB_backup_mirror/` → Supprimé (backup Git inutile, ~50MB)
  - `spinoza_NB_fastapi/` → Supprimé (version non utilisée)

- ✅ **Nettoyage fichiers de test :**
  - `app_local.js`, `index_local.html`, `index_netlify.html` → Supprimés
  - `test-bergson*.html` → Supprimés
  - Logs racine → Déplacés vers `docs/logs/`

- ✅ **Réorganisation documentation :**
  - Fichiers MD racine → Déplacés vers `docs/notes/` ou `docs/tutos/`
  - `CONTEXTE_SESSION_17NOV.md` → Déplacé vers `docs/notes/`

**Gain estimé :** ~50-60% de réduction de taille, déploiement Netlify plus rapide

#### 2. Correction Submodules Git ✅

**Problème :** Dossiers avec `.git/` mais pas dans `.gitmodules` → Erreurs Git

**Actions réalisées :**
- ✅ Suppression `.git/` dans :
  - `SNB_orchestrator/` → Converti en dossier normal
  - `bergsonAndFriends/` → Converti en dossier normal
  - `spinoza_NB/` → Converti en dossier normal

- ✅ Retrait de l'index Git :
  ```bash
  git rm --cached SNB_orchestrator/
  git rm --cached bergsonAndFriends/
  git rm --cached spinoza_NB/
  ```

- ✅ Réajout comme dossiers normaux :
  ```bash
  git add SNB_orchestrator/ bergsonAndFriends/ spinoza_NB/
  ```

**Résultat :** Plus d'erreurs Git, structure propre

#### 3. Renommage `bergsonAndFriends/` → `bergsonAndFriends_HF/` ✅

**Raison :** Clarifier que ce dossier contient le code source du Space HF

**Action réalisée :**
- ✅ Renommage avec `git mv` (préserve historique Git)
- ✅ 53 fichiers renommés
- ✅ Commit et push réussis

**Statut :** Dossier renommé et pushé sur GitHub

#### 4. Documentation et Organisation ✅

**Nouveaux fichiers créés :**
- ✅ `docs/notes/RAPPORT_ETAT_PROJET.md` - Audit complet structure dépôt
- ✅ `docs/notes/DOUBLONS_RESTANTS.md` - Rapport doublons restants
- ✅ `docs/notes/UTILISATION_BERGSONANDFRIENDS.md` - Explication usage dossier
- ✅ `docs/notes/FIX_SUBMODULES.md` - Guide correction submodules
- ✅ `docs/notes/OPTIONS_ELIMINATION_BERGSONANDFRIENDS_HF.md` - Options élimination
- ✅ `docs/notes/ANALYSE_GPU_OPTIONS.md` - Analyse options GPU HF Spaces
- ✅ `docs/notes/CONFIG_MIN_QWEN_14B.md` - Configuration minimale Qwen 14B
- ✅ `docs/notes/EXPLICATION_RAILWAY_NETLIFY.md` - Explication services (noob)
- ✅ `docs/notes/TERMES_SERVICES_CLOUD.md` - Termes techniques services cloud
- ✅ `docs/notes/ENDPOINTS_GRADIO_BERGSONANDFRIENDS.txt` - Endpoints API Gradio

**Mise à jour documentation existante :**
- ✅ `docs/references/methode-meta-skills.md` - Ajout section `logs/` et règle `garbage/`
- ✅ `docs/README.md` - Ajout section `docs/logs/`
- ✅ `.gitignore` - Règle absolue : `garbage/` ne doit JAMAIS être pushé

#### 5. Structure Dépôt Finale ✅

**Dossiers actifs :**
- ✅ `/index_spinoza.html` → Frontend actif (Spinoza, Railway backend)
- ✅ `/netlify/functions/` → Netlify Functions (actif)
- ✅ `/bergsonAndFriends_HF/` → Code source Space HF (renommé)
- ✅ `/data/RAG/` → Corpus RAG source (version propre)
- ✅ `/docs/` → Documentation complète
- ✅ `/docs/logs/` → Logs (Railway, etc.)

**Fichiers supprimés/déplacés :**
- ❌ `bergson-and-friends/` → Supprimé
- ❌ Archives Spinoza → Supprimées
- ❌ Doublons `static/`, `netlify/` → Supprimés
- ❌ Fichiers de test → Supprimés

#### 6. Suppression Dossiers Obsolètes ✅

**Dossiers supprimés :**
- ✅ `spinoza_NB/` (104K) → Ancien Space HF (T4 insuffisant, ne démarre plus)
  - Remplacé par `bergsonAndFriends` (A10G, fonctionnel)
  - Contenait plusieurs versions obsolètes d'app.py
  - 20 fichiers supprimés

- ✅ `SNB_orchestrator/` (32K) → Orchestrateur obsolète
  - Appelait `FJDaz/spinoza_NB` (Space obsolète)
  - Non utilisé dans le code actif
  - Remplacé par appels directs au Space `bergsonAndFriends`

**Résultat :** ~136K supprimés, structure plus claire

#### 7. Commits Réalisés (18 Nov)

**Commits principaux :**
1. `90c48e1` - Remove: Delete obsolete spinoza_NB and SNB_orchestrator
2. `1d4f3eb` - Rename: bergsonAndFriends -> bergsonAndFriends_HF
3. `e2ec9d4` - Add: documentation for submodules fix and duplicates analysis
4. `107b747` - Fix: Convert submodules to normal directories
5. `77852ec` - Remove: delete moved MD files and test files from root
6. `0b96d24` - Reorganize: move MD files to docs/, remove test files
7. `5b18265` - Clean: remove duplicates, add docs, update gitignore with garbage rule
8. `ad0f925` - Clean: move obsolete files to garbage/ + add final project status

**Statut Git :** ✅ Tous les changements pushés sur GitHub

---

## 📊 État Actuel du Projet (18 Nov 2025)

### ✅ Architecture Fonctionnelle

**Frontend :**
- ✅ `index_spinoza.html` → Interface Spinoza (responsive)
- ✅ Backend : Railway (`https://bergson-api-production.up.railway.app`)
- ✅ Styles : `https://fjdaz.com/bergson/statics/style.css`

**Backend :**
- ✅ **HF Space** : `bergsonAndFriends` (A10G, 24GB VRAM)
  - URL : `https://fjdaz-bergsonandfriends.hf.space`
  - API : `//chat_function`, `/lambda`, `/lambda_1`
  - Modèle : Qwen 2.5 14B + LoRA Spinoza

- ✅ **Railway** : Backend API (si utilisé)
  - URL : `https://bergson-api-production.up.railway.app`
  - ⚠️ Logs montrent erreurs mise/pyenv (à vérifier)

- ✅ **Netlify Functions** : Bridge HF Space
  - `philosopher_rag.js` → Function principale RAG
  - `spinoza.js` → Function Spinoza
  - `spinoza_hf.js` → Bridge HF Space

### 📁 Structure Dépôt (Nettoyée)

**Dossiers principaux :**
- `/index_spinoza.html` → Frontend actif
- `/netlify/functions/` → Netlify Functions
- `/bergsonAndFriends_HF/` → Code source Space HF (renommé)
- `/data/RAG/` → Corpus RAG source
- `/docs/` → Documentation complète
- `/docs/logs/` → Logs (Railway, etc.)
- `/garbage/` → Fichiers obsolètes (NE JAMAIS PUSH)

**Fichiers supprimés :**
- ❌ `bergson-and-friends/` (6.3M)
- ❌ Archives Spinoza (~50MB)
- ❌ Doublons `static/`, `netlify/`
- ❌ Fichiers de test

### ⚠️ Points d'Attention

1. **Railway Backend**
   - ⚠️ Logs montrent erreurs mise/pyenv
   - ⚠️ Statut à vérifier : `/health` endpoint

2. **Netlify Déploiement**
   - ⚠️ Crash récent (à investiguer)
   - ⚠️ Configuration `publish = "."` publie tout (à optimiser)

3. **HF Space**
   - ✅ Space actif
   - ⚠️ Coût : ~$1/h (A10G)
   - ⚠️ Risque suspension si impayés

---

## 📚 Documentation Créée (18 Nov)

### Rapports et Analyses
- `RAPPORT_ETAT_PROJET.md` - Audit complet structure dépôt
- `DOUBLONS_RESTANTS.md` - Rapport doublons restants
- `UTILISATION_BERGSONANDFRIENDS.md` - Explication usage dossier
- `FIX_SUBMODULES.md` - Guide correction submodules
- `OPTIONS_ELIMINATION_BERGSONANDFRIENDS_HF.md` - Options élimination
- `ANALYSE_GPU_OPTIONS.md` - Analyse options GPU HF Spaces
- `CONFIG_MIN_QWEN_14B.md` - Configuration minimale Qwen 14B

### Explications et Guides
- `EXPLICATION_RAILWAY_NETLIFY.md` - Explication services (noob)
- `TERMES_SERVICES_CLOUD.md` - Termes techniques services cloud
- `ENDPOINTS_GRADIO_BERGSONANDFRIENDS.txt` - Endpoints API Gradio

### Mise à Jour Documentation
- `methode-meta-skills.md` - Ajout section `logs/` et règle `garbage/`
- `docs/README.md` - Ajout section `docs/logs/`
- `.gitignore` - Règle absolue : `garbage/` ne doit JAMAIS être pushé

---

## 🎯 Prochaines Étapes

### Court Terme
1. ⏳ Vérifier statut Railway backend
2. ⏳ Investiguer crash Netlify
3. ⏳ Optimiser `netlify.toml` (publish directory)
4. ⏳ Tester déploiement Netlify après nettoyage

### Moyen Terme
1. ⏳ Confirmer URL frontend sur fjdaz.com
2. ⏳ Tester flux complet (frontend → Railway/Netlify → HF Space)
3. ⏳ Monitorer coûts HF Space (A10G ~$1/h)

---

---

## 🎯 Architecture Finale Simplifiée (19 Novembre 2025)

### Stack Finale

**Architecture ultra-simplifiée :**
```
Frontend (fjdaz.com)
    ↓
API REST HF Space (3_PHI)
    ↓
Qwen 14B + LoRA Spinoza NB + 3 Prompts Système
```

### Composants

#### Frontend
- **URL 3 Philosophes** : `fjdaz.com/3phi/`
  - `index.html` → Interface 3 philosophes (Bergson, Kant, Spinoza)
  - `app.js` → JavaScript connecté au Space 3_PHI
- **URL Spinoza Seul** : `fjdaz.com/bergson/`
  - `index_spinoza.html` → Interface Spinoza seul
  - Backend : Space HF `bergsonAndFriends` (Spinoza uniquement)
- **Assets** : CSS/Images depuis `https://fjdaz.com/bergson/statics/`

#### Backend

**Space HF `3_PHI` (3 Philosophes)** :
- **URL API** : `https://fjdaz-3-phi.hf.space`
- **Endpoints REST** :
  - `GET /health` → Vérification statut modèle
  - `GET /init/{philosopher}` → Question d'amorce (spinoza/bergson/kant)
  - `POST /chat` → Chat avec `{message, history, philosopher}`
- **Modèle** : Qwen 2.5 14B + LoRA Spinoza Niveau B
- **Prompts** : 3 prompts système (Spinoza, Bergson, Kant) injectés dans le message
- **GPU** : L4 (~18GB VRAM) ou A10G (24GB VRAM)
- **RAG** : ❌ Non géré dans le Space (pas de RAG dans `app.py`)

**Space HF `bergsonAndFriends` (Spinoza Seul)** :
- **URL API** : `https://fjdaz-bergsonandfriends.hf.space`
- **Modèle** : Qwen 2.5 14B + LoRA Spinoza Niveau B
- **GPU** : A10G (24GB VRAM)
- **Usage** : Frontend `fjdaz.com/bergson/` (Spinoza seul)

### Fonctionnalités

✅ **3 Philosophes fonctionnels** :
- Spinoza : Formules dialectiques ("MAIS ALORS"), causalité nécessaire
- Bergson : Métaphores temporelles, opposition durée vs temps spatial
- Kant : Distinctions (phénomène/noumène), examen critique

✅ **Détection contextuelle** : accord/confusion/résistance/neutre

✅ **Questions d'amorce** : Questions BAC personnalisées par philosophe

✅ **Test concluant** : Un seul LoRA (Spinoza NB) suffit pour simuler 3 philosophes via prompts système

### Services Obsolètes (Non Utilisés pour BAF)

❌ **Netlify Functions** : Plus utilisé pour BAF (architecture simplifiée)
  - Fichiers déplacés : `garbage/obsolètes_BAF/netlify/`, `netlify.toml`, `package.json`, `src/`
  
❌ **Railway** : Plus utilisé pour BAF (appels directs au Space HF)
  - Fichiers déplacés : `garbage/obsolètes_BAF/snb_api_*.py`, `Procfile`, `nixpacks.toml`
  - ⚠️ **Note** : Railway est toujours utilisé par **I-Amiens** (projet séparé)
  
❌ **Modal** : Plus utilisé pour BAF (Space HF direct)
  - Fichiers déplacés : `garbage/obsolètes_BAF/snb_api_modal.py`, `modal_spinoza_api.py`

**Spaces HF Actifs** :
- ✅ **`bergsonAndFriends`** : Spinoza seul (BAF) → `fjdaz.com/bergson/`
- ✅ **`3_PHI`** : 3 philosophes (SNB) → `fjdaz.com/3phi/`

### Fichiers Actifs

**Frontend :**
- `/Users/francois-jeandazin/bergsonAndFriends/index.html` → Interface 3 philosophes (`fjdaz.com/3phi/`)
- `/Users/francois-jeandazin/bergsonAndFriends/app.js` → JS connecté à 3_PHI
- `index_spinoza.html` → Interface Spinoza seul (`fjdaz.com/bergson/`) - hébergé sur fjdaz.com

**Backend :**
- `/Users/francois-jeandazin/bergsonAndFriends/3_PHI_HF/app.py` → Code Space HF 3_PHI
- `/Users/francois-jeandazin/bergsonAndFriends/3_PHI_HF/requirements.txt` → Dépendances 3_PHI
- `/Users/francois-jeandazin/bergsonAndFriends/3_PHI_HF/README.md` → Documentation 3_PHI
- `/Users/francois-jeandazin/bergsonAndFriends/bergsonAndFriends_HF/app.py` → Code Space HF bergsonAndFriends (Spinoza seul)

**Fichiers Obsolètes (Déplacés) :**
- `garbage/obsolètes_BAF/` → Netlify Functions, Railway, Modal (non utilisés pour BAF)

### Corrections Apportées

1. ✅ **Fix click handler** : `!wasHidden` → `wasHidden` (ligne 48 app.js)
2. ✅ **Fix historique null** : Filtre des entrées null avant envoi au backend (lignes 120-123 app.js)
3. ✅ **Nettoyage structure** : Fichiers obsolètes déplacés dans `garbage/`

### URLs Actuelles

**Frontend :**
- **3 Philosophes** : `https://fjdaz.com/3phi/` → Space `3_PHI`
- **Spinoza Seul** : `https://fjdaz.com/bergson/` → Space `bergsonAndFriends`

**Backend API 3_PHI :**
- **Base** : `https://fjdaz-3-phi.hf.space`
- **Health Check** : `https://fjdaz-3-phi.hf.space/health`
- **Init** : `https://fjdaz-3-phi.hf.space/init/{philosopher}` (spinoza/bergson/kant)
- **Chat** : `https://fjdaz-3-phi.hf.space/chat` (POST)

**Backend API bergsonAndFriends :**
- **Base** : `https://fjdaz-bergsonandfriends.hf.space`
- **API Gradio** : `//chat_function`, `/lambda`, `/lambda_1`

---

**Dernière modification** : 19 novembre 2025 - 22:00
**Status** : Architecture simplifiée et fonctionnelle - Frontend fjdaz.com → API REST HF Space 3_PHI

---

## 🎨 Travail sur les Prompts Système (19 Novembre 2025)

### ✅ Réalisations

#### 1. Traduction des Schèmes Philosophiques ✅

**Objectif** : Adapter les formulations des schèmes logiques pour un public lycéen (18 ans) tout en préservant la qualité philosophique.

**Fichiers modifiés :**
- ✅ `/Users/francois-jeandazin/bergsonAndFriends/3_PHI_HF/Prompts/Schemes Bergson.json`
  - Formulations traduites en langue contemporaine intelligible
  - Style conversationnel, métaphores accessibles
  - Préservation de la rigueur philosophique
  
- ✅ `/Users/francois-jeandazin/bergsonAndFriends/3_PHI_HF/Prompts/Schemes Kant.json`
  - Formulations adaptées au niveau lycéen
  - Simplification progressive (3 versions : contemporain → formel → lycéen)
  - Langage clair sans compromettre la profondeur

**Intégration dans `app.py` :**
- ✅ Fonction `charger_schemes()` → Charge les schèmes depuis JSON
- ✅ Fonctions `formater_schemes_bergson()` et `formater_schemes_kant()` → Formatent pour prompts
- ✅ Schèmes intégrés dans `SYSTEM_PROMPTS` pour Bergson et Kant

#### 2. Variations de Formulations ✅

**Problème identifié :** Formulations trop systématiques ("mais alors", "Donc tu es d'accord") → Dialogue répétitif

**Solution implémentée :**
- ✅ "MAIS ALORS" → "mais alors" (minuscules partout)
- ✅ Instructions variées dans `construire_prompt_contextuel()` :
  - **Résistance** : "Varie tes formulations : 'mais alors', 'pourtant', 'sauf que', 'or', 'il y a une tension ici', 'c'est contradictoire', etc."
  - **Accord** : "Varie tes transitions : 'Donc', 'Alors', 'Cela implique', 'Si on pousse la logique', etc."

**Document créé :**
- ✅ `3_PHI_HF/Prompts/VARIATIONS_FORMULATIONS.md` → Suggestions et stratégies

#### 3. Suppression Code Gradio ✅

**Action :** Retrait complet du code Gradio de `3_PHI_HF/app.py`
- ✅ Interface uniquement via API REST FastAPI
- ✅ Frontend appelle directement `/chat` et `/init/{philosopher}`
- ✅ Simplification du code

### ⚠️ Problème Identifié : RAG et Style

#### Problème Critique

**Constat :** Les passages RAG bruts (texte authentique des œuvres) cassent le style reformulé/adapté de chaque philosophe.

**Raisons :**
- Style lourd, académique vs style conversationnel lycéen
- Première personne vs troisième personne
- Langage contemporain vs langage classique
- Effort de reformulation produit pour chaque philosophe → RAG brut annule cet effort

**Exemple du problème :**
```
Prompt système : "Tu es Spinoza, tu dialogues en première personne, langage lycéen..."
Passage RAG brut : "Deus sive Natura, substantia unica, ex necessitate causae..."
→ Contradiction de style, lourdeur, perte de cohérence
```

#### Solution Proposée

**Document créé :**
- ✅ `3_PHI_HF/Prompts/INTEGRATION_RAG_INTELLIGENTE.md` → Stratégies d'intégration intelligente

**Stratégie recommandée :**
1. **Extraction d'IDÉES** (pas de texte brut)
   - Extraire les concepts/phrases principales
   - Enlever citations, références complexes
   - Simplifier le langage

2. **Reformulation dans le style du philosophe**
   - Première personne ("Je montre que...", "Je révèle que...")
   - Langage lycéen, conversationnel
   - Intégration naturelle dans le style

3. **Instructions claires au modèle**
   - "Reformule ces idées dans TON style"
   - "Ne récite pas le texte brut"
   - "Intègre naturellement dans ton raisonnement"

**Fonction proposée :**
```python
def extraire_idees_passage(passage: Dict, philosopher: str) -> str:
    """
    Extrait les IDÉES d'un passage (pas le texte brut)
    Reformule dans le style du philosophe (première personne, langage lycéen)
    """
    # Découper en phrases, extraire idées principales
    # Reformuler selon le philosophe (Spinoza/Bergson/Kant)
    # Retourner idées reformulées
```

**Avantages :**
- ✅ Style préservé (première personne, lycéen)
- ✅ Pas de lourdeur académique
- ✅ Cohérence philosophique maintenue
- ✅ RAG utile sans casser le dialogue

### 📝 Documents Créés (19 Nov)

1. **`VARIATIONS_FORMULATIONS.md`**
   - Alternatives à "mais alors" et "Donc tu es d'accord"
   - Stratégies d'implémentation
   - Exemples par philosophe

2. **`INTEGRATION_RAG_INTELLIGENTE.md`**
   - 4 stratégies d'intégration RAG
   - Solution au problème de style (extraction + reformulation)
   - Code d'exemple pour `extraire_idees_passage()`
   - Instructions pour utilisation intelligente

### ⏳ Prochaines Étapes

1. ⏳ **Implémenter `extraire_idees_passage()`** dans `app.py`
2. ⏳ **Tester RAG avec reformulation** (vérifier que le style reste conversationnel)
3. ⏳ **Ajuster seuil de pertinence** selon résultats
4. ⏳ **Optimiser performance** (cache corpus en mémoire)

### 🎯 État Actuel des Prompts

**Spinoza :**
- ✅ Schèmes intégrés (via LoRA acquis)
- ✅ Formulations variées (résistance/accord)
- ✅ Style conversationnel, première personne

**Bergson :**
- ✅ Schèmes chargés depuis JSON et intégrés
- ✅ Formulations variées
- ✅ Style conversationnel, métaphores accessibles

**Kant :**
- ✅ Schèmes chargés depuis JSON et intégrés
- ✅ Formulations variées
- ✅ Style conversationnel, distinctions claires

**RAG :**
- ⚠️ Problème de style identifié
- ✅ Solution documentée (extraction + reformulation)
- ⏳ Implémentation à faire

---

**Dernière modification** : 19 novembre 2025 - 23:30
**Status** : Prompts système optimisés, problème RAG identifié et solution documentée


