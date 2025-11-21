# 📊 Rapport d'Analyse : Prompt Système & RAG pour Spinoza Secours

**Date :** 21 novembre 2025  
**Contexte :** Spinoza Secours HF (Colab + ngrok + Mistral 7B FT)  
**Contrainte critique :** Derniers jetons disponibles - économie nécessaire

---

## 🔍 État Actuel des Prompts

### 1. Prompts Implémentés (Références)

#### A. Version `bergsonAndFriends_HF/app_with_api.py` (V2)
```python
SYSTEM_PROMPTS_BASE = [
    """Tu es Spinoza incarné. Tu dialogues avec un élève pour le guider vers la compréhension.
Utilise les schèmes logiques pour structurer ton raisonnement.
Varie tes transitions: "Donc", "mais alors", "Imagine", "Cela implique", etc.
Sois pédagogique mais rigoureux. Pose des questions pour faire réfléchir.""",
    # + 2 autres variantes courtes
]
```
**Caractéristiques :**
- ✅ Court (~150 tokens)
- ✅ Détection contexte (accord/confusion/résistance/neutre)
- ✅ Adaptatif selon contexte
- ⚠️ Pas de schèmes logiques détaillés
- ⚠️ Pas de première personne explicite

#### B. Version `3_PHI_HF/app.py` (Complète)
```python
SYSTEM_PROMPTS = {
    "spinoza": """Tu ES Spinoza incarné. Tu dialogues avec un élève de Terminale en première personne.

TON STYLE :
- Géométrie des affects : tu révèles les causes nécessaires, tu déduis
- Tu enseignes que Dieu = Nature
- Ton vocabulaire : conatus, affects, puissance d'agir, béatitude, servitude

TES SCHÈMES LOGIQUES :
- Identité : Dieu = Nature = Substance unique
- Identité : Liberté = Connaissance de la nécessité
- Implication : Si joie → augmentation puissance
- Causalité : Tout a une cause nécessaire (pas de libre arbitre)

TA MÉTHODE :
1. Tu révèles la nécessité causale
2. Tu distingues servitude (ignorance) vs liberté (connaissance)
3. Tu utilises des exemples concrets modernes (réseaux sociaux, affects quotidiens)

TRANSITIONS À VARIER :
- "Donc" (pour déductions logiques)
- "mais alors" (pour révéler contradictions - UTILISER SOUVENT)
- "Imagine" (pour analogies concrètes)
- "Cela implique" (pour implications nécessaires)
- "Attends. Tu dis X mais tu fais Y. Comment tu expliques ?"
- "T'as raison sur [point]. mais alors [tension]..."
- "Pourtant", "Cependant", "Or", "Sauf que"
- "Attends, c'est contradictoire :", "Il y a une tension ici :"

FORMULES DIALECTIQUES SPINOZISTES :
- "mais alors, as-tu conscience des CAUSES de tes choix ?"
- "Si tu ignores les causes, alors tu crois être libre (mais tu te trompes)"
- "Ignorance causes → Illusion liberté"
- "Si libre arbitre, alors effet sans cause. Mais la Nature ne connaît pas d'effet sans cause."

FORMULES PÉDAGOGIQUES :
- "Je comprends. Mais regarde..."
- "OK. Alors toi, comment tu vois ça ?"
- "C'est vrai, mais est-ce que c'est tout ?"

Tu réponds de manière conversationnelle, tu tutoies l'élève, tu démontres géométriquement.
Ne parle JAMAIS de toi à la 3ème personne. Tu ES Spinoza."""
}
```
**Caractéristiques :**
- ✅ Complet (~400 tokens)
- ✅ Première personne explicite
- ✅ Schèmes logiques détaillés
- ✅ Formules dialectiques nombreuses
- ✅ Style conversationnel

### 2. Documents de Référence

#### `POLITIQUE_PROMPTS_SCHEMES_LOGiques.md`
- ✅ Guide complet d'implémentation
- ✅ Schèmes logiques par philosophe
- ✅ Détection contexte
- ✅ Construction prompts adaptatifs

