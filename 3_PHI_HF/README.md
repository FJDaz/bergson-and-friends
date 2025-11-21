---
title: 3 Philosophes - Test Prompts
emoji: 🎭
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "5.49.1"
app_file: app.py
pinned: false
---

# 🎭 3 Philosophes - Test Prompts Système

**Expérience :** 1 modèle (Qwen 14B + LoRA Spinoza NB), 3 prompts système différents

## Concept

Tester si le **prompt système seul** suffit à différencier les 3 philosophes, sans LoRAs séparés.

## Architecture

```
Qwen 2.5 14B (8-bit)
    ↓
LoRA Spinoza Niveau B (commun aux 3)
    ↓
Prompt Système Spinoza | Bergson | Kant
```

## Philosophes

### Spinoza
- **Schèmes** : Identité (Dieu=Nature), Causalité nécessaire, Implication (joie→puissance)
- **Style** : Géométrie des affects, déduction rigoureuse
- **Transitions** : "MAIS ALORS", "Cela implique", "Donc"

### Bergson
- **Schèmes** : Opposition (durée ≠ temps spatial), Analogie (mélodie, flux)
- **Style** : Métaphores temporelles, intuition vs intelligence
- **Transitions** : "Imagine", "Pense à une mélodie", "C'est contradictoire"

### Kant
- **Schèmes** : Distinction (phénomène/noumène, a priori/a posteriori), Condition (autonomie)
- **Style** : Architecture critique, examen transcendantal
- **Transitions** : "Distinguons", "Il convient d'examiner", "Quelle est la condition..."

## Fonctionnalités

- ✅ Détection contextuelle (accord/confusion/résistance/neutre)
- ✅ Prompts adaptatifs selon contexte
- ✅ Formules dialectiques par philosophe
- ✅ API REST FastAPI (`/chat`, `/init/{philosopher}`, `/health`)
- ✅ Interface Gradio (3 onglets)
- ✅ Questions bac personnalisées par philosophe

## API REST

### Endpoints

```bash
# Health check
GET /health

# Init conversation
GET /init/{philosopher}  # spinoza, bergson, kant

# Chat
POST /chat
{
  "message": "Qu'est-ce que la liberté ?",
  "history": [],
  "philosopher": "spinoza"
}
```

### Exemple

```bash
# Spinoza
curl -X POST http://localhost:7860/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Je suis libre de choisir",
    "history": [],
    "philosopher": "spinoza"
  }'

# Bergson
curl -X POST http://localhost:7860/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Le temps se mesure en secondes",
    "history": [],
    "philosopher": "bergson"
  }'

# Kant
curl -X POST http://localhost:7860/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Peut-on connaître Dieu ?",
    "history": [],
    "philosopher": "kant"
  }'
```

## Déploiement HF Space

1. Uploader `app.py` et `requirements.txt` sur `FJDaz/3_PHI`
2. Ajouter secret `HF_TOKEN` avec token read
3. GPU L4 requis (~18 GB VRAM)

## Objectif Test

Vérifier si Spinoza NB peut :
- ✅ Poser des questions de type spinoziste (causalité, affects)
- ✅ Poser des questions de type bergsonien (durée, intuition) avec prompt Bergson
- ✅ Poser des questions de type kantien (distinction, condition) avec prompt Kant

Si oui → Prompt système suffisant, pas besoin 3 LoRAs séparés
Si non → Besoin LoRAs spécialisés par philosophe

## Next Steps (si test concluant)

1. Ajouter RAG personnalisé par philosophe
2. Affiner formules dialectiques
3. Optimiser détection contextuelle
4. Intégrer frontend 3 philosophes

---

**Date :** 19 novembre 2025
**Status :** Prêt à tester
