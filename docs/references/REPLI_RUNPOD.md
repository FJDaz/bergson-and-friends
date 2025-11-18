# 🚀 Plan de Repli RunPod - Guide Complet

Si le Space HF `bergsonAndFriends` ne démarre pas, voici comment déployer sur RunPod en 30 minutes.

---

## ⚡ Quick Start (30 minutes)

### 1. Créer un compte RunPod (5 min)

1. Va sur https://www.runpod.io/
2. Créer un compte (email + password)
3. Ajouter une méthode de paiement (carte bancaire)
4. Créditer le compte de $5-10 pour commencer (pay-per-use, tu peux arrêter quand tu veux)

---

### 2. Créer un Template (10 min)

**Depuis le dashboard RunPod :**

1. Va sur **"Templates"** → **"Create Template"**

2. **Configuration du Template :**
   ```
   Name: spinoza-nb-14b
   Container Image: python:3.10-slim
   Docker Command:
   ```

3. **Dockerfile dans le template (à copier) :**
   ```dockerfile
   FROM python:3.10-slim
   
   WORKDIR /app
   
   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       build-essential \
       git \
       && rm -rf /var/lib/apt/lists/*
   
   # Install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Clone repo SNB (ou copier depuis ton repo)
   RUN git clone https://huggingface.co/spaces/FJDaz/spinoza_NB /app/snb || true
   
   # Copier app.py
   COPY app.py /app/app.py
   
   # Expose port
   EXPOSE 7860
   
   # Run Gradio
   CMD ["python", "/app/app.py"]
   ```

4. **Ou plus simple - Docker Command direct :**
   ```bash
   git clone https://huggingface.co/spaces/FJDaz/spinoza_NB /app && \
   cd /app && \
   pip install -r requirements.txt && \
   python app.py
   ```

---

### 3. Déployer un Pod GPU (5 min)

1. Va sur **"Pods"** → **"Create Pod"**

