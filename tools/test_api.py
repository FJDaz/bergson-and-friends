#!/usr/bin/env python3
"""
Script de diagnostic pour tester l'API du HF Space Spinoza
"""
import requests
import json
import os
from typing import Dict, Any

SPACE_URL = "https://fjdaz-bergsonandfriends.hf.space"
HF_TOKEN = os.getenv("HF_TOKEN", "")

def print_section(title: str):
    """Affiche une section avec style"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_root():
    """Test GET / pour vérifier si le Space est accessible"""
    print_section("Test 1: GET /")

    try:
        response = requests.get(SPACE_URL, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")

        if response.status_code == 200:
            print("✅ Space accessible")
            return True
        else:
            print(f"❌ Status inattendu: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_docs():
    """Test GET /docs pour vérifier la documentation FastAPI"""
    print_section("Test 2: GET /docs (FastAPI docs)")

    try:
        response = requests.get(f"{SPACE_URL}/docs", timeout=10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("✅ Docs FastAPI accessibles")
            return True
        else:
            print(f"⚠️  Pas de docs FastAPI (normal pour Gradio pur)")
            return False

    except Exception as e:
        print(f"⚠️  Erreur: {str(e)}")
        return False

def test_config():
    """Test GET /config pour récupérer la config Gradio"""
    print_section("Test 3: GET /config (Gradio config)")

    headers = {}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"

    try:
        response = requests.get(f"{SPACE_URL}/config", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            config = response.json()
            print("✅ Config Gradio récupérée")

            # Afficher les endpoints disponibles
            if "dependencies" in config:
                print("\n📋 Dependencies (endpoints) disponibles:")
                for dep in config["dependencies"]:
                    api_name = dep.get("api_name")
                    targets = dep.get("targets", [])
                    print(f"  - {api_name}: targets={targets}")

            return config
        else:
            print(f"❌ Échec: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None

def test_api_predict(endpoint: str):
    """Test POST /api/predict/{endpoint}"""
    print_section(f"Test 4: POST /api/predict/{endpoint}")

    headers = {
        "Content-Type": "application/json"
    }
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"

    payload = {
        "data": [
            "La liberté est-elle une illusion ?",  # message
            []  # history
        ]
    }

    url = f"{SPACE_URL}/api/predict/{endpoint}"

    try:
        print(f"URL: {url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"\nStatus: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")

        if response.status_code == 200:
            data = response.json()
            print("✅ Réponse reçue!")
            print(f"\nRéponse: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
            return data
        else:
            print(f"❌ Échec: {response.status_code}")
            print(f"Body: {response.text[:500]}")
            return None

    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None

def test_gradio_client():
    """Test avec gradio_client Python"""
    print_section("Test 5: gradio_client Python")

    try:
        from gradio_client import Client

        print(f"Connexion à {SPACE_URL}...")
        client = Client(SPACE_URL, hf_token=HF_TOKEN if HF_TOKEN else None)

        print("✅ Client connecté")

        # Essayer de prédire
        print("\nTest predict avec /chat_function...")
        result = client.predict(
            message="La liberté est-elle une illusion ?",
            history=[],
            api_name="/chat_function"
        )

        print(f"✅ Réponse reçue: {result}")
        return result

    except ImportError:
        print("⚠️  gradio_client non installé (pip install gradio-client)")
        return None
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None

def main():
    """Exécute tous les tests de diagnostic"""
    print("\n" + "="*60)
    print("  🔍 DIAGNOSTIC HF SPACE SPINOZA")
    print("="*60)
    print(f"\nSpace: {SPACE_URL}")
    print(f"HF Token: {'Configuré ✅' if HF_TOKEN else 'Non configuré ⚠️'}")

    # Test 1: Root
    test_root()

    # Test 2: Docs
    test_docs()

    # Test 3: Config
    config = test_config()

    # Test 4: API predict
    if config and "dependencies" in config:
        # Essayer tous les endpoints détectés
        for dep in config["dependencies"]:
            api_name = dep.get("api_name", "").lstrip("/")
            if api_name:
                test_api_predict(api_name)
    else:
        # Essayer les endpoints courants
        for endpoint in ["chat_function", "predict", "chat"]:
            test_api_predict(endpoint)

    # Test 5: Gradio client
    test_gradio_client()

    print_section("FIN DU DIAGNOSTIC")

if __name__ == "__main__":
    main()