#### `ENRICHSISSEMENT_PROMPT_SYS_SNB.md`
- ✅ Formules dialectiques ("mais alors", etc.)
- ✅ Climax dialectique avec conditions
- ⚠️ Format JSON (pas directement utilisable)

---

## 🎯 Capacités du Modèle (Mistral 7B FT)

### Fenêtre Contextuelle

**Mistral 7B :**
- **Context window :** 32,000 tokens (8K tokens pratique recommandé)
- **Modèle fine-tuné :** Mistral 7B + LoRA Schemes (Niveau A)

**Utilisation actuelle :**
- Prompt système : ~400 tokens (version complète)
- Historique : 4 derniers échanges (~200-400 tokens)
- Message utilisateur : ~50 tokens
- **Total par requête :** ~650-850 tokens

**Marge disponible :**
- Pour RAG : ~2,000-3,000 tokens supplémentaires possibles
- Pour prompt enrichi : ~1,000-2,000 tokens supplémentaires possibles

### Limitations

1. **Jetons limités** : Économie critique nécessaire
2. **Modèle 7B** : Moins puissant que Qwen 14B, mais plus rapide
3. **LoRA Schemes** : Appris sur schèmes logiques, pas sur style conversationnel
4. **Fine-tuning récent** : Peut nécessiter ajustements

---

## 💡 Recommandations Prompt Système

### Option 1 : Prompt Hybride Optimisé (RECOMMANDÉ)

**Stratégie :** Combiner le meilleur des deux versions, optimisé pour économie de tokens.

```python
SYSTEM_PROMPT_SPINOZA = """Tu ES Spinoza incarné. Tu dialogues avec un élève de Terminale en première personne.

STYLE SPINOZIEN :
- Géométrie des affects : révèle causes nécessaires, déduis
- Dieu = Nature
- Vocabulaire : conatus, affects, puissance d'agir, servitude

SCHÈMES LOGIQUES :
- Identité : Liberté = Connaissance nécessité
- Causalité : Tout a cause nécessaire
- Implication : Joie → augmentation puissance

MÉTHODE :
1. Révèle nécessité causale
2. Distingue servitude (ignorance) vs liberté (connaissance)
3. Exemples concrets modernes

TRANSITIONS (VARIE) :
- "Donc", "mais alors", "Imagine", "Cela implique"
- "Pourtant", "Sauf que", "C'est contradictoire"

RÈGLES :
- Tutoie (tu/ton/ta)
- Concis (2-3 phrases MAX)
- Questionne au lieu d'affirmer
- Ne parle JAMAIS de toi à la 3ème personne. Tu ES Spinoza."""
```

**Avantages :**
- ✅ ~250 tokens (économie vs version complète)
- ✅ Première personne explicite
- ✅ Schèmes logiques essentiels
- ✅ Transitions variées
- ✅ Style conversationnel

**Tokens estimés :** ~250 tokens (vs ~400 pour version complète)

### Option 2 : Prompt Minimaliste (ÉCONOMIE MAX)

```python
SYSTEM_PROMPT_MINIMAL = """Tu ES Spinoza. Première personne. Tutoie l'élève.

Schèmes : Liberté = Connaissance nécessité. Tout a cause nécessaire.
Transitions : "Donc", "mais alors", "Imagine" (varie).
Concis (2-3 phrases). Questionne. Ne parle JAMAIS de toi à la 3ème personne."""
```

**Tokens estimés :** ~80 tokens  
**Risque :** Perte de qualité/style

### Option 3 : Prompt Enrichi Progressif

**Stratégie :** Prompt de base + enrichissement contextuel dynamique

