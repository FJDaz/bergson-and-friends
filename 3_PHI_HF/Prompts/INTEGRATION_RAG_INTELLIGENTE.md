# 🧠 Intégration Intelligente du RAG

**Date :** 19 novembre 2025  
**Objectif :** Intégrer le RAG de manière intelligente dans le Space 3_PHI, sans surcharger le prompt ni perdre la cohérence philosophique.

---

## 🎯 Principe : RAG Intelligent vs RAG Brut

### ❌ RAG Brut (À Éviter)
```
Message utilisateur + Injection brute de passages RAG → Modèle
```
**Problèmes :**
- Surcharge du prompt (trop de texte)
- Perte de cohérence (le modèle peut se perdre)
- Passages non pertinents injectés
- Pas de sélection intelligente
- **⚠️ CRITIQUE : Les passages bruts (texte authentique) cassent le style reformulé/adapté de chaque philosophe**
  - Style lourd, académique vs style conversationnel lycéen
  - Première personne vs troisième personne
  - Langage contemporain vs langage classique

### ✅ RAG Intelligent (Objectif)
```
Message utilisateur → Extraction concepts → Sélection passages pertinents → 
Extraction IDÉES (pas texte brut) → Reformulation style philosophe → 
Injection contextuelle ciblée → Modèle
```
**Avantages :**
- Seulement les passages vraiment pertinents
- Injection contextuelle (pas de surcharge)
- Cohérence philosophique préservée
- **✅ Style préservé : idées extraites et reformulées dans le style du philosophe**
- Utilisation intelligente par le modèle

---

## 🔧 Stratégies d'Intégration

### Stratégie 1 : RAG Sélectif (Recommandée)

**Principe :** Ne pas injecter le RAG systématiquement, mais seulement quand nécessaire.

#### Logique de Sélection

```python
def should_use_rag(message: str, philosopher: str, contexte: str) -> bool:
    """
    Détermine si le RAG est nécessaire pour cette question
    """
    # 1. Questions conceptuelles complexes → RAG utile
    concepts_complexes = ["liberté", "causalité", "durée", "phénomène", "noumène", 
                          "conatus", "affects", "intuition", "catégories"]
    
    message_lower = message.lower()
    has_complex_concept = any(concept in message_lower for concept in concepts_complexes)
    
    # 2. Questions courtes/simples → Pas besoin de RAG
    is_simple = len(message.split()) < 5
    
    # 3. Contexte "confusion" → RAG utile pour clarifier
    needs_clarification = contexte == "confusion"
    
    # 4. Contexte "accord" → RAG utile pour approfondir
    needs_deepening = contexte == "accord"
    
    return (has_complex_concept or needs_clarification or needs_deepening) and not is_simple
```

#### Injection Contextuelle

```python
def enrichir_message_avec_rag(message: str, rag_passages: List[Dict], philosopher: str) -> str:
    """
    Enrichit le message avec RAG de manière intelligente
    """
    if not rag_passages:
        return message
    
    # Filtrer les passages vraiment pertinents (score > seuil)
    passages_pertinents = [p for p in rag_passages if p.get('score', 0) > 3]
    
    if not passages_pertinents:
        return message
    
    # Construire contexte RAG ciblé
    context_rag = "\n\n[Contexte pertinent de l'œuvre] :\n"
    for i, passage in enumerate(passages_pertinents[:2], 1):  # Max 2 passages
        context_rag += f"\n{i}. {passage['title']} :\n{passage['content'][:300]}...\n"
    
    # Instruction pour utiliser le RAG intelligemment
    instruction = "\n\nUtilise ce contexte pour enrichir ta réponse, mais ne le récite pas. Intègre-le naturellement dans ton raisonnement philosophique."
    
    return message + context_rag + instruction
```

---

### Stratégie 2 : RAG Adaptatif par Contexte

**Principe :** Adapter l'utilisation du RAG selon le contexte détecté.

#### Contexte "Confusion" → RAG pour Clarifier

