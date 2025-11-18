# ⚠️ Problème : Fichier Uploadé Incomplet

## ❌ Problème Détecté

Le fichier `app-v2.js` sur le serveur ne fait que **196 bytes** au lieu de **13 Ko**.

**Vérification :**
```bash
curl https://fjdaz.com/bergson/statics/app-v2.js | wc -c
# Résultat : 196 bytes (au lieu de 13317 bytes)
```

**Conclusion :** Le fichier uploadé est **incomplet ou corrompu**.

## 🔍 Causes Possibles

1. **Upload interrompu** (connexion coupée)
2. **Problème de permissions** (fichier tronqué)
3. **Erreur lors de l'upload** (fichier partiel)
4. **Problème de format** (binaire vs texte)

## ✅ Solution

### 1. Vérifier le Fichier Local

Le fichier local doit faire **13317 bytes** :
```bash
wc -c static/app-v2.js
# Doit afficher : 13317
```

### 2. Ré-uploader le Fichier

**Méthode recommandée :**

#### Option A : SCP (si SSH disponible)
```bash
scp /Users/francois-jeandazin/bergsonAndFriends/static/app-v2.js user@fjdaz.com:/path/to/bergson/statics/app-v2.js
```

#### Option B : SFTP
```bash
sftp user@fjdaz.com
cd bergson/statics
put /Users/francois-jeandazin/bergsonAndFriends/static/app-v2.js app-v2.js
exit
```

#### Option C : Interface Web (cPanel/Plesk)
1. Se connecter à l'interface
2. Naviguer vers `/bergson/statics/`
3. **Supprimer** l'ancien `app-v2.js` (196 bytes)
4. **Uploader** le nouveau `app-v2.js` (13 Ko)
5. Vérifier que la taille est correcte après upload

### 3. Vérifier Après Upload

```bash
# Vérifier la taille
curl -I https://fjdaz.com/bergson/statics/app-v2.js | grep -i content-length
# Doit afficher : Content-Length: 13317

# Vérifier le contenu
curl https://fjdaz.com/bergson/statics/app-v2.js | grep -A 2 "API_BASE_URL"
# Doit afficher la configuration API_BASE_URL
```

## 📋 Checklist

- [ ] Vérifier que le fichier local fait bien 13317 bytes
- [ ] Supprimer l'ancien `app-v2.js` sur le serveur (196 bytes)
- [ ] Ré-uploader `app-v2.js` (13 Ko)
- [ ] Vérifier la taille après upload (doit être 13317 bytes)
- [ ] Vérifier que `API_BASE_URL` est présent
- [ ] Tester sur `https://fjdaz.com/bergsonandfriends`

## 🔍 Vérification du Fichier Local

**Fichier correct :**
- Chemin : `/Users/francois-jeandazin/bergsonAndFriends/static/app-v2.js`
- Taille : 13317 bytes
- MD5 : `4a0233726fab81591d824d3eb82828c3`
- Commence par : `// === CONFIGURATION API ===`

---

**Dernière mise à jour :** 17 novembre 2025


