# ✅ Actions Restantes - 17 Novembre 2025

## 🎯 Objectif
Configurer un système fonctionnel pour le 26 novembre : **Bergson and Friends** avec RAG + SNB pour 3 philosophes.

---

## ✅ Actions Complétées

1. **✅ index.html corrigé et committé**
   - Chemin `app.js` corrigé vers `https://fjdaz.com/bergson/statics/app.js`
   - Commit: `Fix app.js path: use absolute URL to fjdaz.com/bergson/statics/app.js`

2. **✅ Documentation créée**
   - `GUIDE_UPLOAD_APP_JS.md` - Guide pour uploader app.js
   - `scripts/test_space_connection.js` - Script de test pour vérifier la connexion au Space HF

---

## ⚠️ Actions Urgentes (À Faire Maintenant)

### 1. Uploader `app.js` sur fjdaz.com ⚠️ CRITIQUE

**Fichier :** `/Users/francois-jeandazin/bergsonAndFriends/static/app.js`

**Destination :** `fjdaz.com/bergson/statics/app.js`

**Guide :** Voir `GUIDE_UPLOAD_APP_JS.md`

**Vérification :**
```bash
curl -I https://fjdaz.com/bergson/statics/app.js
# Doit retourner: 200 OK
```

**Impact :** Sans cet upload, le frontend ne peut pas charger le JavaScript.

---

### 2. Vérifier les Variables d'Environnement Netlify ⚠️ IMPORTANT

**Dashboard Netlify → Site settings → Environment variables**

Vérifier que :
- `USE_MOCK` n'est **PAS** défini ou est `false`
- `SNB_BACKEND_URL` est vide (utilise le défaut) ou pointe vers `https://fjdaz-bergsonandfriends.hf.space`

**Comment vérifier :**
1. Aller sur Netlify Dashboard
2. Sélectionner le site
3. Settings → Environment variables
4. Vérifier les valeurs

**Impact :** Si `USE_MOCK=true`, le système utilisera toujours les réponses mock au lieu du Space HF.

---

### 3. Tester le Flux Complet

**Étapes :**
1. Uploader `app.js` (action 1)
2. Vérifier variables Netlify (action 2)
3. Tester depuis `https://fjdaz.com/bergsonandfriends`
4. Ouvrir la console développeur (F12)
5. Poser une question à un philosophe
6. Vérifier que la réponse vient du Space HF (pas du mock)

**Script de test local :**
```bash
node scripts/test_space_connection.js
```

**Impact :** Permet de détecter les problèmes avant le 26 novembre.

---

## 📋 Actions pour le 26 Novembre

### 4. Tester avec les 3 Philosophes

- [ ] Tester Spinoza
- [ ] Tester Bergson
- [ ] Tester Kant
- [ ] Vérifier que chaque philosophe a son style distinct
- [ ] Vérifier que le RAG fonctionne (concepts extraits)

### 5. Vérifier les Logs Netlify

**Dashboard Netlify → Functions → philosopher_rag → Logs**

Chercher :
- `[SNB]` - Logs de connexion au Space
- `[RAG]` - Logs du système RAG
- `[SNB Error]` - Erreurs de connexion
- `[RAG] Erreur SNB` - Erreurs lors de l'appel SNB

**Si erreurs :**
- Vérifier que le Space `bergsonAndFriends` tourne
- Vérifier l'URL dans les logs
- Vérifier le timeout (10s sur plan free Netlify)

### 6. Plan de Repli (Si Problème HF)

**Guide :** Voir `REPLI_RUNPOD.md`

**Temps estimé :** 25-30 minutes

**Actions :**
1. Créer compte RunPod (si pas déjà fait)
2. Déployer template Docker
3. Attendre chargement modèle (5-10 min)
4. Tester l'endpoint
5. Mettre à jour `SNB_BACKEND_URL` sur Netlify
6. Redéployer Netlify

---

## 🔍 Points de Debug

### Si fallback mock persiste

1. **Vérifier `USE_MOCK`** dans Netlify (doit être `false` ou non défini)
2. **Consulter logs Netlify** pour erreur exacte
3. **Tester `@gradio/client`** localement :
   ```bash
   node scripts/test_space_connection.js
   ```
4. **Vérifier que le Space répond** :
   ```bash
   curl https://fjdaz-bergsonandfriends.hf.space/gradio_api/info
   ```

### Si `app.js` ne charge pas

1. **Vérifier upload** sur fjdaz.com : `https://fjdaz.com/bergson/statics/app.js`
2. **Vérifier permissions** du fichier (readable)
3. **Vérifier cache navigateur** (hard refresh : Cmd+Shift+R)
4. **Vérifier console navigateur** pour erreurs CORS ou 404

### Si timeout Netlify

- **Limite :** 10s sur plan free Netlify
- **Solution :** Le Space HF peut prendre 30-60s au cold start
- **Workaround :** Garder le Space actif (éviter le cold start)
- **Alternative :** Passer au plan Pro Netlify (26s timeout) ou utiliser RunPod

---

## 🔗 URLs Importantes

- **Space HF :** https://fjdaz-bergsonandfriends.hf.space
- **API Info :** https://fjdaz-bergsonandfriends.hf.space/gradio_api/info
- **Frontend :** https://fjdaz.com/bergsonandfriends
- **Netlify Dashboard :** https://app.netlify.com → Site → Functions → Logs

---

## 📝 Checklist Finale (Avant le 26 Novembre)

- [ ] `app.js` uploadé sur fjdaz.com
- [ ] `index.html` poussé sur le repo (✅ fait)
- [ ] Variables Netlify vérifiées (`USE_MOCK=false`, `SNB_BACKEND_URL` correct)
- [ ] Test du flux complet depuis fjdaz.com/bergsonandfriends
- [ ] Test avec les 3 philosophes
- [ ] Logs Netlify vérifiés (pas d'erreurs)
- [ ] Plan de repli RunPod préparé (optionnel mais recommandé)

---

**Dernière mise à jour :** 17 novembre 2025 - Après commit index.html

