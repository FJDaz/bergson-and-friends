#!/usr/bin/env python3
"""
Test local des fonctions de modal_spinoza.py sans Modal
Teste uniquement la détection contextuelle et le post-processing
"""
import sys
import os

# Importer les fonctions depuis modal_spinoza
sys.path.insert(0, os.path.dirname(__file__))

# Simuler les imports pour éviter l'erreur Modal
import re
import random

# Copier les fonctions de détection
def detecter_oui_explicite(user_input: str) -> bool:
    patterns = [
        r'\boui\b', r'\byep\b', r'\byes\b', r'\bexact\b',
        r'\bd\'accord\b', r'\bok\b', r'\btout à fait\b',
        r'\bc\'est ça\b', r'\bvoilà\b'
    ]
    text_lower = user_input.lower()
    return any(re.search(pattern, text_lower) for pattern in patterns)

def detecter_confusion(user_input: str) -> bool:
    patterns = [
        r'comprends? pas', r'vois pas', r'c\'est quoi',
        r'je sais pas', r'j\'en sais rien', r'pourquoi',
        r'rapport', r'quel lien', r'chelou', r'dingue'
    ]
    text_lower = user_input.lower()
    return any(re.search(pattern, text_lower) for pattern in patterns)

def detecter_resistance(user_input: str) -> bool:
    patterns = [
        r'\bmais\b', r'\bnon\b', r'pas d\'accord', r'faux',
        r'n\'importe quoi', r'pas vrai', r'je peux',
        r'bullshit', r'chiant'
    ]
    text_lower = user_input.lower()
    return any(re.search(pattern, text_lower) for pattern in patterns)

def detecter_contexte(user_input: str) -> str:
    """Détecte contexte selon logique V2 succès"""
    if detecter_oui_explicite(user_input):
        return "accord"
    elif detecter_confusion(user_input):
        return "confusion"
    elif detecter_resistance(user_input):
        return "resistance"
    else:
        return "neutre"

def nettoyer_reponse(text: str) -> str:
    """Code exact succès V2"""
    # Annotations méta
    text = re.sub(r'\([^)]*[Aa]ttends[^)]*\)', '', text)
    text = re.sub(r'\([^)]*[Pp]oursuis[^)]*\)', '', text)
    text = re.sub(r'\([^)]*[Dd]onne[^)]*\)', '', text)

    # Emojis
    text = re.sub(r'[😀-🙏🌀-🗿🚀-🛿]', '', text)

    # Nettoyer espaces
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\s+([.!?])', r'\1', text)

    return text

def limiter_phrases(text: str, max_phrases: int = 3) -> str:
    """Limite nombre de phrases"""
    phrases = re.split(r'[.!?]+\s+', text)
    phrases = [p.strip() for p in phrases if p.strip()]

    if len(phrases) <= max_phrases:
        return text

    return '. '.join(phrases[:max_phrases]) + '.'

# ============================================
# TESTS
# ============================================

def test_detection_contexte():
    """Test de la détection contextuelle"""
    print("=" * 60)
    print("  TEST : Détection Contextuelle")
    print("=" * 60)

    test_cases = [
        ("Oui je suis d'accord", "accord"),
        ("Oui tout à fait", "accord"),
        ("Je comprends pas", "confusion"),
        ("C'est quoi le rapport ?", "confusion"),
        ("Mais non c'est faux", "resistance"),
        ("Je peux pas accepter ça", "resistance"),
        ("La liberté est-elle une illusion ?", "neutre"),
        ("Qu'est-ce que la vérité ?", "neutre"),
    ]

    for phrase, expected in test_cases:
        detected = detecter_contexte(phrase)
        status = "✅" if detected == expected else "❌"
        print(f"{status} '{phrase}' -> {detected} (attendu: {expected})")

def test_post_processing():
    """Test du post-processing"""
    print("\n" + "=" * 60)
    print("  TEST : Post-processing")
    print("=" * 60)

    test_cases = [
        (
            "Voici ma réponse (Attends je réfléchis). C'est important !",
            "Voici ma réponse. C'est important!"
        ),
        (
            "Test 😀 avec emoji 🌀",
            "Test avec emoji"
        ),
        (
            "Phrase   avec    espaces    multiples  .",
            "Phrase avec espaces multiples."
        ),
    ]

    for text, expected in test_cases:
        cleaned = nettoyer_reponse(text)
        status = "✅" if cleaned.strip() == expected.strip() else "❌"
        print(f"{status}")
        print(f"  Input:    '{text}'")
        print(f"  Output:   '{cleaned}'")
        print(f"  Expected: '{expected}'")
        print()

def test_limiter_phrases():
    """Test de limitation de phrases"""
    print("=" * 60)
    print("  TEST : Limitation de phrases")
    print("=" * 60)

    long_text = "Première phrase. Deuxième phrase. Troisième phrase. Quatrième phrase. Cinquième phrase."
    limited = limiter_phrases(long_text, 3)

    print(f"Input:  {long_text}")
    print(f"Output: {limited}")
    print(f"Phrases: {len(limited.split('.'))} (attendu: 4 avec le point final)")

def main():
    """Exécute tous les tests locaux"""
    print("\n🧪 TESTS LOCAUX - modal_spinoza.py\n")

    test_detection_contexte()
    test_post_processing()
    test_limiter_phrases()

    print("\n" + "=" * 60)
    print("  ✅ Tests terminés")
    print("=" * 60)
    print("\nNote: Ces tests vérifient uniquement les fonctions utilitaires.")
    print("Pour tester le modèle complet, utilisez: modal run modal_spinoza.py")

if __name__ == "__main__":
    main()
