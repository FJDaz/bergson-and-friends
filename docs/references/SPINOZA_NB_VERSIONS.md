# 📦 Archive complète : spinoza_NB - Toutes les versions

## ✅ Historique complet récupéré

**Total de commits :** 12

**Backup créé :**
- Mirror complet : `spinoza_NB_backup_mirror/` (tout l'historique Git)

---

## 📋 Liste de toutes les versions

### 1. **Version actuelle (main)** - 23f53af
- **Description :** Fix: Force model on GPU only (T4 16GB) - no CPU offload for bitsandbytes
- **Fichiers :** `app.py` (version 4-bit en préparation)

### 2. **Version précédente** - fce312e
- **Description :** Fix: Enable CPU offload for 8-bit quantization + fix deprecated torch_dtype
- **Fichiers :** `app.py` (8-bit avec offload CPU)

### 3. **Version 3 endpoints** - 333c7c3
- **Description :** Force rebuild: Confirm 3 API endpoints exposed
- **Fichiers :** `app.py` (3 endpoints `/chat_spinoza`, `/chat_bergson`, `/chat_kant`)

### 4. **Version 3 endpoints Netlify** - b80dadc
- **Description :** Expose 3 API endpoints séparés pour Netlify
- **Fichiers :** `app.py` (3 endpoints avec `api_name`)

### 5. **Version 3 philosophes UI** - 3e23fc4
- **Description :** Interface 3 philosophes avec onglets Gradio
- **Fichiers :** `app.py` (UI avec onglets Spinoza/Bergson/Kant)

### 6. **Version API Gradio** - fda24ba
- **Description :** Enable Gradio API with show_api=True and queue()
- **Fichiers :** `app.py` (avec `show_api=True` et `api_name="/chat_function"`)

### 7. **Version système adaptatif** - ea9a337
- **Description :** Restaure système adaptatif avec historique frontend
- **Fichiers :** `app.py` (système adaptatif V2)

### 8. **Version V2 référence** - 752d809
- **Description :** Fix: Align with working V2 reference code (anti-radotage)
- **Fichiers :** `app.py` (V2 avec corrections)

### 9. **Version V2 complète** - d3c0677 ⭐ **SPINOZA SEUL FONCTIONNEL**
- **Description :** Deploy Spinoza Niveau B V2 - Complete system with adaptive detection
- **Fichiers :** `app.py` (Spinoza seul avec `/chat_function` - version qui fonctionnait !)
- **Note :** Cette version est disponible dans `app_spinoza_seul.py` (modifiée pour `show_api=True`)

### 10. **Version initiale** - b4df233
- **Description :** initial commit
- **Fichiers :** Version de base

---

## 🔄 Comment récupérer une version spécifique

```bash
cd /Users/francois-jeandazin/bergsonAndFriends/spinoza_NB

# Voir toutes les versions
git log --oneline

# Checkout une version spécifique
git checkout d3c0677  # Version Spinoza seul qui fonctionnait
git checkout fda24ba  # Version avec API /chat_function
git checkout 333c7c3  # Version avec 3 endpoints

# Revenir à la version actuelle
git checkout main
```

---

## 📁 Fichiers disponibles dans le repo

- `app.py` - Version actuelle (main)
- `app_spinoza_seul.py` - Version restaurée Spinoza seul (basée sur d3c0677)
- `app_3_philosophes.py` - Version 3 philosophes (ancienne)
- `app_fastapi.py` - Version FastAPI (test)

---

## ✅ Backup complet

- **Repo Git complet :** `spinoza_NB/` avec tout l'historique
- **Mirror backup :** `spinoza_NB_backup_mirror/` (clone --mirror)
- **Fichiers locaux :** Toutes les versions dans les fichiers `app*.py`

**Tout est sauvegardé localement !** 🎉
