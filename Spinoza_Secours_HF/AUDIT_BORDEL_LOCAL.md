# 🧹 Audit Complet : Le Bordel en Local

**Date :** 21 novembre 2025  
**Objectif :** Identifier ce qui sert, ce qui flotte, ce qui n'a pas de place, ce qui devrait être ailleurs

---

## 📊 État Actuel de la Structure

### ✅ CE QUI SERT (Actif/Production)

#### 1. **Spaces HF Actifs**

**`3_PHI_HF/`** ✅ **ACTIF**
- **Usage :** Space HF principal (Qwen 14B, 3 philosophes)
- **Status :** ⏸️ Paused (à vérifier)
- **Fichiers :** `app.py`, `requirements.txt`, `Prompts/`
- **Place :** ✅ Bonne place (racine, clair)

**`Spinoza_Secours_HF/`** ✅ **ACTIF**
- **Usage :** Space HF secours (Mistral 7B, Spinoza seul)
- **Status :** 🟢 Actif (Colab + ngrok)
- **Fichiers :** `index_spinoza.html`, `prompt_systeme_hybride.py`, rapports
- **Place :** ✅ Bonne place (racine, clair)

**`bergsonAndFriends_HF/`** ⚠️ **À VÉRIFIER**
- **Usage :** Ancien Space HF ? Archive ?
- **Status :** ❓ Non clair
- **Fichiers :** `app.py`, `app_with_api.py`, `index.html`, corpus textes
- **Place :** ⚠️ Devrait être dans `garbage/` ou `docs/archives/` si obsolète

#### 2. **Données Actives**

**`data/FT/`** ✅ **ACTIF**
- **Usage :** Datasets fine-tuning
- **Fichiers :** `Dataset Niveau A Schemes.txt`, `processed/*.jsonl`
- **Place :** ✅ Bonne place (structure claire)

**`data/RAG/`** ✅ **ACTIF**
- **Usage :** Corpus RAG (glossaires, textes dialogiques)
- **Fichiers :** Corpus Spinoza, Bergson, Kant
- **Place :** ✅ Bonne place (source propre)

**`data/raw/txt/`** ✅ **ACTIF**
- **Usage :** Textes sources bruts
- **Place :** ✅ Bonne place

#### 3. **Code Actif**

**`rag_system.py`** ✅ **ACTIF**
- **Usage :** Système RAG principal
- **Place :** ⚠️ Devrait être dans `scripts/` ou `tools/` ?

**`app.py`** (racine) ⚠️ **À VÉRIFIER**
- **Usage :** Legacy ? Actif ?
- **Place :** ❌ Devrait être dans `garbage/` si obsolète

**`app.js`** (racine) ⚠️ **À VÉRIFIER**
- **Usage :** Legacy ? Actif ?
- **Place :** ❌ Devrait être dans `garbage/` si obsolète

**`index.html`** (racine) ⚠️ **À VÉRIFIER**
- **Usage :** Frontend principal ? Legacy ?
- **Place :** ⚠️ À clarifier

#### 4. **Documentation**

**`docs/`** ✅ **ACTIF**
- **Usage :** Documentation complète
- **Place :** ✅ Bonne place

**`CLAUDE.md`** ✅ **ACTIF**
- **Usage :** Guide pour Claude Code
- **Place :** ✅ Bonne place (racine)

**`README.md`** ✅ **ACTIF**
- **Usage :** Documentation projet
- **Place :** ✅ Bonne place (racine)

#### 5. **Scripts Utilitaires**

**`scripts/`** ✅ **ACTIF**
- **Usage :** Scripts de préparation, tests
- **Place :** ✅ Bonne place

---

### 🗑️ CE QUI FLOTTE (Obsolète/Archive)

#### 1. **Dossier `garbage/`** 🗑️ **ARCHIVE**

**Contenu :**
- `app_local.js`, `app_static_old.js`, `app-new.js`, `app-v2.js`
- `index_local.html`, `index_netlify.html`, `index_spinoza_netlify.html`
- `bergson-and-friends/` (6.3M) - Doublon majeur
- `spinoza_NB_archive/` - Archive Spinoza
- `spinoza_NB_backup_mirror/` - Backup Git
- `spinoza_NB_fastapi/` - Version FastAPI obsolète
- `obsolètes_BAF/` - Archives BAF
- `Procfile`, `railway_deploy*.log`, `requirements_mock.txt`

**Status :** ✅ **Bonne place** (déjà dans `garbage/`)
**Action :** Rien à faire (déjà archivé)

#### 2. **Doublons RAG**

