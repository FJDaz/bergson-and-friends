# ✅ Fix : Prompt Système Complet Utilisé

## 🐛 Problème Identifié

Le code utilisait `STYLE_INJECTION` (version courte) au lieu de `SYSTEM_PROMPTS` (version complète) dans la fonction `callSNB`.

**Avant :**
```javascript
const STYLE_INJECTION = {
    bergson: "Tu es Henri Bergson. Utilise des métaphores temporelles...",
    // Version très courte
};
```

**Problème :** Le prompt système complet (style + schèmes logiques + méthode) n'était pas utilisé.

## ✅ Solution Appliquée

**Après :**
```javascript
// Utiliser le prompt système COMPLET (style + schèmes logiques + méthode)
const systemPrompt = SYSTEM_PROMPTS[philosopher];
const enrichedMessage = `${systemPrompt}

Contexte pertinent (extraits de la littérature) :
${ragContext}

Question de l'élève : ${userMessage}`;
```

## 📋 Contenu du Prompt Système Complet

Chaque `SYSTEM_PROMPTS[philosopher]` contient :

1. **Style du philosophe**
   - Métaphores, vocabulaire, oppositions

2. **Schèmes logiques à mobiliser**
   - Opposition, analogie, implication, identité, causalité

3. **Méthode**
   - Étapes de raisonnement
   - Approche pédagogique

## 🎯 Résultat

Maintenant, quand le Space HF reçoit une question :
- ✅ Le prompt système complet est inclus dans le message
- ✅ Le contexte RAG (littérature locale) est ajouté
- ✅ La question de l'élève est incluse

Le philosophe aura donc accès à :
- Son style complet
- Ses schèmes logiques
- Sa méthode
- Le contexte de la littérature
- La question de l'élève

## 📝 Fichiers Modifiés

- `src/prompts.js` : Remplacement de `STYLE_INJECTION` par `SYSTEM_PROMPTS`

## 🧪 Test

Pour tester :
1. Déployer sur Netlify (ou tester localement)
2. Poser une question à un philosophe
3. Vérifier dans les logs Netlify que le prompt système complet est envoyé
4. Vérifier que la réponse du philosophe utilise bien son style complet

---

**Commit :** `Fix: Use complete SYSTEM_PROMPTS instead of short STYLE_INJECTION`
**Date :** 17 novembre 2025


