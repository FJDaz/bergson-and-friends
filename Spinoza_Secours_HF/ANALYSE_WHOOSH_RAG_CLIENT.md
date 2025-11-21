# 🔍 Analyse : Whoosh pour RAG Côté Client

**Date :** 21 novembre 2025  
**Contexte :** Optimisation RAG pour Spinoza Secours (économie tokens)

---

## 💡 Concept Proposé

**Idée :** Utiliser Whoosh (ou équivalent) côté client (JavaScript) pour trier/filtrer les passages RAG **avant** d'envoyer au modèle, économisant ainsi des tokens.

---

## 🔍 Qu'est-ce que Whoosh ?

**Whoosh** est un moteur de recherche full-text en Python, léger et rapide.

**Caractéristiques :**
- ✅ Pure Python (pas de dépendances C)
- ✅ Léger (~500KB)
- ✅ Rapide pour petits/moyens corpus
- ✅ Indexation en mémoire ou disque
- ✅ Recherche avec scoring (BM25, TF-IDF)

**Limitation :** Whoosh est en **Python**, pas en JavaScript.

---

## 🎯 Alternatives JavaScript

### Option 1 : Lunr.js (RECOMMANDÉ)

**Lunr.js** est l'équivalent JavaScript de Whoosh.

**Caractéristiques :**
- ✅ Pure JavaScript (pas de dépendances)
- ✅ Léger (~14KB minifié)
- ✅ Rapide pour corpus moyens
- ✅ Indexation côté client
- ✅ Recherche avec scoring (BM25)
- ✅ Compatible navigateur + Node.js

**Exemple d'utilisation :**
```javascript
// Indexation côté client
const lunr = require('lunr');

const corpus = [
  { id: 1, text: "La liberté est la connaissance de la nécessité..." },
  { id: 2, text: "Le conatus est l'effort pour persévérer..." },
  // ...
];

const idx = lunr(function() {
  this.ref('id');
  this.field('text');
  corpus.forEach(doc => this.add(doc));
});

// Recherche
const results = idx.search('liberté causalité');
// Retourne : [{ ref: 1, score: 0.8 }, ...]
```

### Option 2 : FlexSearch

**FlexSearch** est un moteur de recherche ultra-rapide.

**Caractéristiques :**
- ✅ Ultra-rapide (indexation + recherche)
- ✅ Léger (~10KB minifié)
- ✅ Support recherche partielle, fuzzy
- ✅ Compatible navigateur + Node.js

**Exemple :**
```javascript
const FlexSearch = require('flexsearch');

const index = new FlexSearch.Index({
  tokenize: "forward",
  threshold: 0.1
});

// Indexation
corpus.forEach((doc, id) => index.add(id, doc.text));

// Recherche
const results = index.search('liberté');
```

### Option 3 : MiniSearch

**MiniSearch** est un moteur de recherche simple et efficace.

**Caractéristiques :**
- ✅ Simple à utiliser
- ✅ Léger (~8KB minifié)
- ✅ Support recherche avec boost
- ✅ Compatible navigateur + Node.js

---

## 🏗️ Architecture Proposée

### Schéma Actuel (RAG Côté Serveur)

```
Frontend (index_spinoza.html)
    ↓
Message utilisateur
    ↓
API Colab (FastAPI)
    ↓
rag_system.py (recherche passages)
    ↓
Injection passages dans prompt
    ↓
Modèle Mistral 7B
    ↓
Réponse générée
```

**Problème :** Tous les passages pertinents sont envoyés au modèle → consommation tokens.

### Schéma Proposé (RAG Côté Client)

```
Frontend (index_spinoza.html)
    ↓
Message utilisateur
    ↓
Lunr.js (recherche côté client)
    ↓
Tri passages par score
    ↓
Sélection top 1-2 passages
    ↓
API Colab (FastAPI)
    ↓
Injection passages sélectionnés
    ↓
Modèle Mistral 7B
    ↓
Réponse générée
```

**Avantage :** Seuls les passages les plus pertinents sont envoyés → économie tokens.

---

## 📊 Analyse Avantages/Inconvénients

### ✅ Avantages

1. **Économie Tokens**
   - Tri côté client → envoi seulement top passages
   - Réduction ~50-70% tokens RAG

2. **Rapidité**
   - Recherche instantanée (pas de latence réseau)
   - Pas d'attente serveur pour recherche RAG

3. **Scalabilité**
   - Charge serveur réduite
   - Corpus peut être plus volumineux

4. **Flexibilité**
   - Ajustement seuil score côté client
   - Pas besoin de modifier serveur

### ⚠️ Inconvénients

1. **Taille Corpus**
   - Corpus doit être chargé côté client (JavaScript)
   - Augmente taille page HTML (~500KB-2MB)
   - Temps chargement initial plus long

2. **Sécurité**
   - Corpus visible côté client (pas critique pour textes publics)
   - Pas de protection contre extraction

3. **Complexité**
   - Indexation côté client (première charge)
   - Gestion cache nécessaire

4. **Compatibilité**
   - Nécessite JavaScript activé
   - Performance dépend navigateur

---

## 🎯 Recommandation

### Pour Spinoza Secours (Contrainte Tokens)

**Option Recommandée :** **Hybride (Client + Serveur)**

**Stratégie :**
1. **Corpus léger côté client** (~50-100 passages clés)
   - Glossaire conversationnel (12 concepts Spinoza)
   - Passages courts (1-2 phrases)
   - Indexation Lunr.js

