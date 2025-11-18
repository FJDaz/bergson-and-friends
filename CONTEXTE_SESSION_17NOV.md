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


