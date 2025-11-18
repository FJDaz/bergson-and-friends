# 🔧 Fix : Désactiver le Mock sur Netlify

## ❌ Problème

Le système renvoie toujours la même réponse mock au lieu d'appeler le Space HF.

**Réponse mock Spinoza :**
> "Écoute. Tout a une cause nécessaire. La liberté n'est pas le libre arbitre, mais la connaissance de cette nécessité. Plus tu comprends les causes qui te déterminent, plus tu es libre. C'est paradoxal mais rigoureux."

## 🔍 Causes Possibles

### 1. Variable `USE_MOCK=true` dans Netlify

**Vérification :**
1. Aller sur **Netlify Dashboard**
2. Sélectionner le site : `chimerical-kashata-65179e`
3. **Site settings** → **Environment variables**
4. Chercher `USE_MOCK`

**Si `USE_MOCK=true` existe :**
- **Action :** Le supprimer ou le mettre à `false`

### 2. Erreur lors de l'appel au Space HF

**Vérification :**
1. **Netlify Dashboard** → **Functions** → `philosopher_rag` → **Logs**
2. Chercher : `[RAG] Erreur SNB, fallback mock`
3. Vérifier l'erreur exacte

**Erreurs possibles :**
- Timeout (10s sur plan free Netlify)
- Erreur de connexion au Space HF
- Erreur avec `@gradio/client`

## ✅ Solution

### Étape 1 : Vérifier/Désactiver USE_MOCK

**Netlify Dashboard → Site settings → Environment variables :**

1. **Si `USE_MOCK` existe :**
   - Cliquer sur l'icône poubelle pour supprimer
   - OU changer la valeur à `false`

2. **Si `USE_MOCK` n'existe pas :**
   - C'est bon, le mock n'est pas forcé

3. **Redéployer le site** (si nécessaire)

### Étape 2 : Vérifier les Logs Netlify

**Netlify Dashboard → Functions → philosopher_rag → Logs**

Chercher dans les logs récents :
- `[RAG] Mode MOCK (USE_MOCK=true)` → Mock forcé
- `[RAG] Erreur SNB, fallback mock` → Erreur lors de l'appel
- `[RAG] Mode SNB Space OK` → ✅ Ça fonctionne !

### Étape 3 : Vérifier le Timeout

**Problème possible :** Le Space HF prend 30-60s au cold start, mais Netlify free a un timeout de 10s.

**Solution :**
- Garder le Space actif (éviter le cold start)
- OU passer au plan Pro Netlify (26s timeout)
- OU utiliser RunPod (voir `REPLI_RUNPOD.md`)

## 📋 Checklist

- [ ] Vérifier `USE_MOCK` dans Netlify (doit être `false` ou non défini)
- [ ] Consulter les logs Netlify pour voir l'erreur exacte
- [ ] Vérifier que le Space HF répond : `https://fjdaz-bergsonandfriends.hf.space/gradio_api/info`
- [ ] Tester à nouveau sur `https://chimerical-kashata-65179e.netlify.app/`

## 🔍 Test Rapide

Pour tester si le Space HF fonctionne :

```bash
curl -X POST https://chimerical-kashata-65179e.netlify.app/.netlify/functions/philosopher_rag \
  -H "Content-Type: application/json" \
  -d '{"action":"respond","philosopher":"spinoza","message":"test","history":[]}'
```

**Si la réponse est différente du mock** → ✅ Le Space HF fonctionne
**Si la réponse est identique au mock** → ❌ Vérifier `USE_MOCK` et les logs

---

**Dernière mise à jour :** 17 novembre 2025