2. **Configuration :**
   - **Template :** `spinoza-nb-14b` (celui créé à l'étape 2)
   - **GPU :** 
     - **A10G** (24GB VRAM) - ~$1.00/h ✅ Recommandé
     - **T4** (16GB VRAM) - ~$0.30/h (si A10G indisponible)
   - **Container Disk :** 50GB (pour le modèle)
   - **Volume Disk :** 0GB (pas nécessaire pour débuter)

3. **Network :**
   - **Port Mapping :**
     - Container Port: `7860`
     - Public Port: `Auto` (RunPod génère une URL)

4. **Clique "Create Pod"**

5. **Attendre le démarrage** (2-5 minutes)
   - Le pod va cloner le repo
   - Installer les dépendances
   - Charger le modèle (5-10 minutes pour Qwen 14B)

---

### 4. Obtenir l'URL publique (1 min)

Une fois le pod démarré :

1. Va sur **"Pods"** → Clique sur ton pod
2. Tu verras **"Connect"** avec une URL publique type :
   ```
   https://abc123xyz-7860.proxy.runpod.net
   ```
3. Cette URL expose ton Gradio sur le port 7860

---

### 5. Tester l'API (2 min)

```bash
# Tester l'endpoint API
curl https://abc123xyz-7860.proxy.runpod.net/gradio_api/info

# Tester /chat_function
curl -X POST https://abc123xyz-7860.proxy.runpod.net/gradio_api/call/chat_function \
  -H "Content-Type: application/json" \
  -d '{"data":["Tu es Spinoza. Question: La liberté est-elle une illusion ?",[]]}'
```

---

### 6. Mettre à jour Netlify (2 min)

1. Va sur **Netlify Dashboard** → **Site settings** → **Environment variables**

2. Ajouter/modifier :
   ```
   SNB_BACKEND_URL=abc123xyz-7860.proxy.runpod.net
   SNB_API_PREFIX=/gradio_api
   ```

3. **Redéployer Netlify :**
   ```bash
   # Ou depuis l'interface Netlify
   # Site → Deploys → Trigger deploy
   ```

4. ✅ **C'est fait !** Netlify va maintenant appeler RunPod au lieu de HF Space

---

## 📋 Préparation Préventive (AVANT le problème)

### Option A : Template Prêt

1. **Créer le template maintenant** (même si pas utilisé)
   - Template: `spinoza-nb-14b`
   - Docker command prêt
   - Tu peux tester une fois pour vérifier que ça marche

2. **Tester une fois** (optionnel mais recommandé) :
   - Créer un pod de test (1h = $1)
   - Vérifier que le modèle charge
   - Tester l'API
   - Supprimer le pod
   - **Coût : ~$1 pour être sûr que ça marche**

### Option B : Dockerfile Prêt

Créer un `Dockerfile.runpod` dans ton repo :

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py /app/app.py

# Expose port
EXPOSE 7860

# Run
CMD ["python", "/app/app.py"]
```

Puis dans RunPod, utilise ton repo Git comme source au lieu du template.

---

## 💰 Coûts RunPod

**Pour le 26 novembre (démo 3h) :**
- **A10G :** $1.00/h × 3h = **$3.00** (+ 10min de chargement = ~$0.17) = **~$3.20**
- **T4 :** $0.30/h × 3h = **$0.90** (+ 10min = ~$0.05) = **~$0.95**

**Recommandation :** A10G pour plus de marge (24GB VRAM) = **$3-4 pour la démo complète**

**Important :** Tu peux **arrêter le pod immédiatement** après la démo pour éviter les coûts.

---

## 🔄 Plan d'Urgence (si Space HF ne démarre pas)

**Temps estimé : 25-30 minutes**

1. **RunPod : Créer template** (5 min) ✅ Ou utiliser template pré-créé
2. **RunPod : Créer pod A10G** (2 min)
3. **Attendre chargement modèle** (10 min)
4. **Tester API** (2 min)
5. **Mettre à jour Netlify** (2 min)
6. **Redéployer Netlify** (2 min)
7. ✅ **Démo opérationnelle**

---

## 📝 Notes Importantes

### Configuration du modèle

Le pod va utiliser le même code que le Space HF :
- Qwen 14B + LoRA Spinoza
- Gradio avec API `/chat_function`
- Même configuration que `app_spinoza_seul.py` ou `app.py`

### Variables d'environnement

Si tu utilises des secrets (HF_TOKEN, etc.) :
1. RunPod Dashboard → **Pods** → Ton pod → **Edit**
2. Section **"Environment Variables"**
3. Ajouter :
   ```
   HF_TOKEN=ton_token_hf
   ```

### Persistance du modèle

- Le modèle sera téléchargé à chaque démarrage (10 min)
- Pour éviter ça, utiliser un **Volume Disk** (persistant)
- Mais pour une démo ponctuelle, c'est OK de le retélécharger

---

## 🆘 Troubleshooting

### Pod ne démarre pas
- Vérifier les logs : **Pods** → Ton pod → **Logs**
- Vérifier que le template est correct
- Essayer un GPU différent

### API ne répond pas
- Vérifier que le port 7860 est bien mappé
- Vérifier les logs du pod
- Tester directement l'URL publique dans un navigateur

### Modèle ne charge pas
- Vérifier la VRAM disponible (logs)
- Essayer T4 si A10G indisponible
- Vérifier que HF_TOKEN est bien configuré

---

## ✅ Checklist de Repli

- [ ] Compte RunPod créé et crédité
- [ ] Template créé (ou Dockerfile prêt)
- [ ] Test une fois si possible (~$1)
- [ ] Variables Netlify prêtes (`SNB_BACKEND_URL`)
- [ ] Guide RunPod imprimé/sauvegardé

**Si problème HF le 26 novembre :**
- [ ] Créer pod RunPod A10G
- [ ] Attendre chargement (10 min)
- [ ] Tester API
- [ ] Mettre à jour Netlify
- [ ] Redéployer Netlify
- [ ] ✅ Démo opérationnelle

---

**Temps total de repli : 25-30 minutes** ⚡


