# 📊 Rapport d'État - Projet Bergson and Friends

**Date :** 18 novembre 2025  
**Session :** Audit structure dépôt + Identification fichiers actifs

---

## 🎯 État Général

### ✅ Ce qui fonctionne

1. **Frontend Spinoza** (`index_spinoza.html`)
   - ✅ Interface responsive (desktop + mobile)
   - ✅ Pointe vers Railway backend
   - ✅ Dernière modification : 18 nov 22:55
   - **URL Production :** `fjdaz.com/bergsonandfriends/index_spinoza.html` (à confirmer)

2. **Backend Railway**
   - ✅ URL : `https://bergson-api-production.up.railway.app`
   - ✅ Endpoints : `/init/spinoza`, `/chat/spinoza`
   - ⚠️ Statut : À vérifier (logs Railway montrent erreurs mise)

3. **HF Space `bergsonAndFriends`**
   - ✅ URL : `https://fjdaz-bergsonandfriends.hf.space`
   - ✅ Modèle : Qwen 2.5 14B + LoRA Spinoza
   - ✅ GPU : A10G (24GB VRAM)
   - ✅ API Gradio : `//chat_function`, `/lambda`, `/lambda_1`

4. **Netlify Functions**
   - ✅ Functions dans `/netlify/functions/`
   - ✅ `philosopher_rag.js` (principal)
   - ✅ `spinoza_hf.js` (bridge HF Space)
   - ⚠️ Déploiement : Crash récent (à investiguer)

---

## ⚠️ Problèmes Identifiés

### 1. Structure Dépôt - Doublons Majeurs

#### A. Dossiers dupliqués
- **`bergson-and-friends/`** (6.3M) vs **`bergsonAndFriends/`** (2.1M)
  - `bergson-and-friends/` : Ancienne version frontend (à supprimer)
  - `bergsonAndFriends/` : Backend HF Space (à garder)

#### B. Fichiers index.html multiples
- `/index.html` (racine) → Non utilisé actuellement
- `/index_spinoza.html` (racine) → **ACTIF** (frontend Spinoza)
- `/bergson-and-friends/index.html` → Doublon (à supprimer)
- `/bergsonAndFriends/index.html` → Version backend (à garder)
- `/static/index.html` → Doublon (à supprimer)

#### C. Dossiers static/ multiples
- `/static/` (racine) → Utilisé par frontend
- `/bergson-and-friends/static/` → Doublon (à supprimer)
- `/bergsonAndFriends/static/` → Version backend (à garder)
- `/static/static/` → Doublon imbriqué (à supprimer)

#### D. Dossiers netlify/functions/ multiples
- `/netlify/functions/` (racine) → **ACTIF** (utilisé par Netlify)
- `/bergson-and-friends/netlify/functions/` → Non utilisé (à supprimer)
- `/bergsonAndFriends/netlify/functions/` → Non utilisé (à supprimer)

---

### 2. Submodules Git Mal Configurés

**Problème :** Dossiers avec `.git/` mais pas dans `.gitmodules`

- `SNB_orchestrator/` → Erreur Git : "fatal: no submodule mapping found"
- `bergson-and-friends/` → Submodule non configuré
- `bergsonAndFriends/` → Submodule non configuré
- `spinoza_NB/` → Submodule non configuré

**Impact :** Git ne peut pas gérer ces dossiers correctement

---

### 3. Archives et Backups Obsolètes

#### A. Archives Spinoza
- `spinoza_NB_archive/` → Archive version 23f53af (documentée dans docs)
- `spinoza_NB_backup_mirror/` → Backup Git complet (inutile, ~50MB)
- `spinoza_NB_fastapi/` → Version FastAPI non utilisée

#### B. Doublons RAG
- `/RAG/` (racine) → Fichiers `.bak`, `.bak2` uniquement
- `/bergson-and-friends/RAG/` → Doublon (à supprimer)
- `/data/RAG/` → **VERSION SOURCE** (à garder)

#### C. Fichiers de test
- `app_local.js`, `index_local.html`, `index_netlify.html` → Versions de test
- `test-bergson-debug.html`, `test-bergson.html` → Tests locaux
- `railway_deploy.log`, `railway_deploy_hf.log` → Logs (à déplacer vers `docs/logs/`)

