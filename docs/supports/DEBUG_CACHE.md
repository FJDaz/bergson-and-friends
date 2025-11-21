# 🔍 Debug : Problème de Cache ou Chemin

## ❌ Problème

Vous avez uploadé le fichier (13 Ko), mais `curl` récupère toujours l'ancienne version (19015 bytes).

## 🔍 Vérifications

### 1. Vérifier le chemin exact sur le serveur

**Question :** Où avez-vous uploadé le fichier exactement ?

- `fjdaz.com/bergson/statics/app.js` ?
- `fjdaz.com/bergsonandfriends/statics/app.js` ?
- Un autre chemin ?

### 2. Vérifier s'il y a plusieurs copies

Il pourrait y avoir plusieurs copies du fichier :
- Une dans `/bergson/statics/`
- Une dans `/bergsonandfriends/statics/`
- Une autre ailleurs

### 3. Vérifier le cache serveur

Si vous utilisez un CDN ou un cache serveur (Cloudflare, etc.), il faut :
- Vider le cache du CDN
- Ou attendre l'expiration du cache
- Ou utiliser un paramètre de version : `app.js?v=2`

### 4. Vérifier les permissions

Le fichier doit être :
- Lisible publiquement (chmod 644)
- Accessible via HTTP

## 🔧 Solutions

### Solution 1 : Vérifier le chemin exact

Dans votre interface d'upload, vérifiez le chemin exact où vous avez uploadé le fichier.

### Solution 2 : Vider le cache serveur

Si vous utilisez un CDN (Cloudflare, etc.) :
1. Aller dans le dashboard du CDN
2. Vider le cache pour `fjdaz.com/bergson/statics/app.js`
3. Ou purger tout le cache

### Solution 3 : Ajouter un paramètre de version

Dans `index.html`, changer :
```html
<script src="https://fjdaz.com/bergson/statics/app.js"></script>
```

En :
```html
<script src="https://fjdaz.com/bergson/statics/app.js?v=2"></script>
```

Cela forcera le navigateur à recharger le fichier.

### Solution 4 : Vérifier via FTP/SFTP directement

Se connecter directement au serveur et vérifier :
```bash
# Vérifier la taille
ls -lh /path/to/bergson/statics/app.js

# Vérifier le contenu
head -15 /path/to/bergson/statics/app.js
```

## 📋 Questions à Répondre

1. **Quel est le chemin exact** où vous avez uploadé le fichier ?
2. **Utilisez-vous un CDN** (Cloudflare, etc.) ?
3. **Quelle méthode d'upload** avez-vous utilisée (FTP, SFTP, interface web) ?
4. **Pouvez-vous vérifier directement** sur le serveur (via SSH/FTP) que le fichier fait bien 13 Ko ?

---

**Dernière mise à jour :** 17 novembre 2025