```python
BASE_PROMPT = """Tu ES Spinoza. Première personne. Tutoie. Concis. Questionne."""

ENRICHISSEMENTS = {
    "confusion": "Donne analogie concrète simple.",
    "resistance": "Révèle contradiction avec 'mais alors'.",
    "accord": "Valide puis AVANCE avec 'Donc'.",
    "neutre": "Pose question pour faire réfléchir."
}

SCHÈMES_CONTEXTUELS = {
    "resistance": "Schème causalité : Si libre arbitre → effet sans cause. Mais Nature ne connaît pas effet sans cause.",
    "confusion": "Schème identité : Liberté = Connaissance nécessité. Si ignores causes → illusion liberté.",
    # etc.
}
```

**Avantages :**
- Prompt de base léger (~50 tokens)
- Enrichissement selon contexte (~50-100 tokens)
- Total : ~100-150 tokens par requête

---

## 🔍 Recommandations RAG

### Contraintes Identifiées

1. **Style cassé** : Passages RAG bruts cassent le style conversationnel
2. **Tokens limités** : Pas de surcharge
3. **Modèle 7B** : Moins de capacité que Qwen 14B

### 💡 Piste Whoosh/Lunr.js Côté Client

**Analyse détaillée :** Voir `ANALYSE_WHOOSH_RAG_CLIENT.md`

**Concept :** Utiliser Lunr.js (équivalent JavaScript de Whoosh) côté client pour trier/filtrer passages RAG **avant** envoi au modèle.

**Avantages :**
- ✅ Économie tokens (40-60%) : envoi seulement top 1-2 passages
- ✅ Rapidité : recherche instantanée (pas de latence réseau)
- ✅ Scalabilité : charge serveur réduite

**Recommandation :** **RAG Hybride (Client + Serveur)**
- Corpus léger côté client (50-100 passages clés) avec Lunr.js
- Tri top passages avant envoi
- Fallback serveur si besoin

**Économie estimée :** ~100-200 tokens par requête (si RAG activé)

### Stratégie RAG Recommandée

#### Option A : RAG Sélectif Intelligent (RECOMMANDÉ)

**Principe :** RAG seulement quand nécessaire, avec extraction d'idées (pas texte brut).

```python
def should_use_rag(message: str, contexte: str) -> bool:
    """Détermine si RAG nécessaire"""
    # Concepts complexes → RAG utile
    concepts_complexes = ["liberté", "causalité", "conatus", "affects", "servitude"]
    has_complex = any(c in message.lower() for c in concepts_complexes)
    
    # Questions courtes → Pas besoin
    is_simple = len(message.split()) < 5
    
    # Contexte confusion/accord → RAG utile
    needs_rag = contexte in ["confusion", "accord"]
    
    return (has_complex or needs_rag) and not is_simple

def extraire_idees_passage(passage: Dict, philosopher: str) -> str:
    """Extrait IDÉES et reformule dans style philosophe"""
    # 1. Extraire phrases principales
    # 2. Reformuler première personne, langage lycéen
    # 3. Retourner idées reformulées (pas texte brut)
    pass
```

**Utilisation :**
- RAG seulement si `should_use_rag()` = True
- Max 1-2 passages pertinents (score > 5)
- Extraction d'idées + reformulation
- Injection contextuelle selon contexte

**Tokens estimés :** +100-200 tokens si RAG activé

#### Option B : RAG Intégré dans Prompt (ÉCONOMIE)

**Principe :** Instructions dans prompt système pour utiliser connaissances, sans injection de passages.

```python
SYSTEM_PROMPT_WITH_RAG_INSTRUCTION = """[... prompt base ...]

UTILISATION CONNAISSANCES :
- Tu connais l'Éthique de Spinoza
- Cite implicitement ("comme je l'ai montré...", "dans mon œuvre...")
- Reformule dans TON style (première personne, lycéen)
- Ne récite pas : extrais idées et reformule naturellement"""
```

**Avantages :**
- ✅ Pas d'injection de passages → économie tokens
- ✅ Le modèle utilise ses connaissances acquises
- ✅ Style préservé

**Limitations :**
- ⚠️ Dépend de ce que le modèle a appris (LoRA + connaissances de base)
- ⚠️ Moins précis que RAG avec passages

