# Déploiement HF Space avec API REST

## Objectif
Déployer `app_with_api.py` sur le HF Space pour exposer une API REST vanilla (bypass Gradio) que Render peut appeler.

## Architecture finale
```
Frontend (fjdaz.com)
    ↓
Render (snb_api_hf.py) - GRATUIT
    ↓
HF Space (app_with_api.py) - $24/jour (déjà en cours)
    ↓
Qwen 2.5 14B + LoRA Spinoza
```

## Étapes de déploiement

### 1. Remplacer app.py sur le HF Space

Sur https://huggingface.co/spaces/FJDaz/bergsonAndFriends :

1. Aller dans **Files** > **app.py**
2. Cliquer sur **Edit**
3. **Remplacer tout le contenu** par le fichier `bergsonAndFriends_HF/app_with_api.py`
4. Commit avec message : "Add REST API endpoints (bypass Gradio)"

### 2. Vérifier les dépendances

Vérifier que le fichier `requirements.txt` du Space contient :
```txt
torch>=2.0.0
transformers>=4.35.0
peft>=0.7.0
bitsandbytes>=0.41.0
accelerate>=0.24.0
gradio>=4.0.0
fastapi>=0.104.0
uvicorn>=0.24.0
```

Si manquant, ajouter `fastapi` et `uvicorn`.

### 3. Attendre le rebuild

Le Space va automatiquement rebuild. Cela prend **5-10 minutes**.

### 4. Tester l'API REST

Une fois le Space démarré :

```bash
# Test health endpoint
curl https://fjdaz-bergsonandfriends.hf.space/health | python3 -m json.tool

# Test chat endpoint
curl -X POST https://fjdaz-bergsonandfriends.hf.space/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bonjour Spinoza",
    "history": []
  }' | python3 -m json.tool
```

**Résultat attendu :**
```json
{
  "reply": "Bonjour ! Je suis Spinoza...",
  "history": [["Bonjour Spinoza", "Bonjour ! Je suis Spinoza..."]],
  "contexte": "neutre"
}
```

### 5. Render auto-redeploy

Render détecte automatiquement le Procfile et redéploie avec `snb_api_hf.py`.

Vérifier sur https://bergson-and-friends.onrender.com/health :
```json
{
  "status": "ok",
  "mode": "hf_space_http",
  "space_url": "https://fjdaz-bergsonandfriends.hf.space",
  "space_status": "connected"
}
```

### 6. Test end-to-end

Frontend → Render → HF Space :

```bash
curl -X POST https://bergson-and-friends.onrender.com/chat/spinoza \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Qu'\''est-ce que la liberté ?",
    "history": [],
    "philosopher": "spinoza"
  }' | python3 -m json.tool
```

## Avantages de cette solution

✅ **Déployable** : API REST simple, pas de gradio_client complexe
✅ **Maintenable** : Code clair, debuggable
✅ **Compatible** : Fonctionne avec l'architecture existante
✅ **POC intact** : Interface Gradio toujours disponible sur le Space

## Coûts

- **Render** : Gratuit (free tier)
- **HF Space** : ~$24/jour (GPU L4, déjà en cours)
- **Total** : $24/jour

## Troubleshooting

### Space ne démarre pas
- Vérifier les logs HF Space
- S'assurer que `HF_TOKEN` est défini dans les secrets du Space

### API 404
- Vérifier que `app_with_api.py` est bien utilisé (pas `app.py`)
- Redémarrer le Space

### Timeout Render → Space
- Le cold start du Space peut prendre 30-60s
- Augmenter le timeout dans `snb_api_hf.py` si nécessaire

### "Model loading"
- Le modèle 14B + 8-bit prend 2-3 minutes à charger
- Attendre que `/health` retourne `"model_loaded": true`
