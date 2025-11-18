# Guide : Upload index.html sur fjdaz.com

## 🚨 Problème Actuel

L'erreur dans la console montre :
```
GET https://fjdaz.com/static/app.js net::ERR_ABORTED 404 (Not Found)
```

Cela signifie que `index.html` sur le serveur utilise encore l'ancien chemin `/static/app.js` au lieu de `https://fjdaz.com/bergson/statics/app.js`.

## 📋 Solution

### Étape 1: Vérifier le fichier local

Le fichier local `/Users/francois-jeandazin/bergsonAndFriends/index.html` a déjà le bon chemin (ligne 150) :
```html
<script src="https://fjdaz.com/bergson/statics/app.js"></script>
```

### Étape 2: Uploader index.html sur fjdaz.com

**Fichier source :** `/Users/francois-jeandazin/bergsonAndFriends/index.html`

**Destination :** `fjdaz.com/bergsonandfriends/index.html` (ou le chemin exact où se trouve le fichier sur votre serveur)

## 🚀 Méthodes d'Upload

### Option 1 : FTP/SFTP

```bash
# Exemple avec sftp
sftp user@fjdaz.com
cd bergsonandfriends  # ou le chemin exact
put /Users/francois-jeandazin/bergsonAndFriends/index.html index.html
exit
```

### Option 2 : SCP

```bash
scp /Users/francois-jeandazin/bergsonAndFriends/index.html user@fjdaz.com:/path/to/bergsonandfriends/index.html
```

### Option 3 : Interface Web (cPanel, Plesk, etc.)

1. Se connecter à l'interface d'administration
2. Naviguer vers le dossier où se trouve `index.html` (probablement `/bergsonandfriends/`)
3. Uploader le nouveau `index.html` (remplacer l'ancien)
4. Vérifier les permissions (lecture publique)

## ✅ Vérification

Après l'upload :

1. **Vider le cache du navigateur** :
   - Mac: `Cmd + Shift + R`
   - Windows: `Ctrl + Shift + R`

2. **Vérifier le fichier sur le serveur** :
   ```bash
   curl https://fjdaz.com/bergsonandfriends/index.html | grep app.js
   ```
   
   **Résultat attendu :**
   ```html
   <script src="https://fjdaz.com/bergson/statics/app.js"></script>
   ```

3. **Tester dans le navigateur** :
   - Ouvrir: `https://fjdaz.com/bergsonandfriends`
   - Console développeur (F12)
   - Vérifier qu'il n'y a plus d'erreur 404 pour `app.js`

## 🔍 Vérification du Chemin Exact

Si vous n'êtes pas sûr du chemin exact sur le serveur, vérifiez :

1. **Où se trouve actuellement index.html ?**
   - L'URL complète que vous utilisez : `https://fjdaz.com/bergsonandfriends`
   - Le fichier doit être dans le dossier correspondant

2. **Structure attendue sur le serveur :**
   ```
   fjdaz.com/
   └── bergsonandfriends/
       └── index.html  ← Ici
   └── bergson/
       └── statics/
           └── app.js  ← Déjà uploadé (vérifié)
   ```

## ⚠️ Notes Importantes

- **Cache navigateur** : Toujours vider le cache après un upload
- **Permissions** : Le fichier doit être lisible publiquement (chmod 644)
- **Backup** : Faire une copie de l'ancien `index.html` avant de le remplacer (au cas où)

---

**Dernière mise à jour :** 17 novembre 2025


