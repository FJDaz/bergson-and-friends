# 🚀 Déploiement Netlify + Hugging Face + FJDAZ.com

Guide complet pour déployer **Bergson and Friends** sur l'architecture Netlify + Hugging Face API.

---

## 📋 Architecture du Projet

```
┌─────────────────────┐
│   FJDAZ.com         │  ← Domaine custom
│   (via Netlify)     │
└──────────┬──────────┘
           │
           ├─── Frontend (index.html + static/)
           │
           ├─── Netlify Functions (API)
           │    ├── spinoza.js  → Hugging Face Space
           │    ├── bergson.js  → Together AI / Mock
           │    └── kant.js     → Together AI / Mock
           │
           └─── Hugging Face Space
                └── FJDaz/bergsonAndFriends
                    └── Modèle Spinoza fine-tuné (Qwen2.5-14B)
```

---

## ✅ Prérequis

1. **Compte Netlify** : [https://app.netlify.com/signup](https://app.netlify.com/signup)
2. **Compte Hugging Face** : [https://huggingface.co/join](https://huggingface.co/join)
3. **Token Hugging Face** : [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) (avec accès lecture)
4. **Compte Together AI** (optionnel) : [https://api.together.xyz/](https://api.together.xyz/)
5. **Repository Git** : Ce projet sur GitHub

---

## 🔧 Étape 1 : Préparer le Hugging Face Space

### 1.1 Vérifier que votre Space est actif

Votre Space **FJDaz/bergsonAndFriends** doit être :
- ✅ Public ou avec token d'accès
- ✅ Status : Running (pas Sleep)
- ✅ SDK : Gradio
- ✅ Endpoint actif : `https://huggingface.co/spaces/FJDaz/bergsonAndFriends`

### 1.2 Tester le Space manuellement

```bash
# Test local avec curl
curl -X POST \
  https://fjdaz-bergsonandfriends.hf.space/call/chat_function \
  -H "Content-Type: application/json" \
  -d '{"data": ["Bonjour Spinoza", []]}'
```

---

## 🌐 Étape 2 : Déployer sur Netlify

### 2.1 Méthode 1 : Import depuis GitHub (Recommandé)

1. Connectez-vous à [Netlify](https://app.netlify.com/)
2. Cliquez sur **"Add new site"** → **"Import an existing project"**
3. Sélectionnez **GitHub** et autorisez l'accès
4. Choisissez le repository **bergson-and-friends**
5. Configuration du build :
   ```
   Build command: (laissez vide)
   Publish directory: .
   Functions directory: netlify/functions
   ```
6. Cliquez sur **"Deploy site"**

### 2.2 Méthode 2 : Netlify CLI

```bash
# Installer Netlify CLI
npm install -g netlify-cli

# Se connecter à Netlify
netlify login

# Initialiser le site
netlify init

# Déployer
netlify deploy --prod
```

---

## 🔑 Étape 3 : Configurer les Variables d'Environnement

### 3.1 Sur Netlify (Production)

1. Allez dans votre site Netlify
2. **Site settings** → **Environment variables**
3. Ajoutez les variables suivantes :

| Variable | Valeur | Obligatoire |
|----------|--------|-------------|
| `HF_TOKEN` | Votre token Hugging Face | ✅ OUI |
| `TOGETHER_API_KEY` | Votre clé Together AI | ⚠️ Optionnel* |

> *Si `TOGETHER_API_KEY` n'est pas fournie, Bergson et Kant utiliseront des réponses mock/fallback

### 3.2 Pour le Développement Local

```bash
# Créer un fichier .env
cp .env.example .env

# Éditer le fichier .env avec vos vraies clés
nano .env
```

Contenu du `.env` :
```bash
HF_TOKEN=hf_VotreTrueTokenIci
TOGETHER_API_KEY=your_together_key_here  # Optionnel
```

**⚠️ Important :** Ajoutez `.env` au `.gitignore` pour ne pas commit vos clés !

---

## 🌍 Étape 4 : Configurer le Domaine FJDAZ.com

### 4.1 Dans Netlify

1. Allez dans **Site settings** → **Domain management**
2. Cliquez sur **"Add custom domain"**
3. Entrez : `bergson.fjdaz.com` (ou le sous-domaine de votre choix)
4. Netlify vous donnera des instructions DNS

### 4.2 Dans votre DNS Provider (ex: OVH, Cloudflare, etc.)

Ajoutez un enregistrement CNAME :

```
Type: CNAME
Nom: bergson (ou @)
Valeur: votre-site.netlify.app
TTL: Automatique
```

### 4.3 Activer HTTPS

Netlify active automatiquement Let's Encrypt SSL. Patientez 2-5 minutes après la configuration DNS.

---

## 🧪 Étape 5 : Tester le Déploiement

### Test 1 : Frontend

Visitez : `https://votre-site.netlify.app` (ou votre domaine custom)

Vous devriez voir l'interface avec les 3 philosophes.

### Test 2 : Fonction Spinoza (Hugging Face)

```bash
curl -X POST https://votre-site.netlify.app/.netlify/functions/spinoza \
  -H "Content-Type: application/json" \
  -d '{"question": "La liberté est-elle une illusion ?"}'
```

Réponse attendue :
```json
{
  "philosopher": "Spinoza",
  "answer": "...",
  "timestamp": "2025-...",
  "source": "huggingface_space"
}
```

### Test 3 : Fonction Bergson (Together AI)

```bash
curl -X POST https://votre-site.netlify.app/.netlify/functions/bergson \
  -H "Content-Type: application/json" \
  -d '{"question": "Qu'\''est-ce que la durée ?"}'
```

### Test 4 : Fonction Kant (Together AI)

```bash
curl -X POST https://votre-site.netlify.app/.netlify/functions/kant \
  -H "Content-Type: application/json" \
  -d '{"question": "Qu'\''est-ce que l'\''impératif catégorique ?"}'
```

---

## 📊 Monitoring et Logs

### Logs Netlify Functions

1. Dans Netlify : **Functions** → Sélectionnez une fonction
2. Consultez les logs en temps réel
3. Vérifiez les erreurs et temps de réponse

### Logs Hugging Face Space

1. Allez sur [https://huggingface.co/spaces/FJDaz/bergsonAndFriends](https://huggingface.co/spaces/FJDaz/bergsonAndFriends)
2. Onglet **"Logs"** pour voir les appels API
3. Surveillez le status (Running / Sleep)

---

## ⚠️ Problèmes Courants

### 1. Spinoza répond "Je suis en train de me réveiller"

**Cause** : Le Hugging Face Space est en mode Sleep (inactivité > 48h)

**Solution** :
- Patientez 30-60 secondes, le Space va se réveiller automatiquement
- Ou : Allez manuellement sur le Space pour le réveiller
- Ou : Configurez un "ping" automatique toutes les heures

### 2. Bergson/Kant répondent avec des messages mock

**Cause** : `TOGETHER_API_KEY` non configurée

**Solution** :
- Ajoutez la clé dans les variables d'environnement Netlify
- Ou : Utilisez les réponses mock (c'est normal si vous n'avez pas de clé)

### 3. CORS Errors

**Cause** : Headers CORS manquants

**Solution** :
- Vérifiez que `netlify.toml` est présent
- Les fonctions incluent déjà les headers CORS dans le code

### 4. CSS ne se charge pas

**Cause** : Chemins CSS pointent vers `https://fjdaz.com/bergson/statics/`

**Solution** :
- Vérifiez que les ressources sont bien hébergées sur FJDAZ.com
- Ou : Modifiez `index.html` pour utiliser des chemins relatifs (`./static/`)

---

## 🚀 Optimisations Futures

### 1. Empêcher le Sleep du Space HF

**Option A** : Upgrade vers un Space persistant (payant)

**Option B** : Créer un cron job qui ping le Space toutes les heures

```js
// netlify/functions/keep-alive.js
exports.handler = async () => {
  await fetch('https://fjdaz-bergsonandfriends.hf.space/', {
    method: 'GET'
  });
  return { statusCode: 200 };
};
```

Puis configurez un cron sur Netlify ou Uptime Robot.

### 2. Ajouter un Cache Layer

Utiliser Netlify Edge Functions + KV store pour cacher les réponses fréquentes.

### 3. Migrer Bergson/Kant vers Hugging Face

Créer des Spaces séparés pour chaque philosophe, tous hébergés sur HF.

---

## 📞 Support

- **Netlify Docs** : [https://docs.netlify.com/](https://docs.netlify.com/)
- **Hugging Face Spaces** : [https://huggingface.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces)
- **Gradio Client** : [https://www.gradio.app/guides/getting-started-with-the-python-client](https://www.gradio.app/guides/getting-started-with-the-python-client)

---

## ✅ Checklist Finale

- [ ] Space HF actif et accessible
- [ ] Token HF créé et configuré dans Netlify
- [ ] Site déployé sur Netlify
- [ ] Variables d'environnement configurées
- [ ] Domaine custom configuré (optionnel)
- [ ] HTTPS activé
- [ ] Tests des 3 philosophes réussis
- [ ] Monitoring configuré

**🎉 Votre projet est maintenant live sur Netlify + Hugging Face + FJDAZ.com !**
