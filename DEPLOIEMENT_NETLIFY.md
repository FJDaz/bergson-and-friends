# 🚀 Déploiement Netlify → HF Space (Bypass Railway)

**Date**: 18 novembre 2025
**Architecture**: Frontend → Netlify Functions → HF Space Gradio

---

## ✅ Fichiers Créés

### 1. Netlify Function
- **Fichier**: `netlify/functions/spinoza_hf.js`
- **Endpoint**: `/.netlify/functions/spinoza_hf`
- **Dépendance**: `@gradio/client` (déjà dans package.json)

### 2. Config Netlify
- **Fichier**: `netlify.toml`
- **Build**: Functions dans `netlify/functions/`

---

## 📋 Étapes de Déploiement

### 1. Push vers GitHub (quand stable)
```bash
git add netlify/ netlify.toml package.json
git commit -m "Add Netlify Function for HF Space bridge"
git push origin main
```

### 2. Connecter à Netlify
1. Aller sur https://app.netlify.com
2. New site → Import existing project
3. Connect to GitHub → `bergson-and-friends`
4. Build settings :
   - Build command: `npm install`
   - Publish directory: `.`
   - Functions directory: `netlify/functions`

### 3. Déployer
Netlify auto-deploy à chaque push sur `main`.

---

## 🔌 API Netlify Function

### Endpoint Init
```javascript
POST /.netlify/functions/spinoza_hf
{
  "action": "init"
}

// Retourne:
{
  "question": "La liberté est-elle une illusion ?",
  "greeting": "Bonjour ! Je suis Spinoza...",
  "history": [[null, "greeting..."]]
}
```

### Endpoint Chat
```javascript
POST /.netlify/functions/spinoza_hf
{
  "action": "chat",
  "message": "La joie augmente-t-elle ma puissance?",
  "history": []
}

// Retourne:
{
  "reply": "Réponse de Qwen 14B...",
  "history": [[user, assistant], ...]
}
```

---

## 🔄 Adapter le Frontend

Modifier `index_spinoza.html` ligne 88 :

```javascript
// AVANT (Railway):
const API_BASE_URL = 'https://bergson-api-production.up.railway.app';

// APRÈS (Netlify):
const API_BASE_URL = 'https://[ton-site].netlify.app/.netlify/functions/spinoza_hf';
```

Et adapter les appels :

```javascript
// Init
const response = await fetch(API_BASE_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ action: 'init' })
});

// Chat
const response = await fetch(API_BASE_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    action: 'chat',
    message: userMessage,
    history: conversationHistory
  })
});
```

---

## 🎯 Avantages vs Railway

✅ **Pas de problème GitHub/pyenv** : Node.js build toujours stable
✅ **Tier gratuit** : 125k requêtes/mois gratuites
✅ **Auto-deploy** : Push → Deploy automatique
✅ **Direct HF Space** : Pas de proxy intermédiaire

---

## ⚠️ Important

- **HF Space doit tourner** : Vérifie que le Space est Running, pas Paused
- **Gradio client** : `@gradio/client` déjà installé dans package.json
- **CORS** : Headers CORS déjà configurés dans la fonction

---

## 🧪 Test Local

```bash
# Installer Netlify CLI
npm install -g netlify-cli

# Tester en local
netlify dev

# Test endpoint
curl -X POST http://localhost:8888/.netlify/functions/spinoza_hf \
  -H "Content-Type: application/json" \
  -d '{"action":"init"}'
```

---

**Prochaine étape** : Attendre que GitHub soit stable, puis push + deploy Netlify ! 🚀