2. **Recherche côté client**
   - Tri top 1-2 passages
   - Envoi seulement passages sélectionnés

3. **Corpus complet côté serveur** (si besoin)
   - Corpus complet (18k tokens)
   - Recherche serveur si client ne trouve rien

**Avantages :**
- ✅ Économie tokens (tri côté client)
- ✅ Rapidité (recherche instantanée)
- ✅ Taille page raisonnable (~200-300KB)
- ✅ Fallback serveur si besoin

**Implémentation :**
```javascript
// Frontend (index_spinoza.html)
const corpus_light = [
  { id: 1, concept: "liberté", text: "La liberté est la connaissance de la nécessité..." },
  { id: 2, concept: "conatus", text: "Le conatus est l'effort pour persévérer..." },
  // ... 50-100 passages clés
];

const idx = lunr(function() {
  this.ref('id');
  this.field('text');
  this.field('concept');
  corpus_light.forEach(doc => this.add(doc));
});

function searchRAG(message) {
  const results = idx.search(message);
  // Top 1-2 passages avec score > 0.3
  const topPassages = results
    .filter(r => r.score > 0.3)
    .slice(0, 2)
    .map(r => corpus_light.find(d => d.id === r.ref));
  
  return topPassages;
}

// Utilisation
const userMessage = "Qu'est-ce que la liberté ?";
const ragPassages = searchRAG(userMessage);

// Envoi au serveur avec passages sélectionnés
fetch(`${API_BASE_URL}/chat`, {
  method: 'POST',
  body: JSON.stringify({
    message: userMessage,
    rag_passages: ragPassages  // Seulement top passages
  })
});
```

---

## 📊 Comparaison Options

| Option | Tokens Économisés | Taille Page | Complexité | Recommandation |
|--------|------------------|-------------|------------|----------------|
| **RAG Serveur (actuel)** | 0% | ~50KB | ⭐⭐ | ❌ Pas optimal |
| **RAG Client (Lunr.js)** | 50-70% | ~500KB-2MB | ⭐⭐⭐ | ⚠️ Si corpus léger |
| **RAG Hybride** | 40-60% | ~200-300KB | ⭐⭐⭐⭐ | ✅ **RECOMMANDÉ** |

---

## 🚀 Plan d'Implémentation

### Étape 1 : Préparation Corpus Léger

1. **Extraire passages clés** du corpus complet
   - Glossaire conversationnel (12 concepts)
   - Passages courts (1-2 phrases)
   - Max 50-100 passages

2. **Format JSON** pour chargement côté client
   ```json
   [
     {
       "id": 1,
       "concept": "liberté",
       "text": "La liberté est la connaissance de la nécessité...",
       "source": "Éthique, Partie II"
     },
     // ...
   ]
   ```

### Étape 2 : Intégration Lunr.js

1. **Ajouter Lunr.js** dans `index_spinoza.html`
   ```html
   <script src="https://unpkg.com/lunr@2.3.9/lunr.min.js"></script>
   ```

2. **Indexation au chargement**
   ```javascript
   let ragIndex = null;
   
   function initRAG() {
     ragIndex = lunr(function() {
       this.ref('id');
       this.field('text');
       this.field('concept');
       corpus_light.forEach(doc => this.add(doc));
     });
   }
   ```

3. **Recherche avant envoi**
   ```javascript
   function submitQuestion(userMessage) {
     // Recherche RAG côté client
     const ragPassages = searchRAG(userMessage);
     
     // Envoi avec passages sélectionnés
     fetch(`${API_BASE_URL}/chat`, {
       method: 'POST',
       body: JSON.stringify({
         message: userMessage,
         rag_passages: ragPassages
       })
     });
   }
   ```

### Étape 3 : Ajustement Serveur

1. **Modifier endpoint `/chat`** pour accepter `rag_passages`
   ```python
   @app_api.post("/chat")
   def chat(req: ChatReq):
       # Si rag_passages fournis, utiliser ceux-là
       if req.rag_passages:
           # Utiliser passages fournis (déjà triés côté client)
       else:
           # Fallback : recherche serveur
   ```

---

## ⚠️ Points d'Attention

### 1. Taille Corpus
- **Limite recommandée :** ~100 passages max
- **Taille estimée :** ~200-300KB (JSON + Lunr.js)
- **Alternative :** Chargement asynchrone (lazy loading)

### 2. Performance
- **Indexation :** ~100-200ms (première charge)
- **Recherche :** ~1-5ms (instantané)
- **Cache :** Indexer une seule fois, réutiliser

### 3. Compatibilité
- **Lunr.js :** Compatible tous navigateurs modernes
- **Fallback :** Si JavaScript désactivé → RAG serveur

---

## 📝 Conclusion

**Recommandation :** **RAG Hybride (Client + Serveur)**

**Pourquoi :**
- ✅ Économie tokens significative (40-60%)
- ✅ Rapidité recherche (instantané)
- ✅ Taille page raisonnable (~200-300KB)
- ✅ Fallback serveur si besoin

**Implémentation :**
1. Corpus léger (50-100 passages clés)
2. Lunr.js pour recherche côté client
3. Tri top 1-2 passages avant envoi
4. Serveur utilise passages fournis

**Économie estimée :** ~100-200 tokens par requête (si RAG activé)

---

**Dernière mise à jour :** 21 novembre 2025