```python
if contexte == "confusion":
    # RAG prioritaire : chercher des analogies/exemples dans le corpus
    rag_passages = rag_lookup(philosopher, concepts, top_k=2)
    # Filtrer pour garder seulement les passages avec analogies/exemples
    passages_analogies = [p for p in rag_passages if "exemple" in p['content'].lower() 
                          or "imagine" in p['content'].lower()]
    
    if passages_analogies:
        # Extraire l'idée de l'analogie (pas le texte brut)
        idee_analogie = extraire_idees_passage(passages_analogies[0], philosopher)
        # Injection reformulée
        base += f"\n\n[Idée pour clarifier - reformule dans ton style] :\n{idee_analogie}\nUtilise cette idée pour éclaircir ta réponse, mais reformule-la dans TON style conversationnel."
```

#### Contexte "Résistance" → RAG pour Argumenter

```python
if contexte == "resistance":
    # RAG prioritaire : chercher des arguments/contre-arguments
    rag_passages = rag_lookup(philosopher, concepts, top_k=2)
    # Filtrer pour garder seulement les passages argumentatifs
    passages_arguments = [p for p in rag_passages if "mais" in p['content'].lower() 
                          or "pourtant" in p['content'].lower()]
    
    if passages_arguments:
        # Extraire l'idée de l'argument (pas le texte brut)
        idee_argument = extraire_idees_passage(passages_arguments[0], philosopher)
        # Injection reformulée
        base += f"\n\n[Idée argumentative - reformule dans ton style] :\n{idee_argument}\nUtilise cette idée pour révéler la contradiction, mais reformule-la dans TON style dialectique."
```

#### Contexte "Accord" → RAG pour Approfondir

```python
if contexte == "accord":
    # RAG prioritaire : chercher des développements/conséquences
    rag_passages = rag_lookup(philosopher, concepts, top_k=2)
    
    if rag_passages:
        # Extraire l'idée du développement (pas le texte brut)
        idee_developpement = extraire_idees_passage(rag_passages[0], philosopher)
        # Injection reformulée
        base += f"\n\n[Idée pour approfondir - reformule dans ton style] :\n{idee_developpement}\nUtilise cette idée pour avancer logiquement, mais reformule-la dans TON style conversationnel."
```

---

### Stratégie 3 : RAG avec Seuil de Pertinence

**Principe :** Ne pas injecter le RAG si les passages ne sont pas assez pertinents.

```python
def rag_intelligent(message: str, philosopher: str, seuil_pertinence: int = 5) -> Optional[str]:
    """
    RAG intelligent avec seuil de pertinence
    """
    # 1. Extraire concepts
    concepts = extract_concepts(message)
    
    if not concepts:
        return None  # Pas de concepts → pas de RAG
    
    # 2. Lookup RAG
    rag_passages = rag_lookup(philosopher, concepts, top_k=3)
    
    if not rag_passages:
        return None  # Pas de passages → pas de RAG
    
    # 3. Filtrer par seuil de pertinence
    passages_pertinents = [p for p in rag_passages if p.get('score', 0) >= seuil_pertinence]
    
    if not passages_pertinents:
        return None  # Passages pas assez pertinents → pas de RAG
    
    # 4. Formater seulement les plus pertinents (max 2)
    return format_rag_context(passages_pertinents[:2])
```

---

### Stratégie 4 : RAG Intégré dans le Prompt Système

**Principe :** Donner des instructions au modèle sur comment utiliser le RAG intelligemment.

```python
INSTRUCTION_RAG = """
UTILISATION INTELLIGENTE DU CONTEXTE RAG :
- Les idées fournies sont des RÉFÉRENCES, pas du texte à réciter
- REFORMULE ces idées dans TON style (première personne, langage lycéen, conversationnel)
- Ne copie pas le texte brut : extrais l'idée et reformule-la naturellement
- Utilise le contexte pour enrichir, pas pour remplacer ta pensée
- Si le contexte contredit ta logique, privilégie ta logique philosophique
- Cite implicitement (ex: "comme je l'ai montré...", "dans mon œuvre...")
- Varie : parfois utilise le contexte, parfois non
- IMPORTANT : Le style doit rester conversationnel et accessible, pas académique
"""
```

---

## 🎯 Recommandation : Stratégie Hybride

**Combinaison Stratégie 1 + Stratégie 3 + Stratégie 4**

### Implémentation Suggérée

