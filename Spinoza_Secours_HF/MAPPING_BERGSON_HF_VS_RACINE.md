# 📊 Mapping : bergsonAndFriends_HF/ vs Racine

**Date :** 21 novembre 2025  
**Objectif :** Comparer contenus entre `bergsonAndFriends_HF/` et racine pour identifier doublons et décider quoi garder

---

## 📁 Fichiers TXT (RAG Raw)

### Comparaison TXT

| Fichier | bergsonAndFriends_HF/ | data/raw/txt/ | Statut |
|---------|----------------------|---------------|--------|
| `01_esthetique_transcendantale.txt` | ✅ 12K (Nov 17) | ✅ 12K (Nov 10) | 🔄 **DOUBLON** - Garder `data/raw/txt/` |
| `02_analytique_des_concepts.txt` | ✅ 2.5K (Nov 17) | ✅ 2.5K (Nov 10) | 🔄 **DOUBLON** - Garder `data/raw/txt/` |
| `03_antinomies_selection.txt` | ✅ 5.1K (Nov 17) | ✅ 5.1K (Nov 10) | 🔄 **DOUBLON** - Garder `data/raw/txt/` |
| `essai_conscience.txt` | ✅ 355K (Nov 17) | ✅ 355K (Sep 17) | 🔄 **DOUBLON** - Garder `data/raw/txt/` |
| `Éthique_(Saisset,_1861)_Partie_I_clean.txt` | ✅ 90K (Nov 17) | ✅ 90K (Sep 17) | 🔄 **DOUBLON** - Garder `data/raw/txt/` |

**Conclusion :** Tous les fichiers TXT de `bergsonAndFriends_HF/` sont des **doublons** de `data/raw/txt/`.  
**Action :** ✅ Les fichiers TXT dans `bergsonAndFriends_HF/` peuvent être supprimés (sources dans `data/raw/txt/`).

---

## 📂 Structure Comparée

### 1. **netlify/functions/**

#### `bergsonAndFriends_HF/netlify/functions/`
- `bergson.js`
- `kant.js`
- `spinoza.js`
- `spinoza.js.backup`
- `spinoza.js.together_ai_backup`

#### Racine `netlify/functions/`
- ❌ **N'EXISTE PAS** à la racine

**Différence :**
- `bergsonAndFriends_HF/netlify/functions/` est **UNIQUE** (pas de doublon racine)
- Contient `bergson.js`, `kant.js`, `spinoza.js` (spécifiques Space HF)

**Statut :** ✅ **UNIQUE** - Fonctions Netlify pour Space HF uniquement

---

### 2. **static/**

#### `bergsonAndFriends_HF/static/`
- `app.js`
- `fonts/` (28 fichiers .woff/.woff2)
- `img/` (5 fichiers PNG)
- `responsive.css`
- `style.css`

#### Racine `static/`
- `fonts/` (28 fichiers .woff/.woff2)
- `img/` (5 fichiers PNG)
- `responsive.css`
- `style.css`

**Différence :**
- `bergsonAndFriends_HF/static/` a `app.js` (absent racine)
- Autres fichiers identiques

**Statut :** ⚠️ **SIMILAIRES** - `app.js` unique dans `bergsonAndFriends_HF/`

---

### 3. **app.py**

#### `bergsonAndFriends_HF/app.py`
- Application principale (backend HF Space)
- Version standard

#### `bergsonAndFriends_HF/app_with_api.py`
- Version avec API FastAPI

#### Racine `app.py`
- Legacy ? Actif ?

**Statut :** ⚠️ **À VÉRIFIER** - Usage de `app.py` racine

---

### 4. **index.html**

#### `bergsonAndFriends_HF/index.html`
- Interface frontend pour Space HF
- Version backend

#### Racine `index.html`
- Frontend principal ? Legacy ?

**Statut :** ⚠️ **À VÉRIFIER** - Usage de `index.html` racine

---

### 5. **requirements.txt**

#### `bergsonAndFriends_HF/requirements.txt`
- Dépendances pour Space HF

#### Racine `requirements.txt`
- Dépendances racine ? Legacy ?

**Statut :** ⚠️ **À VÉRIFIER** - Usage de `requirements.txt` racine

---

### 6. **README.md**

#### `bergsonAndFriends_HF/README.md`
- Documentation Space HF

#### Racine `README.md`
- Documentation projet principal

**Statut :** ✅ **DIFFÉRENTS** - Contenus différents, garder les deux

---

### 7. **Documentation**

#### `bergsonAndFriends_HF/UPGRADE_PROMPT_SPINOZA.md`
- Documentation upgrade prompt Spinoza

#### Racine `docs/`
- Documentation complète du projet

