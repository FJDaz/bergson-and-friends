# 🧹 Audit Complet - Nettoyage du Dépôt

**Date :** 18 novembre 2025  
**Objectif :** Identifier doublons, archives obsolètes et structure à nettoyer  
**Contexte :** Netlify crash au déploiement, structure confuse avec doublons

---

## 📊 État Actuel - Problèmes Identifiés

### 1. **DOUBLONS MAJEURS** ⚠️

#### A. `bergson-and-friends/` vs `bergsonAndFriends/`

**`bergson-and-friends/`** (6.3M)
- ✅ Contient : `src/`, `RAG/`, `netlify/functions/`, `static/`, `index.html`
- ✅ A son propre `.git` (submodule ?)
- ✅ A son propre `netlify.toml`
- ✅ A son propre `package.json`
- ❓ **Statut :** Probablement ancienne version frontend

**`bergsonAndFriends/`** (2.1M)
- ✅ Contient : `app.py` (backend HF Space), `requirements.txt`, `netlify/functions/`, `static/`, `index.html`
- ✅ A son propre `.git` (submodule ?)
- ✅ **Statut :** Backend HF Space (Space `bergsonAndFriends`)

**PROBLÈME :** Deux dossiers avec noms similaires, contenus différents, tous deux avec `.git`

---

#### B. Fichiers `index.html` multiples

1. **`/index.html`** (racine) → Pointe vers `fjdaz.com/bergson/statics/`
2. **`/bergson-and-friends/index.html`** → Version locale ?
3. **`/bergsonAndFriends/index.html`** → Version backend ?
4. **`/static/index.html`** → Doublon ?

**PROBLÈME :** Netlify publie la racine (`publish = "."`), donc lequel est utilisé ?

---

#### C. Dossiers `static/` multiples

1. **`/static/`** (racine) → Utilisé par `index.html` racine ?
2. **`/bergson-and-friends/static/`** → Version locale ?
3. **`/bergsonAndFriends/static/`** → Version backend ?
4. **`/static/static/`** → Doublon imbriqué ?

**PROBLÈME :** Confusion sur quel `static/` est servi par Netlify

---

#### D. Dossiers `netlify/functions/` multiples

1. **`/netlify/functions/`** (racine) → **UTILISÉ PAR NETLIFY** (config `netlify.toml`)
2. **`/bergson-and-friends/netlify/functions/`** → Non utilisé ?
3. **`/bergsonAndFriends/netlify/functions/`** → Non utilisé ?

**PROBLÈME :** Seul `/netlify/functions/` est utilisé, les autres sont inutiles

---

### 2. **SUBMODULES GIT MAL CONFIGURÉS** ⚠️

**Submodules détectés (avec `.git`) :**
- `SNB_orchestrator/` → Pas dans `.gitmodules`, erreur Git
- `bergson-and-friends/` → Pas dans `.gitmodules` ?
- `bergsonAndFriends/` → Pas dans `.gitmodules` ?
- `spinoza_NB/` → Pas dans `.gitmodules` ?

**PROBLÈME :** Git ne peut pas gérer ces "submodules" car pas de `.gitmodules`

---

### 3. **ARCHIVES ET BACKUPS OBSOLÈTES** 🗑️

#### A. Archives Spinoza
- **`spinoza_NB_archive/`** → Archive version 23f53af
- **`spinoza_NB_backup_mirror/`** → Backup Git complet (dossier `.git` complet)
- **`spinoza_NB_fastapi/`** → Version FastAPI non utilisée ?

**STATUT :** Documenté dans `docs/references/SPINOZA_NB_VERSIONS.md` → Peut être supprimé si archivé ailleurs

---

#### B. Doublons RAG
- **`/RAG/`** (racine) → Fichiers `.bak`, `.bak2`
- **`/bergson-and-friends/RAG/`** → Version propre ?
- **`/data/RAG/`** → Version source ?

**PROBLÈME :** 3 emplacements pour les mêmes fichiers RAG

---

#### C. Fichiers de test/backup
- **`app_local.js`**, **`index_local.html`**, **`index_netlify.html`** → Versions de test ?
- **`test-bergson-debug.html`**, **`test-bergson.html`** → Tests locaux ?
- **`railway_deploy.log`**, **`railway_deploy_hf.log`** → Logs obsolètes ?