**`RAG/`** (racine) 🗑️ **OBSOLÈTE**
- **Contenu :** Fichiers `.bak`, `.bak2`
- **Place :** ❌ Devrait être supprimé (doublons de `data/RAG/`)
- **Action :** Supprimer

#### 3. **Doublons Static**

**`static/static/`** 🗑️ **DOUBLON IMBRIQUÉ**
- **Contenu :** Doublon imbriqué (erreur)
- **Place :** ❌ Devrait être supprimé
- **Action :** Supprimer

#### 4. **Fichiers Racine Obsolètes**

**`DEPLOY_HF_SPACE_API.md`** ⚠️ **À DÉPLACER**
- **Place :** ❌ Devrait être dans `docs/tutos/`
- **Action :** Déplacer

---

### ❌ CE QUI N'A PAS DE PLACE (Mal organisé)

#### 1. **Fichiers Racine qui Devraient Ailleurs**

**`rag_system.py`** (racine)
- **Problème :** Code utilitaire à la racine
- **Place actuelle :** Racine
- **Place idéale :** `scripts/` ou `tools/`
- **Action :** Déplacer vers `scripts/rag_system.py`

**`app.py`** (racine)
- **Problème :** Legacy ? Actif ?
- **Place actuelle :** Racine
- **Place idéale :** `garbage/` si obsolète, ou supprimer
- **Action :** Vérifier usage, puis déplacer/supprimer

**`app.js`** (racine)
- **Problème :** Legacy ? Actif ?
- **Place actuelle :** Racine
- **Place idéale :** `garbage/` si obsolète, ou supprimer
- **Action :** Vérifier usage, puis déplacer/supprimer

**`index.html`** (racine)
- **Problème :** Frontend principal ? Legacy ?
- **Place actuelle :** Racine
- **Place idéale :** À clarifier (si actif, garder, sinon `garbage/`)
- **Action :** Vérifier usage

#### 2. **Dossiers qui Devraient Ailleurs**

**`bergsonAndFriends_HF/`**
- **Problème :** Ancien Space ? Archive ?
- **Place actuelle :** Racine
- **Place idéale :** `garbage/` ou `docs/archives/` si obsolète
- **Action :** Vérifier si encore utilisé, sinon archiver

**`tools/`** (vide ?)
- **Problème :** Dossier vide ou non utilisé
- **Place actuelle :** Racine
- **Place idéale :** Supprimer si vide, ou utiliser pour `rag_system.py`
- **Action :** Vérifier contenu

**`skills/`** (vide ?)
- **Problème :** Dossier vide ou non utilisé
- **Place actuelle :** Racine
- **Place idéale :** Supprimer si vide
- **Action :** Vérifier contenu

#### 3. **Node Modules**

**`node_modules/`** (racine)
- **Problème :** Dépendances Node.js à la racine
- **Place actuelle :** Racine
- **Place idéale :** ✅ Bonne place (standard Node.js)
- **Action :** Rien (mais vérifier `.gitignore`)

---

### 🔄 CE QUI DEVRAIT ÊTRE AILLEURS

#### 1. **Fichiers à Déplacer**

**`DEPLOY_HF_SPACE_API.md`** → `docs/tutos/`
- **Raison :** Documentation tuto
- **Action :** Déplacer

**`rag_system.py`** → `scripts/rag_system.py` ou `tools/rag_system.py`
- **Raison :** Code utilitaire
- **Action :** Déplacer

**`bergsonAndFriends_HF/`** → `garbage/bergsonAndFriends_HF/` (si obsolète)
- **Raison :** Archive si non utilisé
- **Action :** Vérifier usage, puis archiver si obsolète

#### 2. **Fichiers à Supprimer**

**`RAG/`** (racine) - Fichiers `.bak`
- **Raison :** Doublons de `data/RAG/`
- **Action :** Supprimer

**`static/static/`** - Doublon imbriqué
- **Raison :** Erreur de structure
- **Action :** Supprimer

**`tools/`** et **`skills/`** - Si vides
- **Raison :** Dossiers inutiles
- **Action :** Supprimer si vides

---

## 📋 PLAN D'ACTION RECOMMANDÉ

### Phase 1 : Vérifications (URGENT)

```bash
# Vérifier usage fichiers racine
grep -r "app.py" . --exclude-dir=garbage --exclude-dir=node_modules
grep -r "app.js" . --exclude-dir=garbage --exclude-dir=node_modules
grep -r "index.html" . --exclude-dir=garbage --exclude-dir=node_modules

# Vérifier contenu dossiers
ls -la tools/
ls -la skills/
ls -la bergsonAndFriends_HF/
```

### Phase 2 : Nettoyage Doublons (URGENT)

