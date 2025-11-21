# 📝 Variations de Formulations - Réduction Systématisme

**Date :** 19 novembre 2025  
**Objectif :** Réduire les occurrences systématiques de "mais alors" et "donc tu es d'accord" au profit de formulations variées et naturelles.

---

## 🎯 Problème Actuel

### Formulations Trop Systématiques

**"mais alors"** apparaît :
- Dans les transitions (Spinoza, Bergson, Kant)
- Dans les formules dialectiques
- Dans l'adaptation contextuelle (contexte "resistance")
- → **Risque de répétition mécanique**

**"Donc tu es d'accord"** (ou équivalents) :
- Contexte "accord" → "Valide puis AVANCE logiquement avec 'Donc'"
- → **Risque de formulation prévisible**

---

## 💡 Suggestions de Variations

### 1. Alternatives à "mais alors" (Révéler contradictions/oppositions)

#### Pour Spinoza (causalité, nécessité)
- "Attends, si tu dis ça, alors..."
- "Pourtant, regarde..."
- "Sauf que..."
- "Or, si on suit ta logique..."
- "Cependant, cela implique que..."
- "Il y a une tension ici :"
- "C'est contradictoire :"
- "Tu dis X, mais tu fais Y. Comment tu expliques ?"
- "T'as raison sur [point], mais alors [tension]..."
- "OK, mais si c'est vrai, alors..."

#### Pour Bergson (durée vs temps spatial)
- "Pourtant, sens-tu vraiment ça ?"
- "Sauf que la durée, c'est autre chose..."
- "Or, si tu spatialises le temps..."
- "Cependant, le temps vécu..."
- "Il y a une opposition ici :"
- "C'est contradictoire : tu mesures le temps, mais tu le vis aussi."
- "Tu penses le temps, mais le sens-tu vraiment ?"

#### Pour Kant (distinctions, limites)
- "Pourtant, distinguons bien..."
- "Sauf que tu confonds..."
- "Or, si on examine les conditions de possibilité..."
- "Cependant, cela dépasse les limites de l'expérience."
- "Il y a une confusion ici :"
- "Tu mélanges [A] et [B]. Distinguons :"
- "OK, mais quelle est la condition de possibilité de ça ?"

---

### 2. Alternatives à "Donc tu es d'accord" (Contexte accord)

#### Formulations de validation + avancée
- "Exactement. Donc, si on pousse la logique..."
- "Oui, tu as raison. Cela implique que..."
- "Tout à fait. Alors, si on va plus loin..."
- "C'est ça. Donc, cela veut dire que..."
- "OK. Alors, si on suit cette piste..."
- "Je suis d'accord. Poursuivons :"
- "Tu as raison. Maintenant, regardons ce que ça implique :"
- "Exact. Donc, si on tire les conséquences..."
- "Oui. Alors, cela nous amène à..."
- "Tout à fait. Donc, cela signifie que..."

#### Variations selon philosophe

**Spinoza (causalité) :**
- "Oui. Donc, si tu vois les causes, alors..."
- "Exact. Cela implique que la nécessité..."
- "Tout à fait. Donc, si tu connais les causes..."

**Bergson (durée) :**
- "Oui. Donc, si tu sens la durée, alors..."
- "Exact. Cela veut dire que le temps vécu..."
- "Tout à fait. Donc, si tu saisis le flux..."

**Kant (distinctions) :**
- "Oui. Donc, si on distingue bien, alors..."
- "Exact. Cela implique que les conditions de possibilité..."
- "Tout à fait. Donc, si on examine rigoureusement..."

---

### 3. Système de Rotation Aléatoire

**Proposition :** Créer des listes de formulations et en choisir une aléatoirement selon le contexte.

#### Structure suggérée :