---

### 4. **STRUCTURE NETLIFY CONFUSE** ⚠️

**Configuration actuelle (`netlify.toml` racine) :**
```toml
[build]
  functions = "netlify/functions"  # ✅ Utilise /netlify/functions/
  publish = "."                    # ⚠️ Publie TOUT à la racine
```

**PROBLÈME :** Netlify publie TOUT le dépôt, y compris :
- `bergson-and-friends/` (6.3M)
- `bergsonAndFriends/` (2.1M)
- `node_modules/` (énorme)
- `.git/` (si pas ignoré)
- Archives, backups, etc.

**CONSÉQUENCE :** Déploiement lent, crash possible, confusion

---

## ✅ CE QUI DOIT ABSOLUMENT ÊTRE GARDÉ

### 1. **Fichiers Actifs (Production)**

#### A. Frontend (fjdaz.com)
- ✅ **`/index.html`** → Frontend principal (pointe vers fjdaz.com)
- ✅ **`/index_spinoza.html`** → Version Spinoza seule
- ✅ **`/static/app.js`** → JavaScript frontend (si utilisé)
- ✅ **`/static/style.css`**, **`/static/responsive.css`** → Styles
- ✅ **`/static/img/`** → Images (si utilisées)

#### B. Netlify Functions (Production)
- ✅ **`/netlify/functions/philosopher_rag.js`** → Function principale
- ✅ **`/netlify/functions/spinoza.js`** → Function Spinoza
- ✅ **`/netlify/functions/spinoza_hf.js`** → Function HF Space bridge
- ✅ **`/netlify.toml`** → Configuration Netlify

#### C. Backend HF Space
- ✅ **`/bergsonAndFriends/app.py`** → **BACKEND HF SPACE ACTIF**
- ✅ **`/bergsonAndFriends/requirements.txt`** → Dépendances Python
- ✅ **`/bergsonAndFriends/README.md`** → Config Space HF

#### D. Configuration
- ✅ **`/package.json`** → Dépendances Node.js (pour Netlify Functions)
- ✅ **`/.gitignore`** → Ignore `.netlify`, etc.

#### E. Documentation
- ✅ **`/docs/`** → Toute la documentation (garder intacte)

---

### 2. **Fichiers Source (Développement)**

#### A. Source Code
- ✅ **`/src/`** → Code source JavaScript (si utilisé)
- ✅ **`/data/RAG/`** → Corpus RAG source (version propre)
- ✅ **`/scripts/`** → Scripts utilitaires

#### B. Backend Local
- ✅ **`/snb_api_hf.py`** → API Python (si utilisé localement)
- ✅ **`/requirements.txt`** → Dépendances Python racine

---

## 🗑️ CE QUI PEUT ÊTRE SUPPRIMÉ

### 1. **DOUBLONS À SUPPRIMER** (Priorité Haute)

#### A. Dossier `bergson-and-friends/` (6.3M)
**RAISON :** Doublon de `bergsonAndFriends/`, contient ancienne version frontend
- ❌ **`/bergson-and-friends/`** → **SUPPRIMER ENTIÈREMENT**
- ✅ **Garder :** Rien (tout est doublon ou obsolète)

**VÉRIFICATION AVANT SUPPRESSION :**
- [ ] Vérifier que `/netlify/functions/` racine contient les bonnes functions
- [ ] Vérifier que `/index.html` racine est la version active
- [ ] Vérifier que `/static/` racine contient les bons fichiers

---

#### B. Dossier `static/static/` (imbriqué)
**RAISON :** Doublon imbriqué, probable erreur
- ❌ **`/static/static/`** → **SUPPRIMER ENTIÈREMENT**

---

#### C. Fichiers `index.html` doublons
- ❌ **`/static/index.html`** → Supprimer (si doublon)
- ❌ **`/bergson-and-friends/index.html`** → Supprimer avec dossier
- ✅ **Garder :** `/index.html` (racine) et `/index_spinoza.html`

---

