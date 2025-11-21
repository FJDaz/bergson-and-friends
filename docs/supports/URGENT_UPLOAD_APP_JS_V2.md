# 🚨 URGENT : Uploader app.js VERSION 2 sur fjdaz.com

## ❌ Problème Confirmé

Le fichier `app.js` sur `fjdaz.com` est l'**ANCIENNE VERSION** (sans `API_BASE_URL`).

**Vérification :**
```bash
curl https://fjdaz.com/bergson/statics/app.js | grep API_BASE_URL
# Résultat : 0 (pas trouvé)
```

**Conséquence :** Les appels API échouent car le chemin `/.netlify/functions/` n'existe pas sur `fjdaz.com`.

## ✅ Solution

### Fichier à Uploader

**Source (LOCAL, VERSION CORRECTE) :**
- Chemin : `/Users/francois-jeandazin/bergsonAndFriends/static/app.js`
- Contient : `API_BASE_URL` avec l'URL Netlify
- Ligne 6-8 :
  ```javascript
  const API_BASE_URL = window.location.hostname === 'fjdaz.com' 
      ? 'https://chimerical-kashata-65179e.netlify.app/.netlify/functions'
      : '/.netlify/functions';
  ```

**Destination (SERVEUR) :**
- Chemin : `fjdaz.com/bergson/statics/app.js`
- **Action :** Remplacer l'ancien fichier par le nouveau

### Méthode d'Upload

#### Option 1 : SCP (Recommandé)
```bash
scp /Users/francois-jeandazin/bergsonAndFriends/static/app.js user@fjdaz.com:/path/to/bergson/statics/app.js
```

#### Option 2 : SFTP
```bash
sftp user@fjdaz.com
cd bergson/statics
put /Users/francois-jeandazin/bergsonAndFriends/static/app.js app.js
exit
```

#### Option 3 : Interface Web (cPanel/Plesk)
1. Se connecter à l'interface
2. Naviguer vers `/bergson/statics/`
3. Uploader le nouveau `app.js` (remplacer l'ancien)

## ✅ Vérification Après Upload

### 1. Vérifier le contenu
```bash
curl https://fjdaz.com/bergson/statics/app.js | grep -A 2 "API_BASE_URL"
```

**Résultat attendu :**
```javascript
const API_BASE_URL = window.location.hostname === 'fjdaz.com' 
    ? 'https://chimerical-kashata-65179e.netlify.app/.netlify/functions'
```

### 2. Vider le cache navigateur
- **Mac :** `Cmd + Shift + R`
- **Windows :** `Ctrl + Shift + R`

### 3. Tester sur fjdaz.com
1. Ouvrir : `https://fjdaz.com/bergsonandfriends`
2. Console développeur (F12)
3. Vérifier que `API_BASE_URL` est défini :
   ```javascript
   console.log(API_BASE_URL);
   // Doit afficher : https://chimerical-kashata-65179e.netlify.app/.netlify/functions
   ```
4. Vérifier que les philosophes s'initialisent automatiquement

## 📋 Checklist

- [ ] Uploader `static/app.js` (nouvelle version) sur `fjdaz.com/bergson/statics/app.js`
- [ ] Vérifier avec curl que `API_BASE_URL` est présent
- [ ] Vider le cache navigateur
- [ ] Tester depuis `https://fjdaz.com/bergsonandfriends`
- [ ] Vérifier dans la console que les appels API fonctionnent

---

**Dernière mise à jour :** 17 novembre 2025
**Priorité :** 🔴 URGENT