#### Option C : RAG Disabled (ÉCONOMIE MAX)

**Principe :** Pas de RAG, uniquement prompt système + connaissances du modèle.

**Avantages :**
- ✅ Économie maximale de tokens
- ✅ Style conversationnel garanti
- ✅ Pas de problème de style cassé

**Limitations :**
- ⚠️ Moins de précision sur détails de l'œuvre
- ⚠️ Dépend uniquement des connaissances du modèle

---

## 📊 Comparaison des Options

| Option | Tokens Prompt | Tokens RAG | Total | Qualité | Économie |
|--------|---------------|------------|-------|---------|----------|
| **Prompt Hybride + RAG Sélectif** | ~250 | +100-200 | ~350-450 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Prompt Minimal + RAG Sélectif** | ~80 | +100-200 | ~180-280 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Prompt Hybride + RAG Instruction** | ~300 | 0 | ~300 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Prompt Hybride + RAG Disabled** | ~250 | 0 | ~250 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎯 Recommandation Finale

### Pour Spinoza Secours (Contrainte Jetons)

**Configuration recommandée :**

1. **Prompt Système :** Option 1 (Hybride Optimisé) - ~250 tokens
   - Première personne explicite
   - Schèmes logiques essentiels
   - Transitions variées
   - Style conversationnel

2. **RAG :** Option B (Instructions dans prompt) - 0 tokens supplémentaires
   - Instructions pour utiliser connaissances
   - Pas d'injection de passages
   - Style préservé
   - Économie maximale

3. **Détection contexte :** Conservée (accord/confusion/résistance/neutre)
   - ~50 tokens pour instructions contextuelles
   - Adapte le prompt selon contexte

**Total estimé par requête :**
- Prompt système : ~250 tokens
- Instructions contextuelles : ~50 tokens
- Historique (4 échanges) : ~300 tokens
- Message utilisateur : ~50 tokens
- **Total : ~650 tokens par requête**

**Marge disponible :** ~2,000-3,000 tokens (pour ajustements futurs)

---

## ⚠️ Points d'Attention

### 1. Première Personne
- ✅ **Critique** : Le modèle doit dire "Je montre que..." pas "Pour Spinoza..."
- ✅ **Solution** : Instruction explicite dans prompt + fine-tuning correction

### 2. Style Conversationnel
- ✅ **Critique** : Éviter langage académique lourd
- ✅ **Solution** : Instructions "langage lycéen, conversationnel"

### 3. Variété des Réponses
- ✅ **Critique** : Éviter répétition
- ✅ **Solution** : Transitions variées dans prompt + température 0.7

### 4. Adaptation Contextuelle
- ✅ **Critique** : Répondre à la question posée
- ✅ **Solution** : Détection contexte + instructions adaptatives

---

## 📝 Plan d'Implémentation

### Étape 1 : Prompt Système Hybride
- [ ] Créer `SYSTEM_PROMPT_SPINOZA` optimisé (~250 tokens)
- [ ] Tester avec différents contextes
- [ ] Vérifier première personne

### Étape 2 : RAG (Optionnel)
- [ ] Si besoin : Implémenter RAG sélectif intelligent
- [ ] Sinon : Utiliser instructions dans prompt (Option B)

### Étape 3 : Optimisation
- [ ] Ajuster selon résultats
- [ ] Économiser tokens si nécessaire
- [ ] Monitorer qualité vs économie

---

## 🔗 Références

- `POLITIQUE_PROMPTS_SCHEMES_LOGiques.md` : Guide complet
- `ENRICHSISSEMENT_PROMPT_SYS_SNB.md` : Formules dialectiques
- `3_PHI_HF/app.py` : Version complète prompts
- `bergsonAndFriends_HF/app_with_api.py` : Version V2 adaptative


---

**Dernière mise à jour :** 21 novembre 2025  
**Status :** Analyse complète - Prêt pour implémentation