#### D. Dossiers `netlify/functions/` inutiles
- ❌ **`/bergson-and-friends/netlify/functions/`** → Supprimer avec dossier
- ❌ **`/bergsonAndFriends/netlify/functions/`** → Supprimer (backend n'en a pas besoin)
- ✅ **Garder :** `/netlify/functions/` (racine) uniquement

---

### 2. **ARCHIVES OBSOLÈTES** (Priorité Moyenne)

#### A. Archives Spinoza
- ❌ **`/spinoza_NB_archive/`** → Supprimer (archivé dans docs)
- ❌ **`/spinoza_NB_backup_mirror/`** → Supprimer (backup Git complet, inutile)
- ⚠️ **`/spinoza_NB/`** → **GARDER** (peut être utilisé comme référence)
- ❌ **`/spinoza_NB_fastapi/`** → Supprimer (version non utilisée)

---

#### B. Doublons RAG
- ❌ **`/RAG/`** (racine) → Supprimer (fichiers `.bak` uniquement)
- ❌ **`/bergson-and-friends/RAG/`** → Supprimer avec dossier
- ✅ **Garder :** `/data/RAG/` (version source propre)

---

#### C. Fichiers de test/backup
- ❌ **`/app_local.js`** → Supprimer (version de test)
- ❌ **`/index_local.html`** → Supprimer (version de test)
- ❌ **`/index_netlify.html`** → Supprimer (version de test)
- ❌ **`/test-bergson-debug.html`** → Supprimer (test local)
- ❌ **`/test-bergson.html`** → Supprimer (test local)
- ❌ **`/railway_deploy.log`** → Déplacer vers `/docs/logs/` ou supprimer
- ❌ **`/railway_deploy_hf.log`** → Déplacer vers `/docs/logs/` ou supprimer

---

### 3. **SUBMODULES MAL CONFIGURÉS** (Priorité Haute)

#### A. `SNB_orchestrator/`
**PROBLÈME :** Submodule sans `.gitmodules`, erreur Git
- ⚠️ **Option 1 :** Supprimer `.git/` dans `SNB_orchestrator/` (devenir dossier normal)
- ⚠️ **Option 2 :** Ajouter à `.gitmodules` si vraiment nécessaire
- ✅ **Recommandation :** Option 1 (supprimer `.git/`)

---

#### B. `bergson-and-friends/` et `bergsonAndFriends/`
**PROBLÈME :** Submodules sans `.gitmodules`
- ✅ **Solution :** Supprimer `bergson-and-friends/` (doublon)
- ⚠️ **`bergsonAndFriends/`** : Supprimer `.git/` (devenir dossier normal) OU ajouter à `.gitmodules`

**RECOMMANDATION :** Supprimer `.git/` dans `bergsonAndFriends/` (pas besoin de submodule)

---

### 4. **AUTRES FICHIERS OBSOLÈTES**

- ❌ **`/DEPLOIEMENT_FINAL.md`** → Déplacer vers `/docs/tutos/` ou supprimer
- ❌ **`/DEPLOIEMENT_NETLIFY.md`** → Déplacer vers `/docs/tutos/` ou supprimer
- ❌ **`/CONTEXTE_SESSION_17NOV.md`** → Déplacer vers `/docs/notes/` ou supprimer
- ❌ **`/Procfile`** → Supprimer (Railway, non utilisé par Netlify)
- ❌ **`/requirements_mock.txt`** → Supprimer (mock non utilisé)

---

## 📋 PLAN D'ACTION RECOMMANDÉ

### Phase 1 : Nettoyage Doublons (Impact Netlify)

1. **Supprimer `bergson-and-friends/`** (6.3M)
   ```bash
   rm -rf bergson-and-friends/
   ```

2. **Supprimer `static/static/`**
   ```bash
   rm -rf static/static/
   ```

3. **Nettoyer fichiers de test**
   ```bash
   rm -f app_local.js index_local.html index_netlify.html
   rm -f test-bergson*.html
   ```

4. **Déplacer logs**
   ```bash
   mv railway_deploy*.log docs/logs/
   ```

---

### Phase 2 : Nettoyage Archives

1. **Supprimer archives Spinoza**
   ```bash
   rm -rf spinoza_NB_archive/
   rm -rf spinoza_NB_backup_mirror/
   rm -rf spinoza_NB_fastapi/
   ```

2. **Supprimer doublons RAG**
   ```bash
   rm -rf RAG/
   # bergson-and-friends/RAG/ sera supprimé avec le dossier
   ```

---

### Phase 3 : Fix Submodules

1. **Supprimer `.git/` dans submodules**
   ```bash
   rm -rf SNB_orchestrator/.git
   rm -rf bergsonAndFriends/.git
   # bergson-and-friends/.git sera supprimé avec le dossier
   ```

2. **Ajouter à `.gitignore`** (si nécessaire)
   ```
   # Submodules devenus dossiers normaux
   SNB_orchestrator/.git
   bergsonAndFriends/.git
   ```

---

### Phase 4 : Réorganisation Documentation

1. **Déplacer fichiers MD racine**
   ```bash
   mv DEPLOIEMENT_*.md docs/tutos/
   mv CONTEXTE_SESSION_*.md docs/notes/
   ```

2. **Supprimer fichiers obsolètes**
   ```bash
   rm -f Procfile requirements_mock.txt
   ```

---

### Phase 5 : Vérification Netlify

1. **Mettre à jour `.gitignore`**
   ```
   # Netlify
   .netlify
   
   # Node
   node_modules/
   
   # Python
   .venv/
   __pycache__/
   *.pyc
   
   # Logs
   *.log
   !docs/logs/*.log
   
   # Archives
   spinoza_NB_archive/
   spinoza_NB_backup_mirror/
   ```

2. **Vérifier `netlify.toml`**
   ```toml
   [build]
     functions = "netlify/functions"
     publish = "."  # ⚠️ Peut-être changer en "static" si on veut publier seulement static/
   
   [functions]
     node_bundler = "esbuild"
   ```

3. **Tester déploiement Netlify**
   - [ ] Push vers GitHub
   - [ ] Vérifier build Netlify
   - [ ] Vérifier que les functions sont bien déployées
   - [ ] Vérifier que le site fonctionne

---

## 📊 ESTIMATION GAIN

**Avant nettoyage :**
- Taille totale : ~15-20M (estimé)
- Fichiers inutiles : ~10M
- Structure : Confuse, doublons partout

**Après nettoyage :**
- Taille totale : ~5-8M (estimé)
- Fichiers inutiles : 0
- Structure : Claire, un seul emplacement par type de fichier

**Gain :** ~50-60% de réduction, déploiement Netlify plus rapide

---

## ⚠️ PRÉCAUTIONS

### Avant de supprimer

1. **Backup complet**
   ```bash
   git add -A
   git commit -m "Backup avant nettoyage"
   git push origin main
   ```

2. **Vérifier références**
   - [ ] Chercher références à `bergson-and-friends/` dans code
   - [ ] Vérifier que `/netlify/functions/` contient tout
   - [ ] Vérifier que `/index.html` racine est la version active

3. **Tester localement**
   - [ ] Tester Netlify Functions localement
   - [ ] Vérifier que le frontend fonctionne

---

## ✅ CHECKLIST FINALE

### À Garder Absolument
- [x] `/index.html` (racine)
- [x] `/index_spinoza.html`
- [x] `/netlify/functions/` (racine)
- [x] `/netlify.toml`
- [x] `/bergsonAndFriends/app.py` (backend HF Space)
- [x] `/package.json`
- [x] `/docs/` (toute la doc)
- [x] `/data/RAG/` (source RAG)
- [x] `/src/` (si utilisé)

### À Supprimer
- [ ] `/bergson-and-friends/` (6.3M)
- [ ] `/static/static/`
- [ ] `/spinoza_NB_archive/`
- [ ] `/spinoza_NB_backup_mirror/`
- [ ] `/spinoza_NB_fastapi/`
- [ ] `/RAG/` (racine, fichiers .bak)
- [ ] Fichiers de test (`app_local.js`, etc.)
- [ ] Logs racine (déplacer vers `docs/logs/`)

### À Réorganiser
- [ ] Fichiers MD racine → `docs/`
- [ ] Fix submodules (supprimer `.git/`)
- [ ] Mettre à jour `.gitignore`

---

**PROCHAINE ÉTAPE :** Examiner ce rapport, valider les suppressions, puis appliquer le plan d'action.

