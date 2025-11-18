# Status Netlify → HF Space - 18 Novembre 2025

## Problème Identifié

### Netlify Functions Timeout

**Limite :** 10 secondes (free tier)
**Temps nécessaire :** HF Space connection + Qwen 14B génération = ~15-30 secondes

**Erreur :**
```json
{
  "errorType": "Runtime.NodeJsExit",
  "errorMessage": "Promise that was never settled"
}
```

## Tests Effectués

### ✅ Test 1 : Endpoint `/init`
```bash
curl -X POST https://chimerical-kashata-65179e.netlify.app/.netlify/functions/spinoza_hf \
  -d '{"action":"init"}'
```

**Résultat :** ✅ Succès (instantané, pas de HF Space)

```json
{
  "question": "Suis-je esclave de mes désirs ?",
  "greeting": "Bonjour ! Je suis Spinoza.\n\n**Suis-je esclave de mes désirs ?**\n\nQu'en penses-tu ?",
  "history": [...]
}
```

### ❌ Test 2 : Endpoint `/chat` (HF Space)
```bash
curl -X POST https://chimerical-kashata-65179e.netlify.app/.netlify/functions/spinoza_hf \
  -d '{"action":"chat","message":"Bonjour Spinoza","history":[]}'
```

**Résultat :** ❌ Timeout après ~10 secondes

**Raison :**
- Connection au HF Space via `@gradio/client`
- Appel au modèle Qwen 14B (génération ~5-10s)
- Total : > 10 secondes (limite Netlify gratuit)

## HF Space Status

**URL :** https://fjdaz-bergsonandfriends.hf.space
**Status :** ✅ En ligne (retourne HTML Gradio)
**Modèle :** Qwen 2.5 14B + LoRA Spinoza
**GPU :** A10G (24GB VRAM)
**Coût :** ~$1/heure

## Solutions Possibles

### Option A : Netlify Pro (Upgrade)
- **Timeout :** 26 secondes (Background Functions: 10 minutes)
- **Coût :** $19/mois
- **Problème :** Coût supplémentaire

### Option B : Railway Backend (déjà testé)
- **Pro :** Pas de limite timeout stricte
- **Contre :** A crash lors du dernier test (problème `python` vs `python3`)
- **Statut :** Échec (erreur "python: command not found")

### Option C : Alternative - Appel HTTP Direct
Au lieu d'utiliser `@gradio/client`, faire un appel HTTP direct à l'API Gradio :
```javascript
POST https://fjdaz-bergsonandfriends.hf.space/call/chat_function
```
**Problème potentiel :** API Gradio peut aussi prendre >10s pour générer

### Option D : Mock + RAG Seulement (Actuel)
- **Pro :** 0€, fonctionne instantanément
- **Contre :** Pas de vraies générations IA
- **Frontend :** https://fjdaz.com/bergson/index_spinoza.html
- **Backend :** https://bergson-api-production.up.railway.app (Mock mode)

### Option E : Vercel Functions (Alternative à Netlify)
- **Timeout :** 10s (Hobby), 60s (Pro), 300s (Enterprise)
- **Coût :** Gratuit (Hobby), $20/mois (Pro)
- **Migration :** Nécessiterait redéploiement complet

## Recommandation

### Court Terme (Maintenant)
**Rester sur Mock + RAG** :
- ✅ Fonctionne (confirmé par user: "It's a win!")
- ✅ 0€
- ✅ Instantané
- ⚠️ Réponses limitées (5-6 mocks par philosophe)

**Mettre HF Space en pause** :
- Économiser ~$24/jour
- Réactiver seulement si solution timeout trouvée

### Moyen Terme
**Tester Railway avec fix Python** :
- Créer `nixpacks.toml` pour forcer Python 3.11
- OU utiliser variable d'env `NIXPACKS_PYTHON_VERSION=3.11`
- Redéployer `snb_api_hf.py` sur Railway

### Long Terme
**Si budget disponible :**
- **Option 1 :** Netlify Pro ($19/mois) → 26s timeout
- **Option 2 :** Vercel Pro ($20/mois) → 60s timeout
- **Option 3 :** Railway seul (gratuit) + fix config Python

## Code Actif

### Frontend (Netlify)
- ✅ `index_spinoza.html` → Pointe vers Railway Mock
- ⚠️ `index_spinoza_netlify.html` → Pointe vers Netlify Function (timeout)

### Backend Railway
- ✅ `snb_api_mock.py` → Déployé, fonctionne (Mock + RAG)
- ⚠️ `snb_api_hf.py` → Code prêt, échec déploiement

### Netlify Function
- ✅ `spinoza_hf.js` → Init fonctionne
- ❌ `spinoza_hf.js` → Chat timeout (HF Space)

## Prochaines Actions

1. **Décision HF Space** : Pause ou garder actif ?
2. **Railway fix** : Tester `nixpacks.toml` pour Python 3.11
3. **Si Railway OK** : Déployer `snb_api_hf.py`
4. **Si Railway KO** : Rester sur Mock + RAG (0€)

---

**Conclusion :** Système Mock + RAG fonctionne. Intégration HF Space bloquée par timeouts (Netlify 10s, Railway crash Python). Solution à 0€ disponible, intégration IA nécessite fix infrastructure ou upgrade payant.