```bash
# Supprimer doublons RAG
rm -rf RAG/

# Supprimer doublon static imbriqué
rm -rf static/static/
```

### Phase 3 : Réorganisation (MOYENNE PRIORITÉ)

```bash
# Déplacer rag_system.py
mv rag_system.py scripts/rag_system.py

# Déplacer documentation
mv DEPLOY_HF_SPACE_API.md docs/tutos/DEPLOY_HF_SPACE_API.md

# Archiver bergsonAndFriends_HF si obsolète
# (après vérification)
mv bergsonAndFriends_HF/ garbage/bergsonAndFriends_HF_archive/
```

### Phase 4 : Nettoyage Final (BASSE PRIORITÉ)

```bash
# Supprimer dossiers vides
rmdir tools/ skills/ 2>/dev/null || echo "Dossiers non vides ou inexistants"

# Supprimer fichiers obsolètes racine (après vérification)
# rm app.py app.js index.html  # SEULEMENT si confirmé obsolète
```

---

## 📊 RÉSUMÉ PAR CATÉGORIE

### ✅ À GARDER (Actif)

| Fichier/Dossier | Usage | Place | Action |
|----------------|-------|-------|--------|
| `3_PHI_HF/` | Space HF principal | ✅ Racine | Rien |
| `Spinoza_Secours_HF/` | Space HF secours | ✅ Racine | Rien |
| `data/` | Datasets + RAG | ✅ Racine | Rien |
| `docs/` | Documentation | ✅ Racine | Rien |
| `scripts/` | Scripts utilitaires | ✅ Racine | Rien |
| `garbage/` | Archives | ✅ Racine | Rien |
| `CLAUDE.md` | Guide Claude | ✅ Racine | Rien |
| `README.md` | Doc projet | ✅ Racine | Rien |

### 🗑️ À SUPPRIMER (Obsolète)

| Fichier/Dossier | Raison | Action |
|----------------|--------|--------|
| `RAG/` (racine) | Doublons `.bak` | Supprimer |
| `static/static/` | Doublon imbriqué | Supprimer |
| `tools/` (si vide) | Dossier inutile | Supprimer |
| `skills/` (si vide) | Dossier inutile | Supprimer |

### 🔄 À DÉPLACER (Mal organisé)

| Fichier/Dossier | Place Actuelle | Place Idéale | Action |
|----------------|----------------|--------------|--------|
| `rag_system.py` | Racine | `scripts/` | Déplacer |
| `DEPLOY_HF_SPACE_API.md` | Racine | `docs/tutos/` | Déplacer |
| `bergsonAndFriends_HF/` | Racine | `garbage/` (si obsolète) | Vérifier puis archiver |

### ⚠️ À VÉRIFIER (Usage incertain)

| Fichier/Dossier | Question | Action |
|----------------|----------|--------|
| `app.py` (racine) | Legacy ou actif ? | Vérifier usage |
| `app.js` (racine) | Legacy ou actif ? | Vérifier usage |
| `index.html` (racine) | Frontend principal ? | Vérifier usage |
| `bergsonAndFriends_HF/` | Ancien Space ? | Vérifier usage |

---

## 🎯 STRUCTURE IDÉALE

```
bergsonAndFriends/
│
├── 📂 3_PHI_HF/              # Space HF principal
├── 📂 Spinoza_Secours_HF/     # Space HF secours
├── 📂 data/                   # Données (FT, RAG, raw)
├── 📂 docs/                   # Documentation
├── 📂 scripts/                # Scripts (incl. rag_system.py)
├── 📂 garbage/                # Archives (incl. bergsonAndFriends_HF si obsolète)
│
├── 📄 README.md
├── 📄 CLAUDE.md
├── 📄 LICENSE
│
└── 📄 index.html              # Frontend principal (si actif)
```

**Fichiers supprimés :**
- ❌ `RAG/` (racine)
- ❌ `static/static/`
- ❌ `app.py`, `app.js` (racine) - si obsolètes
- ❌ `tools/`, `skills/` - si vides

---

## ⚠️ PRÉCAUTIONS

### Avant de supprimer/déplacer

1. **Backup complet**
   ```bash
   git add -A
   git commit -m "Backup avant nettoyage structure"
   git push origin main
   ```

2. **Vérifier références**
   ```bash
   # Chercher références aux fichiers à supprimer
   grep -r "rag_system" . --exclude-dir=garbage
   grep -r "app.py" . --exclude-dir=garbage
   ```

3. **Tester après nettoyage**
   - Vérifier que les imports fonctionnent
   - Vérifier que les scripts fonctionnent
   - Vérifier que la documentation est à jour

---

**Dernière mise à jour :** 21 novembre 2025

