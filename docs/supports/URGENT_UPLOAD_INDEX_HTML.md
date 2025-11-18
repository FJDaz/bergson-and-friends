# 🚨 URGENT : Uploader index.html sur fjdaz.com

## ❌ Problème Actuel

**Erreur console :**
```
GET https://fjdaz.com/static/app.js net::ERR_ABORTED 404 (Not Found)
```

**Cause :** Le fichier `index.html` sur le serveur `fjdaz.com` utilise encore l'ancien chemin `/static/app.js` au lieu de `https://fjdaz.com/bergson/statics/app.js`.

**Vérification :**
```bash
curl https://fjdaz.com/bergsonandfriends/index.html | grep app.js
# Résultat actuel (INCORRECT) :
# <script src="/static/app.js"></script>
```

## ✅ Solution

### Fichier à Uploader

**Source (local, CORRIGÉ) :**
- Chemin : `/Users/francois-jeandazin/bergsonAndFriends/index.html`
- Ligne 150 : `<script src="https://fjdaz.com/bergson/statics/app.js"></script>` ✅

**Destination (serveur) :**
- Chemin : `fjdaz.com/bergsonandfriends/index.html`
- Remplacez l'ancien fichier

### Méthode Rapide (SCP)

```bash
scp /Users/francois-jeandazin/bergsonAndFriends/index.html user@fjdaz.com:/path/to/bergsonandfriends/index.html
```

### Méthode FTP/SFTP

```bash
sftp user@fjdaz.com
cd bergsonandfriends
put /Users/francois-jeandazin/bergsonAndFriends/index.html index.html
exit
```

### Interface Web (cPanel/Plesk)

1. Connectez-vous à l'interface d'administration
2. Naviguez vers `/bergsonandfriends/`
3. Uploader le nouveau `index.html` (remplacer l'ancien)

## ✅ Vérification Après Upload

1. **Vider le cache navigateur** : `Cmd+Shift+R` (Mac) ou `Ctrl+Shift+R` (Windows)

2. **Vérifier le fichier sur le serveur** :
   ```bash
   curl https://fjdaz.com/bergsonandfriends/index.html | grep app.js
   ```
   
   **Résultat attendu (CORRECT) :**
   ```html
   <script src="https://fjdaz.com/bergson/statics/app.js"></script>
   ```

3. **Tester dans le navigateur** :
   - Ouvrir : `https://fjdaz.com/bergsonandfriends`
   - Console développeur (F12)
   - Vérifier qu'il n'y a **plus d'erreur 404** pour `app.js`

## 📋 Checklist

- [ ] Uploader `index.html` corrigé sur `fjdaz.com/bergsonandfriends/index.html`
- [ ] Vider le cache navigateur
- [ ] Vérifier que le chemin dans le fichier serveur est correct
- [ ] Tester depuis `https://fjdaz.com/bergsonandfriends`
- [ ] Vérifier qu'il n'y a plus d'erreur 404 dans la console

---

**Guide détaillé :** Voir `GUIDE_UPLOAD_INDEX_HTML.md`

**Dernière mise à jour :** 17 novembre 2025


