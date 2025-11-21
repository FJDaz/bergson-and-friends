# 🎮 Cellule Colab : Backend Maïeuthon - Évaluation et Message Final

**À ajouter APRÈS la cellule 7 (API FastAPI) et AVANT la cellule 8 (Lancement Serveur)**

---

## 📝 Code de la cellule

```python
# =============================================================================
# 🎮 MAÏEUTHON - Backend : Évaluation et Message Final
# =============================================================================

from pydantic import BaseModel
import json
import re

class EvaluateRequest(BaseModel):
    dialogue: str
    score_front: int

class EvaluateResponse(BaseModel):
    score_final: int
    message_final: str
    details_model: dict

# Prompt d'évaluation (température basse, JSON strict)
PROMPT_EVALUATION = """Tu es Spinoza. Voici l'échange complet avec un élève :

{dialogue}

Évalue l'élève sur 3 critères (0 à 10) :
1. Compréhension de tes idées
2. Coopération dans le dialogue
3. Progression de la pensée

Réponds STRICTEMENT au format JSON, AUCUNE prose :

{{
 "comprehension": X,
 "cooperation": Y,
 "progression": Z,
 "total": X+Y+Z
}}"""

# Prompt message final (température haute, créativité)
PROMPT_MESSAGE_FINAL = """Tu es Spinoza.

En t'inspirant EXCLUSIVEMENT de ton propre système philosophique (Éthique, conatus, affects, puissance d'agir, servitude vs liberté, Dieu = Nature),

rédige un message bref à l'élève.

Structure (obligatoire) :
1. Un compliment sincère lié à son niveau global.
2. Un conseil précis basé sur son critère le plus faible.
3. Un surnom symbolique et positif, tiré de ton univers conceptuel (ex: "puissance d'agir", "essence active", "affect joyeux").

Maximum 3 phrases.
Style concis, poétique, jamais condescendant.

Message :"""

def evaluer_dialogue(dialogue: str, score_front: int) -> dict:
    """
    Évalue le dialogue et génère le message final
    """
    # 1. Évaluation (température basse, JSON strict)
    prompt_eval = PROMPT_EVALUATION.format(dialogue=dialogue)
    
    # Formatage Mistral
    prompt_eval_formatted = f"<s>[INST] {prompt_eval} [/INST]"
    
    inputs_eval = tokenizer(prompt_eval_formatted, return_tensors="pt").to(model.device)
    input_length_eval = inputs_eval['input_ids'].shape[1]
    
    device_type = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if device_type == "cuda" else torch.float32
    
    with torch.autocast(device_type=device_type, dtype=dtype):
        outputs_eval = model.generate(
            **inputs_eval,
            max_new_tokens=100,
            temperature=0.1,  # Très strict pour JSON
            top_p=0.9,
            do_sample=True,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    
    new_tokens_eval = outputs_eval[0][input_length_eval:]
    response_eval = tokenizer.decode(new_tokens_eval, skip_special_tokens=True)
    
    # Extraire JSON de la réponse
    json_match = re.search(r'\{[^}]+\}', response_eval, re.DOTALL)
    if json_match:
        try:
            details_model = json.loads(json_match.group(0))
        except:
            details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
    else:
        details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
    
    # Score total
    score_backend = details_model.get("total", 15)
    score_final = score_front + score_backend
    
    # 2. Message final (température haute, créativité)
    prompt_final = PROMPT_MESSAGE_FINAL
    
    prompt_final_formatted = f"<s>[INST] {prompt_final} [/INST]"
    
    inputs_final = tokenizer(prompt_final_formatted, return_tensors="pt").to(model.device)
    input_length_final = inputs_final['input_ids'].shape[1]
    
    with torch.autocast(device_type=device_type, dtype=dtype):
        outputs_final = model.generate(
            **inputs_final,
            max_new_tokens=150,
            temperature=1.1,  # Haute température pour créativité
            top_p=0.95,
            do_sample=True,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    
    new_tokens_final = outputs_final[0][input_length_final:]
    message_final = tokenizer.decode(new_tokens_final, skip_special_tokens=True)
    
    # Nettoyer le message final
    message_final = nettoyer_reponse(message_final)
    message_final = limiter_phrases(message_final, max_phrases=3)
    
    return {
        "score_final": score_final,
        "message_final": message_final,
        "details_model": details_model
    }

# Endpoint FastAPI
@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest):
    """
    Évalue le dialogue complet et génère le message final
    """
    result = evaluer_dialogue(req.dialogue, req.score_front)
    return EvaluateResponse(**result)

print("✅ Endpoint /evaluate créé pour Maïeuthon")
```

---

## 📋 Instructions d'ajout dans Colab

1. **Ouvrir le notebook** `RAG_Spinoza_secours.ipynb` dans Colab
2. **Insérer une nouvelle cellule** après la cellule 7 (API FastAPI)
3. **Copier-coller le code ci-dessus** dans cette nouvelle cellule
4. **Exécuter la cellule**
5. **Relancer la cellule 8** (Lancement Serveur) pour activer le nouvel endpoint

---

## ✅ Vérification

Après ajout, tester avec :
```bash
curl -X POST https://ton-url-ngrok.ngrok-free.dev/evaluate \
  -H "Content-Type: application/json" \
  -d '{"dialogue": "Élève: Bonjour\nSpinoza: Salut", "score_front": 85}'
```

---

**Note :** Cette cellule utilise les fonctions `nettoyer_reponse()` et `limiter_phrases()` déjà définies dans la cellule 4.