```python
def construire_prompt_avec_rag(philosopher: str, contexte: str, message: str) -> str:
    """
    Construit le prompt avec RAG intelligent
    """
    # 1. Prompt système de base
    base = construire_prompt_contextuel(philosopher, contexte)
    
    # 2. Décider si RAG nécessaire
    if should_use_rag(message, philosopher, contexte):
        # 3. RAG intelligent avec seuil
        context_rag = rag_intelligent(message, philosopher, seuil_pertinence=5)
        
        if context_rag:
            # 4. Injection contextuelle selon contexte
            if contexte == "confusion":
                base += f"\n\n[Contexte pour clarifier] :\n{context_rag}\nUtilise cet exemple pour éclaircir ta réponse."
            elif contexte == "resistance":
                base += f"\n\n[Argument de l'œuvre] :\n{context_rag}\nUtilise cet argument pour révéler la contradiction."
            elif contexte == "accord":
                base += f"\n\n[Développement de l'œuvre] :\n{context_rag}\nUtilise ce développement pour avancer logiquement."
            else:
                base += f"\n\n[Contexte pertinent] :\n{context_rag}\nUtilise ce contexte pour enrichir ta réponse."
            
            # 5. Instruction d'utilisation intelligente
            base += INSTRUCTION_RAG
    
    return base
```

---

## 📊 Avantages de l'Approche Intelligente

### 1. **Sélectivité**
- RAG seulement quand nécessaire
- Pas de surcharge systématique
- Meilleure performance

### 2. **Pertinence**
- Seuil de pertinence (score > 5)
- Filtrage par contexte
- Max 2 passages (pas de surcharge)

### 3. **Cohérence**
- Instructions claires pour utiliser le RAG
- Le modèle intègre, ne récite pas
- Préservation du style philosophique

### 4. **Adaptabilité**
- RAG différent selon contexte
- Analogies pour confusion
- Arguments pour résistance
- Développements pour accord

---

## 🔧 Fichiers à Modifier

### 1. `app.py` - Ajouter RAG Intelligent

**Modifications nécessaires :**
- Importer `rag_system` (ou copier les fonctions)
- Ajouter `should_use_rag()` et `rag_intelligent()`
- Modifier `generate_response()` pour utiliser RAG intelligent
- Ajouter `INSTRUCTION_RAG` dans les prompts

### 2. `requirements.txt` - Vérifier dépendances

**Dépendances RAG :**
- Pas de dépendances externes (juste `pathlib`, `re` - déjà dans stdlib)
- Les fichiers corpus doivent être dans `data/RAG/` (déjà présents)

### 3. Structure Fichiers

```
3_PHI_HF/
├── app.py (modifié avec RAG intelligent)
├── rag_system.py (copier depuis racine ou importer)
├── data/
│   └── RAG/ (déjà présent avec corpus)
└── Prompts/
    └── INTEGRATION_RAG_INTELLIGENTE.md (ce document)
```

---

## ⚠️ Points d'Attention

### 1. **Performance**
- RAG ajoute de la latence (lecture fichiers, scoring)
- Solution : Cache des corpus en mémoire au démarrage
- Limiter à 2 passages max

### 2. **Pertinence**
- Seuil de pertinence à ajuster selon tests
- Commencer avec seuil = 5, ajuster selon résultats

### 3. **Cohérence**
- Instructions claires pour éviter récitation
- Le modèle doit intégrer, pas copier

### 4. **Style (CRITIQUE)**
- **⚠️ Les passages bruts cassent le style reformulé**
- **Solution : Extraire les IDÉES, pas le texte brut**
- **Reformuler dans le style du philosophe (première personne, lycéen)**
- **Instructions claires : "reformule dans TON style"**

### 5. **Corpus**
- Vérifier que les fichiers corpus sont bien dans `data/RAG/`
- Vérifier les noms de fichiers (majuscules/minuscules)

---

## 🎯 Prochaines Étapes

1. ⏳ Copier `rag_system.py` dans `3_PHI_HF/` ou adapter les imports
2. ⏳ Implémenter `should_use_rag()` et `rag_intelligent()`
3. ⏳ Modifier `generate_response()` pour intégrer RAG intelligent
4. ⏳ Tester avec différents contextes
5. ⏳ Ajuster seuil de pertinence selon résultats
6. ⏳ Optimiser performance (cache corpus)

---

**Dernière modification :** 19 novembre 2025

