# 🎭 Interface à Trois Philosophes - Localisation

**Date :** 19 novembre 2025

---

## 📍 Localisation

### Interface Principale

**Fichier :** `/Users/francois-jeandazin/bergsonAndFriends/index.html`

**Description :** Interface HTML complète avec les trois philosophes (Bergson, Kant, Spinoza)

**Caractéristiques :**
- ✅ Version desktop avec 3 sections (bergson, kant, spinoza)
- ✅ Version mobile responsive
- ✅ Charge `app.js` pour la logique JavaScript
- ✅ Utilise les assets depuis `https://fjdaz.com/bergson/statics/`

### JavaScript Associé

**Fichier :** `/Users/francois-jeandazin/bergsonAndFriends/app.js`

**Description :** Logique JavaScript pour gérer les trois philosophes

**Fonctionnalités :**
- ✅ Gestion des états pour chaque philosophe (`bergson`, `kant`, `spinoza`)
- ✅ Initialisation des conversations
- ✅ Appels API backend (Railway)
- ✅ Gestion de l'historique par philosophe

**Configuration API :**
```javascript
const API_BASE_URL = 'https://bergson-api-production.up.railway.app';
```

**Philosophes gérés :**
```javascript
const philosopherStates = {
  bergson: { history: [], active: false },
  kant: { history: [], active: false },
  spinoza: { history: [], active: false }
};
```

---

## 📁 Autres Copies

### 1. Space HF

**Fichier :** `/Users/francois-jeandazin/bergsonAndFriends/bergsonAndFriends_HF/index.html`

**Description :** Copie de l'interface dans le dossier du Space HF

**Usage :** Utilisé par le Space Hugging Face `FJDaz/bergsonAndFriends`

### 2. Static

**Fichier :** `/Users/francois-jeandazin/bergsonAndFriends/static/index.html`

**Description :** Copie dans le dossier static

**Usage :** Possiblement pour déploiement statique

---

## 🔗 Structure HTML

### Desktop Version

```html
<section class="philosophers">
  <article class="philosopher" id="bergson">...</article>
  <article class="philosopher" id="kant">...</article>
  <article class="philosopher" id="spinoza">...</article>
</section>
```

### Mobile Version

```html
<section class="mobile-philosophers">
  <article class="mobile-philosopher" id="mobile-bergson">...</article>
  <article class="mobile-philosopher" id="mobile-kant">...</article>
  <article class="mobile-philosopher" id="mobile-spinoza">...</article>
</section>
```

---

## 🎯 Interface Active

**Interface principale utilisée :** `/Users/francois-jeandazin/bergsonAndFriends/index.html`

**Backend :** Railway (`https://bergson-api-production.up.railway.app`)

**Frontend :** Netlify ou fjdaz.com (à vérifier)

---

**Dernière mise à jour :** 19 novembre 2025

