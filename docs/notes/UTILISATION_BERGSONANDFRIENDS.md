# 📁 Utilisation du Dossier `bergsonAndFriends/`

**Chemin :** `/Users/francois-jeandazin/bergsonAndFriends/bergsonAndFriends/`

---

## 🎯 À Quoi Sert Ce Dossier ?

### **Backend Hugging Face Space**

Le dossier `bergsonAndFriends/` contient le **code source du Space HF `FJDaz/bergsonAndFriends`**.

**Space URL :** https://huggingface.co/spaces/FJDaz/bergsonAndFriends

---

## 📋 Contenu du Dossier

### Fichiers Principaux

1. **`app.py`** (12.2 KB, 360 lignes)
   - ✅ **Application principale Python**
   - Modèle : Qwen 2.5 14B + LoRA Spinoza
   - Framework : Gradio
   - API : Expose `/chat_function` via Gradio

2. **`requirements.txt`**
   - Dépendances Python (torch, transformers, gradio, peft, etc.)

3. **`README.md`**
   - Configuration Space HF (sdk: gradio, app_file: app.py)

4. **`index.html`**
   - Interface frontend HTML (252 lignes)
   - Utilisé par le Space HF pour l'interface web

### Fichiers de Données (Corpus)

- `01_esthetique_transcendantale.txt` (Kant)
- `02_analytique_des_concepts.txt` (Kant)
- `03_antinomies_selection.txt` (Kant)
- `Éthique_(Saisset,_1861)_Partie_I_clean.txt` (Spinoza)
- `essai_conscience.txt` (Bergson)

### Dossiers

- **`static/`** → Fonts, images, CSS (pour l'interface Space HF)
- **`netlify/functions/`** → Functions Netlify (probablement non utilisées par le Space)

---

## 🔌 Utilisation

### ✅ Utilisé par : **Hugging Face Spaces**

**Comment ça fonctionne :**

1. **Déploiement sur HF Spaces**
   - Le dossier `bergsonAndFriends/` est synchronisé avec le Space HF `FJDaz/bergsonAndFriends`
   - Quand vous push le code dans ce dossier → HF Space se met à jour automatiquement
   - HF Spaces lit `app.py` et le fait tourner avec GPU (A10G, 24GB VRAM)

2. **API Gradio**
   - Le Space expose une API Gradio accessible via :
     - `https://fjdaz-bergsonandfriends.hf.space`
   - Endpoints : `//chat_function`, `/lambda`, `/lambda_1`

3. **Interface Web**
   - Le Space héberge aussi `index.html` pour une interface web directe
   - Accessible sur : `https://fjdaz-bergsonandfriends.hf.space`

---

## ❌ NON Utilisé par

### Railway
- **Railway utilise :** Les fichiers à la racine (`snb_api_hf.py`, `snb_api_mock.py`)
- **Railway n'utilise PAS :** Le dossier `bergsonAndFriends/`
- **Railway appelle :** Le Space HF via API Gradio (pas directement le code)

### GitHub (directement)
- **GitHub stocke :** Le code source
- **GitHub n'exécute PAS :** Le code
- **GitHub sert de :** Dépôt de code source uniquement

### Netlify
- **Netlify utilise :** Les functions dans `/netlify/functions/` (racine)
- **Netlify n'utilise PAS :** Le dossier `bergsonAndFriends/`
- **Netlify appelle :** Le Space HF via API Gradio (comme Railway)

---

## 🔄 Flux d'Architecture

```
┌─────────────────────────────────────────┐
│  bergsonAndFriends/ (dossier local)     │
│  - app.py (Qwen 14B + LoRA)            │
│  - requirements.txt                     │
│  - index.html                           │
└─────────────────┬───────────────────────┘
                  │
                  │ git push (si configuré)
                  │ OU upload manuel
                  ▼
┌─────────────────────────────────────────┐
│  Hugging Face Space                     │
│  FJDaz/bergsonAndFriends                │
│  - Déploie app.py sur GPU A10G          │
│  - Expose API Gradio                    │
│  URL: fjdaz-bergsonandfriends.hf.space  │
└─────────────────┬───────────────────────┘
                  │
                  │ API Gradio
                  │ (//chat_function)
                  ▼
┌─────────────────────────────────────────┐
│  Railway / Netlify                      │
│  - Appellent le Space HF via API        │
│  - Ne touchent PAS au code du dossier   │
└─────────────────────────────────────────┘
```

---

## ⚠️ Problème Actuel

### Submodule Mal Configuré

Le dossier `bergsonAndFriends/` a son propre `.git/` mais n'est **pas configuré comme submodule** dans `.gitmodules`.

**Conséquence :**
- Git ne peut pas gérer ce dossier correctement
- Erreur : "fatal: no submodule mapping found"
- Le dossier apparaît comme "modified (untracked content)"

**Solution :**
1. **Option 1 :** Supprimer `.git/` dans `bergsonAndFriends/` → Devenir dossier normal
2. **Option 2 :** Ajouter à `.gitmodules` si vraiment nécessaire comme submodule

---

## 📊 Statut

### ✅ Actif
- **Space HF :** https://fjdaz-bergsonandfriends.hf.space
- **Modèle :** Qwen 2.5 14B + LoRA Spinoza
- **GPU :** A10G (24GB VRAM)
- **Coût :** ~$1/h

### ⚠️ À Vérifier
- Synchronisation avec Space HF (git push ou upload manuel ?)
- Si le dossier local est vraiment synchronisé avec le Space HF

---

## 🎯 Conclusion

**Le dossier `bergsonAndFriends/` sert à :**

1. ✅ **Déployer le backend sur Hugging Face Spaces**
2. ✅ **Contenir le code source du Space HF** (`app.py`, `requirements.txt`, etc.)
3. ✅ **Héberger les fichiers de corpus** (txt pour RAG)
4. ❌ **N'est PAS utilisé par Railway** (Railway appelle le Space via API)
5. ❌ **N'est PAS utilisé par GitHub** (GitHub stocke juste le code)
6. ❌ **N'est PAS utilisé par Netlify** (Netlify appelle le Space via API)

**C'est le code source du Space HF, pas du backend Railway/Netlify.**

