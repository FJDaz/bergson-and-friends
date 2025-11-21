# 🚨 FIX URGENT : Configuration URL API Netlify

## ❌ Problème

Le frontend sur `fjdaz.com` appelle `/.netlify/functions/philosopher_rag` mais ce chemin n'existe que sur Netlify, pas sur un serveur classique.

**Erreur :** Les appels API échouent car le chemin `/.netlify/functions/` n'existe pas sur `fjdaz.com`.

## ✅ Solution Appliquée

J'ai modifié `static/app.js` pour utiliser une variable `API_BASE_URL` configurable :

```javascript
const API_BASE_URL = window.location.hostname === 'fjdaz.com' 
    ? 'https://votre-site.netlify.app/.netlify/functions'  // ⚠️ À CONFIGURER
    : '/.netlify/functions';  // Chemin relatif si sur Netlify
```

## 🔧 Action Requise

**Vous devez remplacer `https://votre-site.netlify.app` par votre vraie URL Netlify.**

### Comment trouver votre URL Netlify ?

1. **Dashboard Netlify** → Votre site
2. **Settings** → **General** → **Site details**
3. **Site URL** : `https://[votre-site].netlify.app`

### Exemple

Si votre site Netlify est `https://bergson-and-friends.netlify.app`, alors :

```javascript
const API_BASE_URL = window.location.hostname === 'fjdaz.com' 
    ? 'https://bergson-and-friends.netlify.app/.netlify/functions'
    : '/.netlify/functions';
```

## 📝 Fichier à Modifier

**Fichier :** `/Users/francois-jeandazin/bergsonAndFriends/static/app.js`

**Ligne 7 :** Remplacer `https://votre-site.netlify.app` par votre URL Netlify

## ✅ Après Modification

1. **Uploader** `static/app.js` sur `fjdaz.com/bergson/statics/app.js`
2. **Tester** depuis `https://fjdaz.com/bergsonandfriends`
3. **Vérifier** dans la console (F12) que les appels API fonctionnent

## 🔍 Alternative : Proxy sur fjdaz.com

Si vous préférez, vous pouvez configurer un proxy sur `fjdaz.com` pour rediriger `/api/*` vers Netlify :

```nginx
# Exemple configuration Nginx
location /api/ {
    proxy_pass https://votre-site.netlify.app/.netlify/functions/;
}
```

Puis dans `app.js` :
```javascript
const API_BASE_URL = '/api';
```

---

**Dernière mise à jour :** 17 novembre 2025


