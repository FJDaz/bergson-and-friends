# ✅ Upgrade Prompt Système Spinoza - Schèmes Logiques

**Date :** 19 novembre 2025
**Objectif :** Remplacer app.py sur HF Space avec prompt système enrichi

---

## 🎯 Ce qui a été fait

Le fichier `app_with_api.py` a été modifié pour inclure le **prompt système détaillé avec schèmes logiques** selon `POLITIQUE_PROMPTS_SCHEMES_LOGIQUES.md`.

### Changements

**AVANT (lignes 67-82)** :
```python
SYSTEM_PROMPTS_BASE = [
    """Tu es Spinoza incarné. Tu dialogues avec un élève...""",
    # 3 variantes courtes
]
```

**APRÈS (lignes 68-94)** :
```python
SYSTEM_PROMPTS_BASE = [
    """Tu es Spinoza. Tu maîtrises les schèmes logiques et tu dialogues avec un élève de Terminale.

STYLE SPINOZIEN :
- Géométrie des affects (causes nécessaires, déductions)
- Identification Dieu = Nature
- Vocabulaire : conatus, affects, puissance d'agir, béatitude, servitude

SCHÈMES LOGIQUES À MOBILISER :
- Identité : Dieu = Nature = Substance unique
- Identité : Liberté = Connaissance de la nécessité
- Implication nécessaire : Si joie → augmentation puissance
- Causalité : Tout a une cause nécessaire (pas de libre arbitre)

MÉTHODE :
1. Révèle la nécessité causale
2. Distingue servitude (ignorance) vs liberté (connaissance)
3. Use d'exemples concrets modernes (réseaux sociaux, affects quotidiens)

TRANSITIONS À VARIER :
- "Donc" (pour déductions logiques)
- "MAIS ALORS" (pour révéler contradictions)
- "Imagine" (pour analogies concrètes)
- "Cela implique" (pour implications nécessaires)

Réponds de manière conversationnelle, tutoie l'élève, démontre géométriquement."""
]
```

---

## 📤 Instructions Upload HF Space

### Option A : Via Interface Web (recommandé)

1. Va sur https://huggingface.co/spaces/FJDaz/bergsonAndFriends
2. Clique sur **Files** > **app.py**
3. Clique sur **Edit**
4. **Remplace TOUT le contenu** par le fichier `/Users/francois-jeandazin/bergsonAndFriends/bergsonAndFriends_HF/app_with_api.py`
5. Commit message : `Upgrade prompt système Spinoza avec schèmes logiques détaillés`
6. Clique **Commit**

### Option B : Via Git (si tu as cloné le repo)

```bash
cd ~/path/to/bergsonAndFriends_HF_space
cp /Users/francois-jeandazin/bergsonAndFriends/bergsonAndFriends_HF/app_with_api.py app.py
git add app.py
git commit -m "Upgrade prompt système Spinoza avec schèmes logiques détaillés"
git push
```

---

## ⏱️ Rebuild HF Space

Après le commit :
- Le Space va **automatiquement rebuild** (5-10 min)
- Tu peux suivre les logs sur la page du Space
- Attendre que le status passe à **Running** ✅

---

## 🧪 Test

Une fois le Space running :

```bash
# Test API health
curl https://fjdaz-bergsonandfriends.hf.space/health | python3 -m json.tool

# Test chat avec nouveau prompt
curl -X POST https://fjdaz-bergsonandfriends.hf.space/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Mais je suis libre, je fais ce que je veux !",
    "history": []
  }' | python3 -m json.tool
```

**Réponse attendue :** Spinoza devrait utiliser "MAIS ALORS" pour révéler la contradiction et appliquer le schème logique de causalité nécessaire.

---

## 📊 Impact attendu

Avec le nouveau prompt :
- ✅ Schèmes logiques explicites (Identité, Implication, Causalité)
- ✅ Vocabulaire spinozien renforcé (conatus, affects, puissance d'agir)
- ✅ Méthode pédagogique claire (révéler nécessité, distinguer servitude/liberté)
- ✅ Transitions variées ("Donc", "MAIS ALORS", "Imagine", "Cela implique")
- ✅ Exemples concrets modernes (réseaux sociaux, affects quotidiens)

---

## 🔄 Rollback (si problème)

Si le nouveau prompt ne fonctionne pas bien :

1. Récupérer l'ancien `app.py` (commit précédent)
2. Le remettre sur le Space
3. Rebuild

Ancien commit disponible dans l'historique Git HF.

---

**Status :** Prêt à upload ✅