---

### 4. Configuration Netlify

**Problème :** `netlify.toml` publie TOUT le dépôt

```toml
[build]
  functions = "netlify/functions"  # ✅ Correct
  publish = "."                    # ⚠️ Publie TOUT (y compris node_modules/, archives, etc.)
```

**Impact :**
- Déploiement lent (publie ~15-20M au lieu de ~5M)
- Risque de crash (fichiers inutiles)
- Confusion sur quel fichier est servi

---

### 5. Logs Railway

**Fichier :** `docs/logs/Railway_logs`

**Erreurs détectées :**
```
✖ Failed to run mise command '/tmp/railpack/mise/mise-2025.11.6 latest python@3.11.9': exit status 1
mise ERROR An IO error occurred when talking to the server
mise ERROR error sending request for url (https://github.com/pyenv/pyenv.git/info/refs?service=git-upload-pack)
```

**Statut :** Railway a des problèmes de déploiement (erreur mise/pyenv)

---

## 📁 Fichiers Actifs (Production)

### Frontend
- ✅ **`/index_spinoza.html`** → Interface Spinoza (responsive)
  - Backend : Railway (`https://bergson-api-production.up.railway.app`)
  - Styles : `https://fjdaz.com/bergson/statics/style.css`
  - Responsive : `https://fjdaz.com/bergson/statics/responsive.css`

### Backend HF Space
- ✅ **`/bergsonAndFriends/app.py`** → Backend Python (Qwen 14B + LoRA)
- ✅ **`/bergsonAndFriends/requirements.txt`** → Dépendances Python
- ✅ **`/bergsonAndFriends/README.md`** → Configuration Space HF

### Netlify Functions
- ✅ **`/netlify/functions/philosopher_rag.js`** → Function principale RAG
- ✅ **`/netlify/functions/spinoza.js`** → Function Spinoza
- ✅ **`/netlify/functions/spinoza_hf.js`** → Bridge HF Space
- ✅ **`/netlify.toml`** → Configuration Netlify

### Configuration
- ✅ **`/package.json`** → Dépendances Node.js (pour Netlify Functions)
- ✅ **`/.gitignore`** → Ignore `.netlify`, etc.

### Documentation
- ✅ **`/docs/`** → Documentation complète (garder intacte)

### Source Data
- ✅ **`/data/RAG/`** → Corpus RAG source (version propre)
- ✅ **`/src/`** → Code source JavaScript (si utilisé)

---

## 🗑️ Fichiers à Supprimer

### Priorité Haute (Impact Netlify)

1. **`/bergson-and-friends/`** (6.3M) → Doublon complet
2. **`/static/static/`** → Doublon imbriqué
3. **`/bergson-and-friends/netlify/functions/`** → Non utilisé
4. **`/bergsonAndFriends/netlify/functions/`** → Non utilisé

### Priorité Moyenne (Archives)

1. **`/spinoza_NB_archive/`** → Archivé dans docs
2. **`/spinoza_NB_backup_mirror/`** → Backup Git inutile
3. **`/spinoza_NB_fastapi/`** → Version non utilisée
4. **`/RAG/`** (racine) → Fichiers `.bak` uniquement
5. **`/bergson-and-friends/RAG/`** → Doublon

### Priorité Basse (Nettoyage)

1. **Fichiers de test :**
   - `app_local.js`
   - `index_local.html`
   - `index_netlify.html`
   - `test-bergson*.html`

2. **Logs racine :**
   - `railway_deploy.log` → Déplacer vers `docs/logs/`
   - `railway_deploy_hf.log` → Déplacer vers `docs/logs/`

3. **Fichiers MD racine :**
   - `DEPLOIEMENT_FINAL.md` → Déplacer vers `docs/tutos/`
   - `DEPLOIEMENT_NETLIFY.md` → Déplacer vers `docs/tutos/`
   - `CONTEXTE_SESSION_17NOV.md` → Déplacer vers `docs/notes/`

4. **Configuration obsolète :**
   - `Procfile` → Railway (non utilisé par Netlify)
   - `requirements_mock.txt` → Mock non utilisé

---

## 🔧 Actions Recommandées

### Phase 1 : Fix Submodules (Urgent)

