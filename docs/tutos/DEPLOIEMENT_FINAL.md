# 🎯 Déploiement Final - Bergson and Friends

**Date**: 18 novembre 2025
**Status**: ✅ Frontend OK | ⏳ Backend HF Space en cours

---

## ✅ Accompli

### 1. Frontend Production
- **URL**: https://fjdaz.com/bergson/index_spinoza.html
- **Status**: ✅ Fonctionnel
- **Stack**: HTML/JS vanilla + CSS fjdaz.com
- **Mobile**: ✅ Responsive adaptatif

### 2. Backend Railway (Mock + RAG)
- **URL**: https://bergson-api-production.up.railway.app
- **Status**: ✅ En ligne
- **Mode actuel**: Mock responses + RAG
- **Fichier**: `snb_api_mock.py`

### 3. HF Space Qwen 14B
- **URL**: https://fjdaz-bergsonandfriends.hf.space
- **Status**: ✅ Running (A10G-small)
- **Modèle**: Qwen 2.5 14B + LoRA Spinoza
- **Coût**: ~$1/h

---

## ⏳ En Cours

### Branchement Railway ↔ HF Space

**Fichier créé**: `snb_api_hf.py`
**Principe**: Railway appelle HF Space Gradio API

**Problème à résoudre**:
- Trouver le bon endpoint Gradio API
- Selon rapport: `api_name="/chat_function"`
- Tester: `/call/chat_function` ou `/api/chat_function`

**Code push**:
```bash
# Commit fait localement
git push origin main  # En cours de retry (GitHub 500 temporaire)
```

---

## 🔧 Prochaines Étapes

### 1. Identifier endpoint Gradio HF Space
```bash
# Tester les endpoints possibles:
curl https://fjdaz-bergsonandfriends.hf.space/call/chat_function
curl https://fjdaz-bergsonandfriends.hf.space/api/chat_function
curl https://fjdaz-bergsonandfriends.hf.space/run/predict
```

### 2. Adapter `snb_api_hf.py`
Une fois l'endpoint trouvé, corriger ligne 66:
```python
# Remplacer:
HF_API_ENDPOINT = f"{HF_SPACE_URL}/api/predict"
# Par le bon endpoint
```

### 3. Redéployer sur Railway
```bash
git add snb_api_hf.py
git commit -m "Fix HF Space API endpoint"
git push origin main
# Railway auto-deploy
```

### 4. Tester flow complet
```bash
# Test depuis Railway vers HF Space
curl -X POST https://bergson-api-production.up.railway.app/chat/spinoza \
  -H "Content-Type: application/json" \
  -d '{"message": "La joie augmente-t-elle ma puissance?", "history": [], "philosopher": "spinoza"}'
```

---

## 📊 Architecture Finale

```
Frontend (fjdaz.com)
    ↓ HTTPS
Railway API (snb_api_hf.py)
    ├─ RAG lookup (rag_system.py)
    └─ Appel Gradio API
         ↓ HTTPS
HF Space (Qwen 14B + LoRA)
    └─ Génération réponse philosophique
```

---

## 💰 Coûts

- **Railway**: Gratuit (tier free)
- **HF Space**: ~$1/h (A10G-small) = ~$720/mois si 24/7
- **Total**: Contrôlé par on/off du Space

**Optimisation**: Arrêter le Space quand pas utilisé

---

## 📝 Fichiers Clés

### Backend
- `snb_api_hf.py`: API Railway → HF Space
- `snb_api_mock.py`: API Railway mock (fallback)
- `rag_system.py`: Système RAG
- `requirements.txt`: Dépendances (fastapi, httpx, pydantic)
- `Procfile`: `web: python3 snb_api_hf.py`
- `runtime.txt`: `python-3.11.9`

### Frontend
- `index_spinoza.html`: Interface production Spinoza seul
- `app.js`: JS production (3 philosophes - backup)

### Data
- `data/RAG/Corpus Spinoza Dialogique 18k.md`
- `data/RAG/Glossaire Conversationnel Spinoza.md`

---

## 🐛 Debug

### Si Railway ne répond pas
```bash
railway logs --service bergson-api
railway status
```

### Si HF Space timeout
- Vérifier status: https://huggingface.co/spaces/FJDaz/bergsonAndFriends
- Restart si nécessaire

### Si frontend ne se connecte pas
- Console navigateur (F12)
- Vérifier logs `[INIT]` et `[CHAT]`
- Tester endpoint directement: `curl https://bergson-api-production.up.railway.app/health`

---

**Dernière mise à jour**: 18 nov 2025, 22h00
**Prochaine session**: Finaliser endpoint HF Space + tester génération réelle