```python
FORMULATIONS_RESISTANCE = {
    "spinoza": [
        "mais alors",
        "pourtant",
        "sauf que",
        "or, si on suit ta logique",
        "il y a une tension ici",
        "c'est contradictoire",
        "attends, si tu dis ça, alors"
    ],
    "bergson": [
        "mais alors",
        "pourtant, sens-tu vraiment ça",
        "sauf que la durée, c'est autre chose",
        "or, si tu spatialises le temps",
        "il y a une opposition ici",
        "tu penses le temps, mais le sens-tu vraiment"
    ],
    "kant": [
        "mais alors",
        "pourtant, distinguons bien",
        "sauf que tu confonds",
        "or, si on examine les conditions",
        "il y a une confusion ici",
        "tu mélanges [A] et [B]. Distinguons"
    ]
}

FORMULATIONS_ACCORD = {
    "spinoza": [
        "Exactement. Donc, si on pousse la logique",
        "Oui, tu as raison. Cela implique que",
        "Tout à fait. Alors, si on va plus loin",
        "C'est ça. Donc, cela veut dire que",
        "OK. Alors, si on suit cette piste"
    ],
    "bergson": [
        "Oui. Donc, si tu sens la durée, alors",
        "Exact. Cela veut dire que le temps vécu",
        "Tout à fait. Donc, si tu saisis le flux",
        "Je suis d'accord. Poursuivons",
        "Tu as raison. Maintenant, regardons ce que ça implique"
    ],
    "kant": [
        "Oui. Donc, si on distingue bien, alors",
        "Exact. Cela implique que les conditions de possibilité",
        "Tout à fait. Donc, si on examine rigoureusement",
        "Je suis d'accord. Examinons les implications",
        "Tu as raison. Distinguons maintenant"
    ]
}
```

---

## 🔧 Implémentation Suggérée

### Option 1 : Rotation Aléatoire Simple

Dans `construire_prompt_contextuel()`, remplacer les instructions fixes par :

```python
if contexte == "resistance":
    formulations = FORMULATIONS_RESISTANCE[philosopher]
    formulation_choisie = random.choice(formulations)
    base += f"\nL'élève résiste → Révèle une contradiction en utilisant '{formulation_choisie}' et tes schèmes logiques."

elif contexte == "accord":
    formulations = FORMULATIONS_ACCORD[philosopher]
    formulation_choisie = random.choice(formulations)
    base += f"\nL'élève est d'accord → Valide puis AVANCE logiquement avec '{formulation_choisie}' et tes schèmes logiques."
```

### Option 2 : Instructions Variées (Sans Aléatoire)

Remplacer les instructions fixes par des instructions qui demandent la variation :

```python
if contexte == "resistance":
    base += f"\nL'élève résiste → Révèle une contradiction dans sa position. Varie tes formulations : 'mais alors', 'pourtant', 'sauf que', 'or', 'il y a une tension ici', etc. Utilise tes schèmes logiques."

elif contexte == "accord":
    base += f"\nL'élève est d'accord → Valide (ex: 'Oui', 'Exact', 'Tout à fait') puis AVANCE logiquement avec 'Donc', 'Alors', 'Cela implique', etc. Utilise tes schèmes logiques."
```

### Option 3 : Liste de Formulations dans le Prompt Système

Ajouter une section dans chaque prompt système avec une liste de formulations à varier :

```python
FORMULATIONS À VARIER SELON CONTEXTE :

Contexte "resistance" :
- "mais alors"
- "pourtant"
- "sauf que"
- "or"
- "il y a une tension ici"
- "c'est contradictoire"
- Varie selon le contexte, ne répète pas toujours la même.

Contexte "accord" :
- "Exactement. Donc..."
- "Oui, tu as raison. Cela implique..."
- "Tout à fait. Alors..."
- "C'est ça. Donc..."
- Varie selon le contexte, ne répète pas toujours la même.
```

---

## 📊 Recommandation

**Option 2 (Instructions Variées)** semble la plus simple et efficace :
- Pas besoin de code supplémentaire
- Le modèle comprend qu'il doit varier
- Moins de risque de répétition mécanique
- Plus naturel

**Option 3 (Liste dans Prompt)** est aussi bonne :
- Plus explicite
- Le modèle a des exemples concrets
- Facile à ajuster

---

## 🎯 Prochaines Étapes

1. ✅ Passer "MAIS ALORS" en minuscules (fait)
2. ✅ Choisir une option d'implémentation : Option 2 (Instructions Variées)
3. ✅ Modifier `construire_prompt_contextuel()` (fait)
4. ⏳ Tester les variations
5. ⏳ Ajuster selon résultats

---

**Dernière modification :** 19 novembre 2025

