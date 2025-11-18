# 🔄 Stratégie de Repli Backend SNB

Si Hugging Face suspend le Space à cause d'impayés, voici les options de repli pour héberger le modèle Qwen 14B + LoRA Spinoza.

## 🎯 Options de Repli (du plus simple au plus complexe)

### Option 1: **RunPod** ou **Vast.ai** (⭐ RECOMMANDÉ pour démo rapide)

**Avantages :**
- Pay-per-use (pas d'engagement)
- GPU à la demande (~$0.20-0.50/h)
- Setup rapide (1-2h)
- Contrôle total
- Compatible Docker (même stack que HF Spaces)

**Étapes :**
1. Créer compte sur [RunPod](https://www.runpod.io/) ou [Vast.ai](https://vast.ai/)
2. Déployer container Docker avec `app_spinoza_seul.py` + FastAPI ou Gradio
3. Obtenir URL publique du pod
4. Mettre à jour `SNB_BACKEND_URL` dans Netlify

**Coût estimé pour le 26 novembre :**
- 3h de démo × $0.30/h = **$0.90**

**Configuration Netlify :**
```bash
SNB_BACKEND_URL=https://ton-pod.runpod.io
# ou
SNB_BACKEND_URL=https://ton-pod.vast.ai
```

---

### Option 2: **Replicate** (API simple mais setup préalable)

**Avantages :**
- API REST simple
- Gestion automatique de l'infrastructure
- Bon pour démos ponctuelles

**Inconvénients :**
- Doit publier le modèle sur Replicate d'abord
- Setup initial plus long
- Coût par requête

**Étapes :**
1. Créer compte Replicate
2. Publier modèle Qwen 14B + LoRA (peut prendre plusieurs heures)
3. Adapter `callSNB()` pour utiliser l'API Replicate

**Coût :** ~$0.002-0.01 par requête

---

### Option 3: **Serveur GPU dédié** (OVH, Scaleway, Hetzner)

**Avantages :**
- Contrôle total
- Performance garantie
- Moins cher si utilisation intensive

**Inconvénients :**
- Setup plus complexe
- Engagement mensuel généralement
- Plus cher pour usage ponctuel

**Coût :** ~$50-100/mois pour GPU NVIDIA T4

---

### Option 4: **AWS/GCP/Azure** (pour usage pro)

**Avantages :**
- Infrastructure professionnelle
- Scaling automatique
- Support 24/7

**Inconvénients :**
- Setup très complexe
- Coûts élevés
- Overkill pour une démo

**Coût :** ~$100-300/mois minimum

---

### Option 5: **Serveur Local** (si tu as un GPU NVIDIA)

**Avantages :**
- Gratuit (si tu as déjà le GPU)
- Latence minimale
- Contrôle total

**Inconvénients :**
- Besoin d'un GPU NVIDIA (16GB+ VRAM pour Qwen 14B)
- Exposition publique complexe (reverse proxy, etc.)
- Électricité consommée

---

## 🛠️ Adaptation du Code

### Étape 1: Rendre l'URL configurable

**Fichier : `src/prompts.js`**
```javascript
async function callSNB(philosopher, ragContext, userMessage) {
    // URL du backend (HF Space par défaut, mais configurable)
    const SPACE_URL = process.env.SNB_BACKEND_URL || "fjdaz-spinoza-nb.hf.space";
    const API_PREFIX = process.env.SNB_API_PREFIX || "/gradio_api";
    
    // ... reste du code inchangé
}
```

### Étape 2: Variable d'environnement Netlify

**Dans Netlify Dashboard → Site settings → Environment variables :**
```
SNB_BACKEND_URL=https://ton-pod.runpod.io
SNB_API_PREFIX=/gradio_api
```

### Étape 3: Dockerfile pour RunPod/Vast.ai

**Créer `Dockerfile.runpod` :**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app_spinoza_seul.py app.py

EXPOSE 7860

CMD ["python", "app.py"]
```

---

## 🚀 Quick Start RunPod (si repli nécessaire)

### 1. Créer un template RunPod

**Settings → Container Image :**
- Image: `python:3.10-slim`
- Docker command:
  ```bash
  git clone https://huggingface.co/spaces/FJDaz/spinoza_NB && \
  cd spinoza_NB && \
  pip install -r requirements.txt && \
  python app_spinoza_seul.py
  ```

### 2. Exposer le port 7860

**Network → Port mapping:**
- Container port: `7860`
- Public port: `7860` (ou port auto)

### 3. Obtenir l'URL publique

RunPod génère une URL type : `https://abc123.runpod.io`

### 4. Mettre à jour Netlify

**Netlify → Environment variables :**
```
SNB_BACKEND_URL=abc123.runpod.io
```

---

## ⚠️ Plan d'Urgence pour le 26 Novembre

**Si HF suspend le Space 1h avant la démo :**

1. **Créer compte RunPod** (5 min)
2. **Déployer template Docker** (10 min)
3. **Attendre que le modèle charge** (5-10 min)
4. **Tester l'endpoint** (2 min)
5. **Mettre à jour `SNB_BACKEND_URL` sur Netlify** (1 min)
6. **Redéployer Netlify** (2 min)

**Total : ~25-30 minutes de repli**

---

## 📋 Checklist Préventive

- [ ] Créer compte RunPod/Vast.ai (préventif, gratuit)
- [ ] Préparer Dockerfile dans le repo
- [ ] Tester déploiement sur RunPod en local (1 test avant la démo)
- [ ] Documenter l'URL de repli
- [ ] Ajouter variable `SNB_BACKEND_URL` dans Netlify (vide = HF par défaut)

---

## 💡 Recommandation Finale

**Pour le 26 novembre :**
- **Backend principal :** HF Space `spinoza_NB` (ZeroGPU gratuit ou T4 small $0.40/h)
- **Backend de repli préparé :** RunPod template créé et testé (prêt en 30min si besoin)

**Si problème HF :**
1. Lancer le pod RunPod (1 clic)
2. Attendre 10min (chargement modèle)
3. Changer variable Netlify
4. Redéployer Netlify
5. ✅ Démo opérationnelle


