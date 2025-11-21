# 🔄 Commandes Colab - Push Notebook vers GitHub

**À copier-coller dans des cellules Colab**

---

## 📍 Étape 1 : Trouver le notebook dans Colab

```python
# Trouver où est le notebook
!find /content -name "RAG_Spinoza_secours.ipynb" 2>/dev/null
!ls -la /content/*.ipynb 2>/dev/null
```

---

## 📥 Étape 2 : Cloner le repo (si pas déjà fait)

```python
# Cloner le repo
!git clone https://github.com/FJDaz/Spinoza_secours.git
%cd Spinoza_secours

# Vérifier
!pwd
!ls -la
```

---

## ⚙️ Étape 3 : Configurer Git

```python
# Configurer Git avec ton identité
!git config user.name "FJDaz"
!git config user.email "FJDaz@users.noreply.github.com"

# Vérifier la config
!git config --list | grep user
```

---

## 🔐 Étape 4 : Configurer l'authentification GitHub

### Option A : Avec token (recommandé)

```python
from google.colab import userdata

# Récupérer le token depuis Secrets (configure-le dans 🔑 Secrets)
GITHUB_TOKEN = userdata.get('GITHUB_TOKEN')

if GITHUB_TOKEN:
    # Configurer remote avec token
    !git remote set-url origin https://{GITHUB_TOKEN}@github.com/FJDaz/Spinoza_secours.git
    print("✅ Remote configuré avec token")
else:
    print("⚠️ Configure GITHUB_TOKEN dans Colab Secrets")
    print("   GitHub → Settings → Developer settings → Personal access tokens")
```

### Option B : HTTPS normal (demandera credentials)

```python
# Configurer remote
!git remote set-url origin https://github.com/FJDaz/Spinoza_secours.git

# Vérifier
!git remote -v
```

---

## 📋 Étape 5 : Copier le notebook dans le repo

```python
%cd /content/Spinoza_secours

# Si le notebook est dans /content (remplace par le vrai chemin trouvé à l'étape 1)
!cp /content/RAG_Spinoza_secours.ipynb .

# OU si le notebook est ailleurs, utilise le chemin trouvé :
# !cp /content/chemin/vers/RAG_Spinoza_secours.ipynb .

# Vérifier
!ls -la RAG_Spinoza_secours.ipynb
```

---

## ✅ Étape 6 : Vérifier les changements

```python
%cd /content/Spinoza_secours

# Vérifier le statut
!git status

# Voir les différences (optionnel)
!git diff RAG_Spinoza_secours.ipynb | head -50
```

---

## 🚀 Étape 7 : Commit et Push

```python
%cd /content/Spinoza_secours

# Ajouter le notebook
!git add RAG_Spinoza_secours.ipynb

# Commit
!git commit -m "Update: Notebook avec cellule Maïeuthon"

# Push
!git push origin main

print("✅ Notebook poussé sur GitHub !")
```

---

## 🔍 Vérification finale

```python
# Vérifier que le push a fonctionné
!git log --oneline -3

# Vérifier le remote
!git remote -v
```

---

## ⚠️ En cas d'erreur

### Erreur : "fatal: could not read Username"

**Solution :** Utilise un token GitHub (Option A de l'étape 4)

### Erreur : "nothing to commit"

**Vérifier :**
```python
!git status
!git diff RAG_Spinoza_secours.ipynb
```

Si vraiment rien à committer, le notebook est déjà à jour.

### Erreur : "fatal: not a git repository"

**Solution :**
```python
%cd /content/Spinoza_secours
!git status
```

---

## 📝 Script complet (tout-en-un)

```python
# =============================================================================
# 🔄 Push Notebook depuis Colab - Script complet
# =============================================================================

from google.colab import userdata
import os

# 1. Aller dans le repo (ou cloner si nécessaire)
try:
    %cd /content/Spinoza_secours
    !git status
except:
    !git clone https://github.com/FJDaz/Spinoza_secours.git
    %cd Spinoza_secours

# 2. Configurer Git
!git config user.name "FJDaz"
!git config user.email "FJDaz@users.noreply.github.com"

# 3. Authentification avec token
try:
    GITHUB_TOKEN = userdata.get('GITHUB_TOKEN')
    if GITHUB_TOKEN:
        !git remote set-url origin https://{GITHUB_TOKEN}@github.com/FJDaz/Spinoza_secours.git
        print("✅ Authentification configurée")
except:
    print("⚠️ Pas de token - utilise HTTPS normal")

# 4. Copier le notebook (ajuste le chemin si nécessaire)
!cp /content/RAG_Spinoza_secours.ipynb . 2>/dev/null || echo "Notebook déjà dans le repo ou chemin différent"

# 5. Vérifier changements
print("\n📋 Statut Git :")
!git status

# 6. Commit et push
!git add RAG_Spinoza_secours.ipynb
!git commit -m "Update: Notebook depuis Colab"
!git push origin main

print("\n✅ Terminé !")
```

---

**Note :** Ajuste les chemins selon où se trouve ton notebook dans Colab.

