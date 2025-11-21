# 🔍 Trouver le Chemin Exact sur le Serveur

## 📋 Questions pour Identifier le Chemin

### 1. Comment accédez-vous au serveur ?

- **SSH ?** → Quel est le chemin de votre home directory ?
- **FTP/SFTP ?** → Dans quel dossier vous connectez-vous ?
- **Interface web (cPanel/Plesk) ?** → Quel est le chemin racine affiché ?

### 2. Où se trouve votre site web ?

Généralement, les sites sont dans :
- `/var/www/html/` (Apache standard)
- `/var/www/` (Apache)
- `/home/username/public_html/` (cPanel)
- `/home/username/www/` (Plesk)
- `/usr/share/nginx/html/` (Nginx)

### 3. Comment avez-vous uploadé les autres fichiers ?

- Où se trouve `index.html` ?
- Où se trouvent les images (`img/Bergson.png`, etc.) ?
- Où se trouve `style.css` ?

## 🔍 Commandes pour Trouver le Fichier

### Si vous êtes en SSH sur le serveur :

```bash
# Chercher le fichier app.js
find / -name "app.js" -type f 2>/dev/null | grep -i bergson

# Ou chercher dans les dossiers communs
find /var/www /home -name "app.js" 2>/dev/null

# Chercher le dossier statics
find /var/www /home -type d -name "statics" 2>/dev/null
```

### Si vous utilisez cPanel/Plesk :

1. Ouvrir le File Manager
2. Naviguer vers le dossier de votre site
3. Chercher le dossier `bergson` ou `statics`

## 🔧 Solution Alternative : Vérifier via l'URL

Puisque `https://fjdaz.com/bergson/statics/app.js` fonctionne (même si c'est l'ancienne version), le chemin HTTP est correct.

Le problème est probablement :
1. **Cache serveur/CDN** très agressif
2. **Le fichier n'a pas été uploadé** au bon endroit
3. **Plusieurs copies** du fichier existent

## ✅ Solution Rapide : Renommer Temporairement

Pour contourner le cache, vous pouvez :

1. **Renommer le fichier** sur le serveur :
   - `app.js` → `app-v2.js`

2. **Modifier index.html** pour pointer vers le nouveau nom :
   ```html
   <script src="https://fjdaz.com/bergson/statics/app-v2.js"></script>
   ```

3. **Uploader les deux fichiers** :
   - `app-v2.js` (nouvelle version, 13 Ko)
   - `index.html` (modifié)

Cela contournera complètement le cache !

---

**Dernière mise à jour :** 17 novembre 2025


