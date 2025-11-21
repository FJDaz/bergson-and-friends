# Guide : Upload app.js sur fjdaz.com

## 📋 Objectif

Uploader le fichier `static/app.js` sur le serveur `fjdaz.com` pour qu'il soit accessible à l'URL :
```
https://fjdaz.com/bergson/statics/app.js
```

## 📁 Fichier Source

**Local :** `/Users/francois-jeandazin/bergsonAndFriends/static/app.js`

**Destination :** `fjdaz.com/bergson/statics/app.js`

## 🚀 Méthodes d'Upload

### Option 1 : FTP/SFTP (si serveur classique)

```bash
# Exemple avec sftp
sftp user@fjdaz.com
cd bergson/statics
put /Users/francois-jeandazin/bergsonAndFriends/static/app.js app.js
exit
```

### Option 2 : SCP (si SSH activé)

```bash
scp /Users/francois-jeandazin/bergsonAndFriends/static/app.js user@fjdaz.com:/path/to/bergson/statics/app.js
```

### Option 3 : Interface Web (cPanel, Plesk, etc.)

1. Se connecter à l'interface d'administration du serveur
2. Naviguer vers `/bergson/statics/`
3. Uploader `app.js`
4. Vérifier les permissions (lecture publique)

### Option 4 : Git (si le repo est sur le serveur)

Si le serveur a un repo Git :

```bash
# Sur le serveur
cd /path/to/fjdaz.com/bergson/statics
git pull origin main  # Si app.js est dans le repo
# OU
cp /path/to/bergsonAndFriends/static/app.js app.js
```

## ✅ Vérification

Après l'upload, vérifier que le fichier est accessible :

```bash
curl -I https://fjdaz.com/bergson/statics/app.js
```

**Résultat attendu :**
- Status: `200 OK`
- Content-Type: `application/javascript` ou `text/javascript`

**Si erreur 404 :**
- Vérifier le chemin exact sur le serveur
- Vérifier les permissions du fichier (chmod 644)
- Vérifier la configuration du serveur web

## 🔍 Test dans le Navigateur

1. Ouvrir : `https://fjdaz.com/bergsonandfriends`
2. Ouvrir la console développeur (F12)
3. Vérifier qu'il n'y a pas d'erreur de chargement de `app.js`
4. Vérifier que le script s'exécute (logs dans la console)

## ⚠️ Notes Importantes

- Le fichier doit être accessible en lecture publique
- Pas de cache navigateur : utiliser `Cmd+Shift+R` (Mac) ou `Ctrl+Shift+R` (Windows) pour forcer le rechargement
- Vérifier que le MIME type est correct (`application/javascript`)

---

**Dernière mise à jour :** 17 novembre 2025