**Statut :** ✅ **COMPLÉMENTAIRES** - `UPGRADE_PROMPT_SPINOZA.md` spécifique au Space

---

### 8. **Tests**

#### `bergsonAndFriends_HF/test-bergson-debug.html`
#### `bergsonAndFriends_HF/test-bergson.html`

**Statut :** 🗑️ **OBSOLÈTES** - Fichiers de test, peuvent être supprimés ou déplacés vers `garbage/`

---

## 📋 Résumé par Catégorie

### ✅ À GARDER dans `bergsonAndFriends_HF/`

| Fichier/Dossier | Raison |
|----------------|--------|
| `app.py` | Backend Space HF (si Space actif) |
| `app_with_api.py` | Version API (si utilisée) |
| `index.html` | Interface Space HF |
| `requirements.txt` | Dépendances Space HF |
| `README.md` | Documentation Space HF |
| `UPGRADE_PROMPT_SPINOZA.md` | Documentation spécifique |
| `static/app.js` | JavaScript unique (si utilisé) |
| `static/fonts/`, `static/img/`, `static/*.css` | Assets Space HF |
| `netlify/functions/bergson.js`, `kant.js` | Si utilisés (à vérifier) |

### 🗑️ À SUPPRIMER de `bergsonAndFriends_HF/`

| Fichier/Dossier | Raison |
|----------------|--------|
| `*.txt` (5 fichiers) | **DOUBLONS** - Sources dans `data/raw/txt/` |
| `test-bergson*.html` | Fichiers de test obsolètes |
| `netlify/functions/spinoza.js.backup` | Backup obsolète |
| `netlify/functions/spinoza.js.together_ai_backup` | Backup obsolète |

### ⚠️ À VÉRIFIER

| Fichier/Dossier | Question |
|----------------|----------|
| `netlify/functions/bergson.js` | Utilisé par Netlify ? |
| `netlify/functions/kant.js` | Utilisé par Netlify ? |
| `netlify/functions/spinoza.js` | Différent de racine ? |
| `static/app.js` | Utilisé par Space HF ? |
| `app.py` vs `app_with_api.py` | Quelle version est active ? |

---

## 🎯 Plan d'Action Recommandé

### Phase 1 : Suppression Doublons TXT

```bash
# Supprimer fichiers TXT doublons
cd bergsonAndFriends_HF/
rm -f *.txt
# (garder requirements.txt)
```

### Phase 2 : Nettoyage Tests

```bash
# Supprimer fichiers de test
rm -f test-bergson*.html
```

### Phase 3 : Nettoyage Backups

```bash
# Supprimer backups obsolètes
rm -f netlify/functions/*.backup
rm -f netlify/functions/*.together_ai_backup
```

### Phase 4 : Vérification Usage

```bash
# Vérifier usage netlify functions
grep -r "bergson.js\|kant.js" . --exclude-dir=garbage --exclude-dir=node_modules

# Vérifier usage app.js
grep -r "static/app.js" . --exclude-dir=garbage

# Vérifier quelle version app.py est active
grep -r "app_with_api" . --exclude-dir=garbage
```

---

## 📊 Structure Idéale Après Nettoyage

```
bergsonAndFriends_HF/
│
├── app.py                    # Backend Space HF
├── app_with_api.py           # Version API (si utilisée)
├── index.html                # Interface Space HF
├── requirements.txt          # Dépendances
├── README.md                 # Documentation Space
├── UPGRADE_PROMPT_SPINOZA.md # Doc spécifique
│
├── static/
│   ├── app.js                # JavaScript (si utilisé)
│   ├── fonts/                # Fonts
│   ├── img/                  # Images
│   ├── responsive.css
│   └── style.css
│
└── netlify/
    └── functions/
        ├── bergson.js        # (si utilisé)
        ├── kant.js           # (si utilisé)
        └── spinoza.js        # (si différent de racine)
```

**Fichiers supprimés :**
- ❌ `*.txt` (5 fichiers) - Doublons de `data/raw/txt/`
- ❌ `test-bergson*.html` - Tests obsolètes
- ❌ `*.backup` - Backups obsolètes

---

## ⚠️ Précautions

### Avant de supprimer

1. **Backup complet**
   ```bash
   git add -A
   git commit -m "Backup avant nettoyage bergsonAndFriends_HF"
   ```

2. **Vérifier références**
   ```bash
   # Chercher références aux fichiers TXT
   grep -r "01_esthetique_transcendantale" . --exclude-dir=garbage
   ```

3. **Vérifier usage Space HF**
   - Vérifier si Space HF `bergsonAndFriends` utilise ces fichiers
   - Vérifier si `app.py` ou `app_with_api.py` est actif

---

**Dernière mise à jour :** 21 novembre 2025

