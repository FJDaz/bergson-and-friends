# Skill : Tester SNB + RAG en Local (Netlify Functions)

## 🎯 Objectif

Lancer la fonction `philosopher_rag` en local et vérifier l'enchaînement SNB + RAG, avec ou sans mock.

## 📋 Principe

Ce skill permet de tester le système complet (RAG + SNB) en local avant déploiement sur Netlify. Il utilise Netlify CLI pour simuler l'environnement de production.

## 🔧 Implémentation

### Pré-requis

- Node.js installé
- Netlify CLI : `npm i -g netlify-cli`
- Fichiers RAG présents dans `RAG/` :
  - `corpus_bergson_27k_dialogique.md`
  - `corpus_kant_20k.txt.md`
  - `Corpus Spinoza Dialogique 18k - Éthique II-IV.md`
  - `glossaire_bergson_conversationnel.md`
  - `glossaire_kant_conversationnel.md`
  - `Glossaire Conversationnel Spinoza - 12 Concepts.md`

### Fonctions

**Lancer le serveur local** :
```bash
# Depuis la racine du repo
export USE_MOCK=true   # ou false pour appeler le Space SNB réel
netlify dev
```
Par défaut: http://localhost:8888

## 📝 Exemple d'Utilisation

### Manuel

**Appels de test** :

- Initialiser (le philosophe pose la première question)
```bash
curl -s http://localhost:8888/.netlify/functions/philosopher_rag \
  -H 'Content-Type: application/json' \
  -d '{"action":"init","philosopher":"spinoza"}' | jq .
```

- Répondre (RAG + SNB)
```bash
curl -s http://localhost:8888/.netlify/functions/philosopher_rag \
  -H 'Content-Type: application/json' \
  -d '{
    "action":"respond",
    "philosopher":"spinoza",
    "message":"Je pense que la liberté c est choisir sans contrainte."
  }' | jq .
```

### Automatique (Skill)

**Cursor** peut invoquer ce skill pour :
- Tester le système après modifications
- Vérifier que RAG + SNB fonctionnent ensemble
- Debugger les problèmes de connexion

**Script d'aide (optionnel)** :
```bash
bash scripts/test_snb_rag_local.sh
```
Ce script effectue des appels init/respond contre un serveur `netlify dev` déjà lancé.

## 🎯 Avantages

1. **Test local** : Pas besoin de déployer pour tester
2. **Mode mock** : Teste RAG sans dépendre du Space SNB
3. **Debug facile** : Logs visibles dans la console
4. **Rapide** : Pas de latence réseau

## ⚠️ Points d'Attention

1. **USE_MOCK** :
   - `true` : Réponse vient de `getMockResponse`, teste RAG uniquement
   - `false` : Appel passe par le Space `fjdaz-spinoza-nb.hf.space` (latence possible au cold start)

2. **Logs** : Les logs utiles s'affichent dans la console `netlify dev` :
   - Concepts extraits
   - Passages RAG
   - Appel SNB
   - Erreurs éventuelles

3. **Dépendances** : Vérifier que tous les fichiers RAG sont présents

## 🔄 Workflow Recommandé

1. Lancer `netlify dev` avec `USE_MOCK=true` pour tester RAG
2. Tester avec `USE_MOCK=false` pour tester l'intégration complète
3. Vérifier les logs pour identifier les problèmes
4. Utiliser le script `test_snb_rag_local.sh` pour tests automatisés

## 📌 Notes

- Le serveur local simule l'environnement Netlify Functions
- Les variables d'environnement sont chargées depuis `.env` ou `netlify.toml`
- Le mode mock permet de tester sans dépendre du Space HF

---

*Dernière mise à jour : 2025-11-18*
