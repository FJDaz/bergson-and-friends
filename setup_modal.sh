#!/bin/bash
# Script pour configurer Modal et créer le secret HF_TOKEN

set -e

echo "============================================================"
echo "  🚀 Configuration Modal pour Spinoza Chatbot"
echo "============================================================"
echo ""

# 1. Vérifier si Modal est installé
if ! command -v modal &> /dev/null; then
    echo "❌ Modal n'est pas installé"
    echo "   Installation: pip3 install modal"
    exit 1
fi

echo "✅ Modal CLI installé (version: $(modal --version | cut -d' ' -f4))"
echo ""

# 2. Authentification Modal
echo "📝 Étape 1/3 : Authentification Modal"
echo "   Cette commande va ouvrir votre navigateur..."
echo ""
read -p "Appuyez sur Entrée pour continuer..."

modal token new || {
    echo "❌ Échec de l'authentification Modal"
    exit 1
}

echo ""
echo "✅ Authentification réussie!"
echo ""

# 3. Vérifier si le secret existe déjà
echo "📝 Étape 2/3 : Vérification des secrets existants"
echo ""

if modal secret list 2>/dev/null | grep -q "hf-token"; then
    echo "✅ Le secret 'hf-token' existe déjà!"
    echo ""
    read -p "Voulez-vous le recréer ? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "⏭️  Conservation du secret existant"
        echo ""
        echo "============================================================"
        echo "  ✅ Configuration terminée!"
        echo "============================================================"
        echo ""
        echo "Prochaine étape : Tester l'application"
        echo "  modal run modal_spinoza.py --question \"Test\""
        echo ""
        exit 0
    fi
fi

# 4. Créer le secret
echo ""
echo "📝 Étape 3/3 : Création du secret HF_TOKEN"
echo ""
echo "Où trouver votre HF_TOKEN :"
echo "  1. Hugging Face : https://huggingface.co/settings/tokens"
echo "  2. Netlify Dashboard : Site settings → Environment variables"
echo ""
read -p "Entrez votre HF_TOKEN (commence par 'hf_'): " HF_TOKEN_VALUE

if [[ ! $HF_TOKEN_VALUE =~ ^hf_ ]]; then
    echo "⚠️  Attention : le token ne commence pas par 'hf_'"
    read -p "Continuer quand même ? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "Création du secret..."
modal secret create hf-token HF_TOKEN="$HF_TOKEN_VALUE" || {
    echo "❌ Échec de la création du secret"
    exit 1
}

echo ""
echo "============================================================"
echo "  ✅ Configuration terminée avec succès!"
echo "============================================================"
echo ""
echo "Prochaines étapes :"
echo "  1. Tester : modal run modal_spinoza.py --question \"Test\""
echo "  2. Déployer : modal deploy modal_spinoza.py"
echo ""
