# 🔍 Doublons Restants - Rapport

**Date :** 18 novembre 2025  
**Après nettoyage initial**

---

## ⚠️ Doublons .git/ (Submodules Mal Configurés)

### Dossiers avec .git/ qui ne devraient pas en avoir :

1. **`SNB_orchestrator/.git/`** → Submodule non configuré
2. **`bergsonAndFriends/.git/`** → Submodule non configuré  
3. **`spinoza_NB/.git/`** → Submodule non configuré
4. **`SNB_orchestrator/SNB_orchestrator/.git/`** → Doublon imbriqué

### Dans garbage/ (normal, à ignorer) :
- `garbage/bergson-and-friends/.git/` → OK (dans garbage)
- `garbage/spinoza_NB_fastapi/.git/` → OK (dans garbage)

**Action recommandée :** Supprimer `.git/` dans les 3 dossiers principaux pour les transformer en dossiers normaux

---

## 📁 Doublons de Dossiers

### 1. `static/` (3 occurrences)
- ✅ **`./static/`** (racine) → **ACTIF** (utilisé par frontend)
- ❌ **`./static/static/`** → **DOUBLON IMBRIQUÉ** (à supprimer)
- ⚠️ **`./bergsonAndFriends/static/`** → Backend HF Space (à garder si utilisé)

### 2. `netlify/` (2 occurrences)
- ✅ **`./netlify/`** (racine) → **ACTIF** (utilisé par Netlify)
- ⚠️ **`./bergsonAndFriends/netlify/`** → Backend HF Space (à vérifier si utilisé)

### 3. `RAG/` (2 occurrences)
- ❌ **`./RAG/`** (racine) → Fichiers `.bak` uniquement (à supprimer)
- ✅ **`./data/RAG/`** → **VERSION SOURCE** (à garder)

---

## 📄 Doublons de Fichiers

### 1. `index.html` (3 occurrences)
- ✅ **`./index.html`** (racine) → Frontend principal
- ❌ **`./static/index.html`** → **DOUBLON** (à supprimer)
- ⚠️ **`./bergsonAndFriends/index.html`** → Backend HF Space (à garder si utilisé)

### 2. `requirements.txt` (4 occurrences)
- ✅ **`./requirements.txt`** (racine) → Dépendances Python racine
- ⚠️ **`./spinoza_NB/requirements.txt`** → Spinoza NB (à garder si utilisé)
- ⚠️ **`./SNB_orchestrator/requirements.txt`** → SNB Orchestrator (à garder si utilisé)
- ✅ **`./bergsonAndFriends/requirements.txt`** → Backend HF Space (à garder)

### 3. `README.md` (5 occurrences)
- ✅ **`./README.md`** (racine) → README principal
- ✅ **`./docs/README.md`** → README documentation (à garder)
- ⚠️ **`./spinoza_NB/README.md`** → Spinoza NB (à garder si utilisé)
- ⚠️ **`./SNB_orchestrator/README.md`** → SNB Orchestrator (à garder si utilisé)
- ✅ **`./bergsonAndFriends/README.md`** → Backend HF Space (à garder)

### 4. `netlify.toml` (2 occurrences)
- ✅ **`./netlify.toml`** (racine) → **ACTIF** (utilisé par Netlify)
- ❌ **`./.netlify/netlify.toml`** → Cache Netlify (à ignorer, dans .gitignore)

---

## 🗑️ Actions Recommandées

### Priorité Haute

1. **Supprimer doublons imbriqués**
   ```bash
   rm -rf static/static/
   rm -f static/index.html
   ```

2. **Supprimer RAG/ racine** (fichiers .bak uniquement)
   ```bash
   rm -rf RAG/
   ```

3. **Supprimer .git/ dans submodules** (pour les transformer en dossiers normaux)
   ```bash
   rm -rf SNB_orchestrator/.git
   rm -rf bergsonAndFriends/.git
   rm -rf spinoza_NB/.git
   rm -rf SNB_orchestrator/SNB_orchestrator/.git
   ```

### Priorité Moyenne

4. **Vérifier et supprimer netlify/ dans bergsonAndFriends/**
   - Si non utilisé par le backend HF Space → supprimer
   - Si utilisé → garder

---

## ✅ Fichiers à Garder (Légitimes)

### Dossiers avec leur propre .git/ (si vraiment nécessaires comme submodules)
- À décider : `SNB_orchestrator/`, `bergsonAndFriends/`, `spinoza_NB/`
- **Option :** Les transformer en dossiers normaux (supprimer `.git/`)

### Fichiers dans sous-dossiers (légitimes)
- `bergsonAndFriends/requirements.txt` → Backend HF Space
- `bergsonAndFriends/README.md` → Backend HF Space
- `spinoza_NB/requirements.txt` → Spinoza NB
- `SNB_orchestrator/requirements.txt` → SNB Orchestrator

---

## 📊 Résumé

### Doublons à Supprimer
- ❌ `static/static/` (doublon imbriqué)
- ❌ `static/index.html` (doublon)
- ❌ `RAG/` (racine, fichiers .bak)
- ❌ `.git/` dans 4 dossiers (submodules mal configurés)

### À Vérifier
- ⚠️ `bergsonAndFriends/netlify/` → Utilisé par backend ?
- ⚠️ `bergsonAndFriends/static/` → Utilisé par backend ?

---

**Prochaine étape :** Appliquer les suppressions de doublons identifiés.

