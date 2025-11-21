# ✅ Fix : Remplacement de @gradio/client par API HTTP Directe

## ❌ Problème Identifié

**Erreur dans les logs Netlify :**
```
[SNB Error]: Cannot read properties of undefined (reading 'connect')
```

**Cause :** `@gradio/client` nécessite un environnement navigateur et ne fonctionne pas dans Netlify Functions (environnement Node.js).

## ✅ Solution Appliquée

Remplacement de `@gradio/client` par un appel HTTP direct à l'API Gradio.

### Changements

**Avant :**
```javascript
const { Client } = await import("@gradio/client");
const client = await Client.connect(SPACE_URL);
const result = await client.predict("/chat_function", {...});
```

**Après :**
```javascript
const https = require('https');
const url = new URL(SPACE_URL);

const payload = JSON.stringify({
    data: [enrichedMessage, []],
    fn_index: 0,
    session_hash: Math.random().toString(36).substring(2, 15)
});

const result = await new Promise((resolve, reject) => {
    const req = https.request({
        hostname: url.hostname,
        port: 443,
        path: '/gradio_api/call/chat_function',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(payload)
        },
        timeout: 60000
    }, (res) => {
        // ... traitement de la réponse
    });
    // ...
});
```

## 📋 Prochaines Étapes

1. **Redéployer sur Netlify**
   - Le code est committé
   - Netlify devrait redéployer automatiquement
   - OU déclencher un déploiement manuel

2. **Tester**
   - Aller sur `https://chimerical-kashata-65179e.netlify.app/`
   - Poser une question à un philosophe
   - Vérifier que la réponse vient du Space HF (pas du mock)

3. **Vérifier les logs**
   - Netlify Dashboard → Functions → `philosopher_rag` → Logs
   - Chercher : `[SNB] Using direct HTTP API`
   - Chercher : `[SNB] Response extracted` (succès)
   - OU : `[SNB Error]` (erreur)

## ⚠️ Note sur le Timeout

**Netlify Free :** Timeout de 10s
**Space HF :** Peut prendre 30-60s au cold start

**Solution :**
- Garder le Space actif (éviter le cold start)
- OU passer au plan Pro Netlify (26s timeout)
- OU utiliser RunPod (voir `REPLI_RUNPOD.md`)

## 🔍 Format de Réponse Attendu

L'API Gradio retourne :
```json
{
  "data": [
    "text_response",
    [
      ["user_message", "assistant_response"]
    ]
  ]
}
```

Le code extrait `data[1][last][1]` (dernière réponse de l'assistant).

---

**Commit :** `ce3e14c` - "Fix: Replace @gradio/client with direct HTTP API for Node.js compatibility"
**Date :** 17 novembre 2025


