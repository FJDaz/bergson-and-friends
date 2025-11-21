# 📚 Documentation du Projet Bergson and Friends

## Structure des Dossiers

```
docs/
├── tutos/             # Guides pas à pas, tutoriels
├── notes/             # Notes rapides, TODO, réflexions
├── references/        # Explications techniques, concepts
├── guides/            # Guides pratiques, procédures
├── analyses/          # Analyses détaillées, bilans
├── tests/             # Documentation des tests
│   └── archives/      # Archives automatiques
├── supports/         # Support technique
└── logs/             # Logs et traces d'exécution
```

## 📁 Contenu par Catégorie

### `docs/tutos/`
Guides pas à pas :
- **create-fastapi-space.md** : Créer un Space FastAPI de test sur HF
- **guide-upload-app-js.md** : Guide pour uploader app.js sur fjdaz.com
- **guide-upload-index-html.md** : Guide pour uploader index.html sur fjdaz.com

### `docs/notes/`
Notes rapides et réflexions :
- **actions-restantes.md** : Actions restantes - 17 Novembre 2025
- **action-finale.md** : Action finale - Uploader les 2 fichiers
- **action-immediate-fjdaz.md** : Action immédiate - Rien ne s'affiche
- **contexte-session-17nov.md** : Résumé de contexte - Session 17 Novembre
- **status-actuel.md** : Status actuel - 17 Novembre 2025

### `docs/references/`
Explications techniques et concepts :
- **methode-meta-skills.md** : Méthode méta pour créer des skills (structure, principes, workflow)
- **prompt-generateur-skills.md** : Prompt complet pour générer automatiquement des skills
- **snb-rag-local.md** : Skill de test SNB + RAG en local (Netlify Functions)
- **repli-backend.md** : Stratégie de repli backend SNB
- **repli-runpod.md** : Plan de repli RunPod - Guide complet
- **spinoza-nb-versions.md** : Archive complète - spinoza_NB - Toutes les versions

### `docs/guides/`
Guides pratiques :
- (À compléter selon besoins)

### `docs/analyses/`
Analyses détaillées et bilans :
- (À compléter selon besoins)

### `docs/tests/`
Documentation des tests :
- **archives/** : Archives automatiques (après 1 jour)

### `docs/supports/`
Support technique :
- **fix-api-url.md** : Fix urgent - Configuration URL API Netlify
- **fix-gradio-client.md** : Fix - Remplacement de @gradio/client
- **fix-mock-netlify.md** : Fix - Désactiver le Mock sur Netlify
- **fix-prompt-systeme.md** : Fix - Prompt Système Complet Utilisé
- **debug-cache.md** : Debug - Problème de Cache ou Chemin
- **debug-fjdaz.md** : Debug - Rien ne s'affiche sur fjdaz.com
- **solution-cache.md** : Solution - Problème de Cache
- **solution-mystere.md** : Solution au Mystère du Cache
- **probleme-upload.md** : Problème - Fichier Uploadé Incomplet
- **trouver-chemin-serveur.md** : Trouver le chemin serveur
- **verification-app-js.md** : Vérification app.js
- **urgent-upload-app-js-v2.md** : Urgent - Upload app.js v2
- **urgent-upload-index-html.md** : Urgent - Upload index.html

### `docs/logs/`
Logs et traces d'exécution :
- **Railway_logs** : Logs du service Railway
- Logs de services (Netlify, HF Spaces, etc.)
- Traces d'erreurs et d'exécution

## 🔄 Archivage Automatique

Les documents de plus de 1 jour dans `docs/tests/` sont automatiquement déplacés vers `docs/tests/archives/` par le script `tools/archive_old_docs.py` (à créer).

## 📝 Conventions

- **Fichiers .md** : Documentation Markdown
- **Noms de fichiers** : En minuscules avec tirets (`-`)
- **Dates** : Format `YYYY-MM-DD` dans les noms de fichiers archivés

## 🎯 Skills Disponibles

### Skills Documentés

1. **snb-rag-local** : Tester SNB + RAG en local
   - **Documentation** : `docs/references/snb-rag-local.md`
   - **Usage** : Test local du système RAG + SNB avec Netlify CLI

### Créer un Nouveau Skill

Suivre la méthode méta documentée dans `docs/references/methode-meta-skills.md` :
1. Créer la documentation dans `docs/references/[nom-skill].md`
2. Créer l'implémentation dans `tools/[nom_skill].py` (ou `.js` selon le projet)
3. **Cursor** peut invoquer automatiquement les skills après actions importantes

## 🔄 Archivage Automatique

Les documents de plus de 1 jour dans `docs/tests/` peuvent être automatiquement archivés par **Cursor** en utilisant le skill `archive-docs-manager` (à créer selon la méthode méta).

