# Configuration Modal pour Spinoza Chatbot

## Option 1 : Script automatique (recommandé)

```bash
./setup_modal.sh
```

Le script vous guidera à travers :
1. Authentification Modal (ouvre le navigateur)
2. Vérification des secrets existants
3. Création du secret `hf-token` si nécessaire

---

## Option 2 : Commandes manuelles

### Étape 1 : Authentification Modal

```bash
modal token new
```

Cela ouvre votre navigateur pour vous connecter à Modal Labs.

### Étape 2 : Vérifier les secrets existants

```bash
modal secret list
```

Si vous voyez `hf-token` dans la liste, passez à l'étape 4 (test).

### Étape 3 : Créer le secret HF_TOKEN

**Option A : Interactive**
```bash
modal secret create hf-token
# Puis entrez : HF_TOKEN=hf_votre_token
# Tapez Ctrl+D pour terminer
```

**Option B : En une ligne**
```bash
modal secret create hf-token HF_TOKEN=hf_votre_token_ici
```

### Étape 4 : Tester l'application

```bash
modal run modal_spinoza.py --question "La liberté est-elle une illusion ?"
```

**Note** : Le premier run télécharge ~14GB de modèles (Qwen 14B + LoRA).
Cela prend 5-10 minutes mais les modèles sont ensuite cachés.

### Étape 5 : Déployer

```bash
modal deploy modal_spinoza.py
```

Vous obtiendrez une URL comme :
```
https://fjdaz--spinoza-chatbot-fastapi-app.modal.run
```

---

## Où trouver votre HF_TOKEN

1. **Hugging Face** : https://huggingface.co/settings/tokens
   - Créer un nouveau token avec permissions `Read` si nécessaire

2. **Netlify Dashboard** :
   - Site settings → Environment variables
   - Chercher `HF_TOKEN`

3. **Dans votre code local** (si configuré) :
   ```bash
   cat ~/.huggingface/token
   ```

---

## Vérification

Une fois configuré, vérifiez que tout fonctionne :

```bash
# Test du secret
modal secret list | grep hf-token

# Test de l'app (remote)
modal run modal_spinoza.py --question "Test"
```

---

## Troubleshooting

### Erreur : "Secret 'hf-token' not found"

Le secret n'existe pas. Créez-le avec l'étape 3.

### Erreur : "Token missing. Could not authenticate client"

Vous n'êtes pas authentifié. Exécutez `modal token new`.

### Erreur lors du téléchargement des modèles

Vérifiez que votre HF_TOKEN est valide :
```bash
curl -H "Authorization: Bearer hf_votre_token" \
  https://huggingface.co/api/whoami
```

Si erreur, créez un nouveau token sur Hugging Face.

---

## Architecture Modal

```
┌─────────────────────────────────────────────┐
│  FastAPI Endpoint (fastapi_app)             │
│  URL: https://xxx.modal.run                 │
│  POST /chat_spinoza                         │
│  GET /health                                │
└────────────────┬────────────────────────────┘
                 │
                 │ appelle .remote()
                 ▼
┌─────────────────────────────────────────────┐
│  SpinozaService (GPU A10G)                  │
│  - Charge Qwen 14B + LoRA (8-bit)          │
│  - Détection contextuelle V2                │
│  - Génération de réponse                    │
│  Secret: hf-token (HF_TOKEN)                │
│  Volume: spinoza-models (cache)             │
└─────────────────────────────────────────────┘
```
