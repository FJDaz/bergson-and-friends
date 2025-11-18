# 🔧 Solution : Problème de Cache

## ✅ Action Effectuée

J'ai ajouté un paramètre de version dans `index.html` :

```html
<script src="https://fjdaz.com/bergson/statics/app.js?v=2"></script>
```

Cela forcera le navigateur à recharger le fichier même s'il y a un cache.

## 🔍 Vérifications à Faire

### 1. Vérifier le chemin exact sur le serveur

**Question importante :** Où avez-vous uploadé le fichier exactement ?

- `fjdaz.com/bergson/statics/app.js` ?
- Ou un autre chemin ?

### 2. Vérifier via SSH/FTP directement

Si vous avez accès SSH/FTP au serveur, vérifiez directement :

```bash
# Vérifier la taille
ls -lh /path/to/bergson/statics/app.js

# Vérifier le contenu (doit commencer par "// === CONFIGURATION API ===")
head -10 /path/to/bergson/statics/app.js
```

### 3. Vider le cache CDN (si applicable)

Si vous utilisez Cloudflare ou un autre CDN :
1. Aller dans le dashboard
2. Vider le cache pour `fjdaz.com/bergson/statics/app.js`
3. Ou purger tout le cache

### 4. Uploader index.html avec le paramètre v=2

Après avoir uploadé `index.html` avec `?v=2`, le navigateur forcera le rechargement.

## 📋 Checklist

- [ ] Vérifier le chemin exact où vous avez uploadé `app.js`
- [ ] Vérifier directement sur le serveur (SSH/FTP) que le fichier fait 13 Ko
- [ ] Vider le cache CDN si applicable
- [ ] Uploader `index.html` avec le paramètre `?v=2`
- [ ] Tester dans le navigateur avec cache vidé (Cmd+Shift+R)

## 🔍 Hash MD5 du Fichier Local

Pour vérifier que vous avez uploadé le bon fichier :

**Fichier local :**
- MD5 : `4a0233726fab81591d824d3eb82828c3`
- Taille : 13317 bytes
- Commence par : `// === CONFIGURATION API ===`

**Vérification sur serveur :**
```bash
# Si vous avez accès SSH
md5sum /path/to/bergson/statics/app.js
# Doit afficher : 4a0233726fab81591d824d3eb82828c3
```

---

**Dernière mise à jour :** 17 novembre 2025


