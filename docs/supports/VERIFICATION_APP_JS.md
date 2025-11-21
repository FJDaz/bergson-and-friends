# ✅ Vérification : app.js sur fjdaz.com

## ❌ Résultat de la Vérification

```bash
curl https://fjdaz.com/bergson/statics/app.js | grep -A 2 "API_BASE_URL"
# Résultat : AUCUNE SORTIE (API_BASE_URL non trouvé)
```

**Conclusion :** Le fichier sur le serveur est l'**ANCIENNE VERSION** (sans `API_BASE_URL`).

**Taille serveur :** 19015 bytes (ancienne version)
**Taille locale :** À vérifier (nouvelle version avec `API_BASE_URL`)

## ✅ Action Requise

### Uploader la Nouvelle Version

**Fichier source :**
```
/Users/francois-jeandazin/bergsonAndFriends/static/app.js
```

**Destination :**
```
fjdaz.com/bergson/statics/app.js
```

### Méthodes d'Upload

#### Option 1 : SCP
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

#### Option 3 : Interface Web
1. Se connecter à l'interface d'administration (cPanel/Plesk)
2. Naviguer vers `/bergson/statics/`
3. Uploader le nouveau `app.js` (remplacer l'ancien)

## ✅ Vérification Après Upload

### 1. Vérifier que API_BASE_URL est présent
```bash
curl https://fjdaz.com/bergson/statics/app.js | grep -A 2 "API_BASE_URL"
```

**Résultat attendu :**
```javascript
const API_BASE_URL = window.location.hostname === 'fjdaz.com' 
    ? 'https://chimerical-kashata-65179e.netlify.app/.netlify/functions'
```

### 2. Vérifier la taille
```bash
curl -I https://fjdaz.com/bergson/statics/app.js | grep -i content-length
```

**Taille attendue :** Légèrement supérieure à 19015 bytes (nouvelle version avec `API_BASE_URL`)

### 3. Tester dans le navigateur
1. Vider le cache : `Cmd+Shift+R` (Mac) ou `Ctrl+Shift+R` (Windows)
2. Ouvrir : `https://fjdaz.com/bergsonandfriends`
3. Console (F12) : Vérifier que `API_BASE_URL` est défini
4. Les philosophes devraient s'initialiser automatiquement

## 📋 Différences Entre les Versions

### Ancienne Version (sur serveur)
- ❌ Pas de `API_BASE_URL`
- ❌ Appels directs à `/.netlify/functions/philosopher_rag`
- ❌ Ne fonctionne pas sur `fjdaz.com`

### Nouvelle Version (locale)
- ✅ `API_BASE_URL` configuré
- ✅ Détection automatique : `fjdaz.com` → URL Netlify complète
- ✅ Fonctionne sur `fjdaz.com` et Netlify

---

**Dernière vérification :** 17 novembre 2025
**Status :** ⚠️ Upload requis


