# 🔍 Debug : Rien ne s'affiche sur fjdaz.com

## ✅ Vérifications à Faire

### 1. Vérifier que app.js est bien uploadé avec la nouvelle version

```bash
# Vérifier la date/modification du fichier
curl -I https://fjdaz.com/bergson/statics/app.js

# Vérifier le contenu (chercher API_BASE_URL)
curl https://fjdaz.com/bergson/statics/app.js | grep -A 2 "API_BASE_URL"
```

**Doit contenir :**
```javascript
const API_BASE_URL = window.location.hostname === 'fjdaz.com' 
    ? 'https://chimerical-kashata-65179e.netlify.app/.netlify/functions'
```

### 2. Vérifier la console navigateur (F12)

**Erreurs possibles :**

#### A. Erreur CORS
```
Access to fetch at 'https://chimerical-kashata-65179e.netlify.app/.netlify/functions/philosopher_rag' from origin 'https://fjdaz.com' has been blocked by CORS policy
```

**Solution :** Vérifier que Netlify Functions a les bons headers CORS (déjà configuré dans `philosopher_rag.js`)

#### B. Erreur 404
```
GET https://chimerical-kashata-65179e.netlify.app/.netlify/functions/philosopher_rag 404
```

**Solution :** Vérifier que la fonction existe sur Netlify

#### C. Erreur de chargement app.js
```
Failed to load resource: https://fjdaz.com/bergson/statics/app.js
```

**Solution :** Uploader la nouvelle version de app.js

### 3. Tester l'API Netlify directement

```bash
# Test action 'init'
curl -X POST https://chimerical-kashata-65179e.netlify.app/.netlify/functions/philosopher_rag \
  -H "Content-Type: application/json" \
  -d '{"action":"init","philosopher":"spinoza"}'
```

**Résultat attendu :**
```json
{
  "philosopher": "spinoza",
  "question": "...",
  "greeting": "Bonjour ! Je suis Spinoza...",
  "history": [[null, "Bonjour ! Je suis Spinoza..."]]
}
```

### 4. Vérifier les logs Netlify

**Dashboard Netlify → Functions → philosopher_rag → Logs**

Chercher :
- Appels depuis `fjdaz.com`
- Erreurs CORS
- Erreurs de timeout
- Erreurs de connexion au Space HF

## 🔧 Solutions Rapides

### Solution 1 : Vider le cache navigateur

**Mac :** `Cmd + Shift + R`
**Windows :** `Ctrl + Shift + R`

### Solution 2 : Vérifier que app.js est bien chargé

Dans la console (F12) :
```javascript
// Vérifier que API_BASE_URL est défini
console.log(API_BASE_URL);
// Doit afficher : https://chimerical-kashata-65179e.netlify.app/.netlify/functions
```

### Solution 3 : Tester l'appel API manuellement

Dans la console (F12) :
```javascript
fetch('https://chimerical-kashata-65179e.netlify.app/.netlify/functions/philosopher_rag', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ action: 'init', philosopher: 'spinoza' })
})
.then(r => r.json())
.then(console.log)
.catch(console.error);
```

## 📋 Checklist Debug

- [ ] app.js uploadé avec la nouvelle version (vérifier avec curl)
- [ ] Console navigateur ouverte (F12) - pas d'erreurs ?
- [ ] API Netlify accessible directement (test curl)
- [ ] Headers CORS corrects dans Netlify Functions
- [ ] Cache navigateur vidé
- [ ] Logs Netlify vérifiés

---

**Dernière mise à jour :** 17 novembre 2025