```bash
# Supprimer .git/ dans submodules pour les transformer en dossiers normaux
rm -rf SNB_orchestrator/.git
rm -rf bergsonAndFriends/.git
# bergson-and-friends/.git sera supprimé avec le dossier
```

### Phase 2 : Supprimer Doublons (Impact Netlify)

```bash
# Supprimer doublon majeur
rm -rf bergson-and-friends/

# Supprimer doublons static
rm -rf static/static/

# Nettoyer fichiers de test
rm -f app_local.js index_local.html index_netlify.html
rm -f test-bergson*.html
```

### Phase 3 : Nettoyer Archives

```bash
# Supprimer archives Spinoza
rm -rf spinoza_NB_archive/
rm -rf spinoza_NB_backup_mirror/
rm -rf spinoza_NB_fastapi/

# Supprimer doublons RAG
rm -rf RAG/
```

### Phase 4 : Réorganiser

```bash
# Déplacer logs
mv railway_deploy*.log docs/logs/

# Déplacer fichiers MD
mv DEPLOIEMENT_*.md docs/tutos/
mv CONTEXTE_SESSION_*.md docs/notes/

# Supprimer obsolètes
rm -f Procfile requirements_mock.txt
```

### Phase 5 : Mettre à jour .gitignore

```gitignore
# Netlify
.netlify

# Node
node_modules/

# Python
.venv/
__pycache__/
*.pyc

# Logs (sauf docs/logs/)
*.log
!docs/logs/*.log

# Archives
spinoza_NB_archive/
spinoza_NB_backup_mirror/
```

---

## 📊 Estimation Gain

### Avant Nettoyage
- **Taille totale :** ~15-20M (estimé)
- **Fichiers inutiles :** ~10M
- **Structure :** Confuse, doublons partout
- **Déploiement Netlify :** Lent, risque crash

### Après Nettoyage
- **Taille totale :** ~5-8M (estimé)
- **Fichiers inutiles :** 0
- **Structure :** Claire, un seul emplacement par type
- **Déploiement Netlify :** Rapide, stable

**Gain :** ~50-60% de réduction, déploiement plus rapide

---

## 🔍 Points de Vigilance

### 1. Railway Backend
- ⚠️ Logs montrent erreurs mise/pyenv
- ⚠️ Statut à vérifier : `https://bergson-api-production.up.railway.app/health`

### 2. Netlify Déploiement
- ⚠️ Crash récent (à investiguer)
- ⚠️ Configuration `publish = "."` publie tout (à optimiser)

### 3. Frontend Production
- ✅ `index_spinoza.html` est le fichier actif
- ⚠️ URL exacte sur fjdaz.com à confirmer
- ⚠️ Backend Railway doit être accessible

### 4. HF Space
- ✅ Space `bergsonAndFriends` actif
- ✅ API Gradio fonctionnelle
- ⚠️ Coût : ~$1/h (A10G)

---

## 📋 Checklist Actions

### Immédiat
- [ ] Vérifier statut Railway backend
- [ ] Investiguer crash Netlify
- [ ] Confirmer URL frontend sur fjdaz.com

### Court Terme
- [ ] Backup complet avant nettoyage
- [ ] Supprimer `bergson-and-friends/` (6.3M)
- [ ] Fix submodules (supprimer `.git/`)
- [ ] Nettoyer archives obsolètes

### Moyen Terme
- [ ] Optimiser `netlify.toml` (publish directory)
- [ ] Mettre à jour `.gitignore`
- [ ] Réorganiser fichiers MD racine
- [ ] Tester déploiement Netlify après nettoyage

---

## 📚 Documentation Référence

- **Audit complet :** `docs/notes/AUDIT_NETTOYAGE_DEPOT.md`
- **Endpoints Gradio :** `docs/notes/ENDPOINTS_GRADIO_BERGSONANDFRIENDS.txt`
- **Explication services :** `docs/notes/EXPLICATION_RAILWAY_NETLIFY.md`
- **Termes techniques :** `docs/notes/TERMES_SERVICES_CLOUD.md`
- **Logs Railway :** `docs/logs/Railway_logs`

---

**Prochaine Étape :** Examiner ce rapport, valider les suppressions, puis appliquer le plan de nettoyage.

