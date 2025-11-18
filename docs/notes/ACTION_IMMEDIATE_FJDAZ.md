# 🚨 ACTION IMMÉDIATE : Rien ne s'affiche sur fjdaz.com

## ✅ Vérifications Rapides

### 1. Vérifier que app.js est bien uploadé (NOUVELLE VERSION)

```bash
# Vérifier que le fichier contient API_BASE_URL
curl https://fjdaz.com/bergson/statics/app.js | grep -A 2 "API_BASE_URL"
```

**Doit afficher :**
```javascript
const API_BASE_URL = window.location.hostname === 'fjdaz.com' 
    ? 'https://chimerical-kashata-65179e.netlify.app/.netlify/functions'
```

**Si ce n'est pas le cas :** Uploader la nouvelle version de `static/app.js`

### 2. Ouvrir la console navigateur (F12)

Sur `https://fjdaz.com/bergsonandfriends`, ouvrir la console et vérifier :

#### A. Erreurs JavaScript
- Chercher les erreurs en rouge
- Vérifier que `app.js` est bien chargé

#### B. Vérifier API_BASE_URL
Dans la console, taper :
```javascript
console.log(API_BASE_URL);
// Doit afficher : https://chimerical-kashata-65179e.netlify.app/.netlify/functions
```

#### C. Tester l'appel API manuellement
Dans la console, taper :
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

**Si ça fonctionne :** L'API est OK, le problème est dans le frontend
**Si ça échoue :** Vérifier les erreurs CORS ou réseau

### 3. Vérifier que les éléments HTML existent

Dans la console, taper :
```javascript
// Vérifier que les éléments existent
console.log('bergson:', document.querySelector('#bergson .qa-history'));
console.log('kant:', document.querySelector('#kant .qa-history'));
console.log('spinoza:', document.querySelector('#spinoza .qa-history'));
```

**Si `null` :** Les éléments n'existent pas ou le DOM n'est pas chargé

### 4. Forcer l'initialisation manuellement

Dans la console, taper :
```javascript
// Forcer l'initialisation
['bergson', 'kant', 'spinoza'].forEach(async (id) => {
  try {
    const response = await fetch('https://chimerical-kashata-65179e.netlify.app/.netlify/functions/philosopher_rag', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'init', philosopher: id })
    });
    const data = await response.json();
    const qaHistory = document.querySelector(`#${id} .qa-history`);
    if (qaHistory && data.greeting) {
      qaHistory.innerHTML = `<div class="qa-pair initial-greeting"><div class="answer">${data.greeting.replace(/\n/g, '<br>')}</div></div>`;
    }
    console.log(`✅ ${id} initialized`);
  } catch (error) {
    console.error(`❌ Failed to init ${id}:`, error);
  }
});
```

## 🔧 Solutions Probables

### Solution 1 : app.js pas uploadé avec la nouvelle version

**Action :** Uploader `/Users/francois-jeandazin/bergsonAndFriends/static/app.js` sur `fjdaz.com/bergson/statics/app.js`

### Solution 2 : Cache navigateur

**Action :** Vider le cache (Cmd+Shift+R ou Ctrl+Shift+R)

### Solution 3 : Erreur JavaScript silencieuse

**Action :** Vérifier la console pour les erreurs

### Solution 4 : DOM pas chargé au moment de l'init

**Action :** L'initialisation se fait dans `DOMContentLoaded`, mais peut-être que les éléments `.qa-history` n'existent pas encore

## 📋 Checklist Debug

1. [ ] app.js uploadé avec nouvelle version (vérifier avec curl)
2. [ ] Console navigateur ouverte (F12)
3. [ ] API_BASE_URL défini correctement
4. [ ] Test API manuel fonctionne
5. [ ] Éléments HTML existent
6. [ ] Initialisation manuelle fonctionne

---

**Dernière mise à jour :** 17 novembre 2025


