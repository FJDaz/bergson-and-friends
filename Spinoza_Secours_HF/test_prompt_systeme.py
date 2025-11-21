"""
Script de Test Prompt Système - Option 1
Teste le prompt système hybride SANS charger le modèle ni l'API
Prêt à copier-coller dans Colab
"""

# =============================================================================
# IMPORTS
# =============================================================================

import re
from typing import Dict, List

# =============================================================================
# PROMPT SYSTÈME HYBRIDE (depuis prompt_systeme_hybride.py)
# =============================================================================

SYSTEM_PROMPT_SPINOZA = """Tu ES Spinoza incarné. Tu dialogues avec un élève de Terminale en première personne.

STYLE SPINOZIEN :
- Géométrie des affects : révèle causes nécessaires, déduis
- Dieu = Nature
- Vocabulaire : conatus, affects, puissance d'agir, servitude

SCHÈMES LOGIQUES :
- Identité : Liberté = Connaissance nécessité
- Causalité : Tout a cause nécessaire
- Implication : Joie → augmentation puissance

MÉTHODE :
1. Révèle nécessité causale
2. Distingue servitude (ignorance) vs liberté (connaissance)
3. Exemples concrets modernes

TRANSITIONS (VARIE) :
- "Donc", "mais alors", "Imagine", "Cela implique"
- "Pourtant", "Sauf que", "C'est contradictoire"

RÈGLES :
- Tutoie (tu/ton/ta)
- Concis (2-3 phrases MAX)
- Questionne au lieu d'affirmer
- Ne parle JAMAIS de toi à la 3ème personne. Tu ES Spinoza."""

INSTRUCTIONS_CONTEXTUELLES = {
    "confusion": "L'élève est confus → Donne UNE analogie concrète simple en utilisant tes schèmes logiques.",
    "resistance": "L'élève résiste → Révèle contradiction avec 'mais alors' et tes schèmes logiques.",
    "accord": "L'élève est d'accord → Valide puis AVANCE logiquement avec 'Donc' et tes schèmes logiques.",
    "neutre": "Élève neutre → Pose question pour faire réfléchir en utilisant tes schèmes logiques."
}

INSTRUCTION_RAG = """
UTILISATION CONNAISSANCES :
- Tu connais l'Éthique de Spinoza
- Cite implicitement ("comme je l'ai montré...", "dans mon œuvre...")
- Reformule dans TON style (première personne, lycéen)
- Ne récite pas : extrais idées et reformule naturellement
"""

def construire_prompt_complet(contexte: str, use_rag_instruction: bool = True) -> str:
    """
    Construit le prompt complet optimisé
    
    Args:
        contexte: "accord", "confusion", "resistance", "neutre"
        use_rag_instruction: Si True, ajoute instructions RAG
    
    Returns:
        Prompt système complet (~250-300 tokens)
    """
    prompt = SYSTEM_PROMPT_SPINOZA
    
    # Ajouter instruction contextuelle
    if contexte in INSTRUCTIONS_CONTEXTUELLES:
        prompt += f"\n\n{INSTRUCTIONS_CONTEXTUELLES[contexte]}"
    
    # Ajouter instruction RAG (optionnel)
    if use_rag_instruction:
        prompt += f"\n\n{INSTRUCTION_RAG}"
    
    return prompt

# =============================================================================
# FONCTIONS DE TEST
# =============================================================================

def estimer_tokens(prompt: str) -> int:
    """
    Estime le nombre de tokens (approximation : 1 token ≈ 0.75 mots)
    """
    mots = len(prompt.split())
    tokens_estimes = int(mots * 1.3)  # Approximation conservatrice
    return tokens_estimes

def valider_structure(prompt: str) -> Dict[str, bool]:
    """
    Valide que le prompt contient les éléments requis
    """
    validations = {
        "premiere_personne": "Tu ES Spinoza" in prompt or "première personne" in prompt.lower(),
        "schemes_logiques": "SCHÈMES LOGIQUES" in prompt or "schèmes" in prompt.lower(),
        "transitions": "mais alors" in prompt.lower() or "Donc" in prompt.lower(),
        "tutoie": "Tutoie" in prompt or "tu/ton/ta" in prompt,
        "concis": "Concis" in prompt or "2-3 phrases" in prompt,
        "questionne": "Questionne" in prompt or "question" in prompt.lower(),
        "ne_parle_pas_3eme": "Ne parle JAMAIS de toi à la 3ème personne" in prompt or "3ème personne" in prompt.lower()
    }
    return validations

def afficher_prompt(contexte: str, use_rag_instruction: bool = True) -> None:
    """
    Affiche le prompt généré pour un contexte donné
    """
    prompt = construire_prompt_complet(contexte, use_rag_instruction)
    tokens = estimer_tokens(prompt)
    validations = valider_structure(prompt)
    
    print("=" * 80)
    print(f"📋 CONTEXTE: {contexte.upper()}")
    print(f"📊 Tokens estimés: {tokens}")
    print(f"✅ Validations: {sum(validations.values())}/{len(validations)}")
    print("=" * 80)
    print("\n📝 PROMPT GÉNÉRÉ:\n")
    print(prompt)
    print("\n" + "=" * 80)
    print("\n🔍 DÉTAILS VALIDATIONS:")
    for key, value in validations.items():
        status = "✅" if value else "❌"
        print(f"  {status} {key}: {value}")
    print("=" * 80 + "\n")

def test_prompt_contextes(use_rag_instruction: bool = True) -> Dict[str, Dict]:
    """
    Teste le prompt système avec tous les contextes
    Retourne un dictionnaire avec les résultats
    """
    contextes = ["accord", "confusion", "resistance", "neutre"]
    resultats = {}
    
    print("🧪 TEST PROMPT SYSTÈME - TOUS LES CONTEXTES\n")
    print(f"RAG Instructions: {'✅ Activé' if use_rag_instruction else '❌ Désactivé'}\n")
    
    for contexte in contextes:
        prompt = construire_prompt_complet(contexte, use_rag_instruction)
        tokens = estimer_tokens(prompt)
        validations = valider_structure(prompt)
        
        resultats[contexte] = {
            "prompt": prompt,
            "tokens": tokens,
            "validations": validations,
            "validations_ok": sum(validations.values()),
            "validations_total": len(validations)
        }
        
        # Afficher pour chaque contexte
        afficher_prompt(contexte, use_rag_instruction)
    
    # Résumé global
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ GLOBAL")
    print("=" * 80)
    print(f"{'Contexte':<15} {'Tokens':<10} {'Validations':<15}")
    print("-" * 80)
    for contexte, resultat in resultats.items():
        validations_str = f"{resultat['validations_ok']}/{resultat['validations_total']}"
        print(f"{contexte:<15} {resultat['tokens']:<10} {validations_str:<15}")
    
    tokens_moyen = sum(r['tokens'] for r in resultats.values()) / len(resultats)
    print("-" * 80)
    print(f"{'MOYENNE':<15} {int(tokens_moyen):<10}")
    print("=" * 80 + "\n")
    
    return resultats

def comparer_avec_rag(contexte: str = "confusion") -> None:
    """
    Compare le prompt avec et sans instructions RAG
    """
    print("=" * 80)
    print(f"🔄 COMPARAISON AVEC/SANS RAG - Contexte: {contexte.upper()}")
    print("=" * 80)
    
    print("\n📝 AVEC RAG Instructions:")
    print("-" * 80)
    prompt_avec = construire_prompt_complet(contexte, use_rag_instruction=True)
    tokens_avec = estimer_tokens(prompt_avec)
    print(f"Tokens: {tokens_avec}")
    print(f"Longueur: {len(prompt_avec)} caractères")
    
    print("\n📝 SANS RAG Instructions:")
    print("-" * 80)
    prompt_sans = construire_prompt_complet(contexte, use_rag_instruction=False)
    tokens_sans = estimer_tokens(prompt_sans)
    print(f"Tokens: {tokens_sans}")
    print(f"Longueur: {len(prompt_sans)} caractères")
    
    economie = tokens_avec - tokens_sans
    print(f"\n💰 Économie sans RAG: {economie} tokens ({economie/tokens_avec*100:.1f}%)")
    print("=" * 80 + "\n")

def tester_detection_contexte() -> None:
    """
    Teste la fonction de détection de contexte avec des exemples
    """
    print("=" * 80)
    print("🧪 TEST DÉTECTION CONTEXTE")
    print("=" * 80 + "\n")
    
    def detecter_contexte(user_input: str) -> str:
        """Détecte le contexte de la réponse utilisateur"""
        text_lower = user_input.lower()
        
        # Accord
        if any(word in text_lower for word in ['oui', 'd\'accord', 'exact', 'ok', 'voilà', 'tout à fait']):
            return "accord"
        
        # Confusion
        if any(phrase in text_lower for phrase in ['comprends pas', 'vois pas', 'c\'est quoi', 'je sais pas', 'pourquoi', 'rapport']):
            return "confusion"
        
        # Résistance
        if any(word in text_lower for word in ['mais', 'non', 'pas d\'accord', 'faux', 'n\'importe quoi', 'je peux']):
            return "resistance"
        
        return "neutre"
    
    exemples = [
        ("Oui, je suis d'accord", "accord"),
        ("Je comprends pas", "confusion"),
        ("Mais non, je peux faire ce que je veux", "resistance"),
        ("La liberté est importante", "neutre"),
        ("D'accord, mais alors...", "accord"),  # "d'accord" détecté en premier
        ("C'est quoi la causalité ?", "confusion"),
        ("Je ne suis pas d'accord", "resistance"),
    ]
    
    print(f"{'Message':<40} {'Contexte détecté':<20} {'Attendu':<15} {'Status'}")
    print("-" * 80)
    
    for message, attendu in exemples:
        detecte = detecter_contexte(message)
        status = "✅" if detecte == attendu else "❌"
        print(f"{message:<40} {detecte:<20} {attendu:<15} {status}")
    
    print("=" * 80 + "\n")

def analyser_mots_cles(prompt: str) -> Dict[str, int]:
    """
    Analyse les mots-clés importants dans le prompt
    """
    mots_cles = {
        "spinoza": prompt.lower().count("spinoza"),
        "première personne": prompt.lower().count("première personne") + prompt.lower().count("premiere personne"),
        "schème": prompt.lower().count("schème") + prompt.lower().count("scheme"),
        "mais alors": prompt.lower().count("mais alors"),
        "donc": prompt.lower().count("donc"),
        "tutoie": prompt.lower().count("tutoie") + prompt.lower().count("tu/ton/ta"),
        "concis": prompt.lower().count("concis"),
        "questionne": prompt.lower().count("questionne"),
    }
    return mots_cles

def analyser_prompt_detail(contexte: str) -> None:
    """
    Analyse détaillée d'un prompt pour un contexte donné
    """
    prompt = construire_prompt_complet(contexte, use_rag_instruction=True)
    mots_cles = analyser_mots_cles(prompt)
    
    print("=" * 80)
    print(f"🔍 ANALYSE DÉTAILLÉE - Contexte: {contexte.upper()}")
    print("=" * 80)
    print(f"\n📊 Statistiques:")
    print(f"  Tokens estimés: {estimer_tokens(prompt)}")
    print(f"  Caractères: {len(prompt)}")
    print(f"  Mots: {len(prompt.split())}")
    print(f"  Lignes: {len(prompt.splitlines())}")
    
    print(f"\n🔑 Mots-clés:")
    for mot, count in mots_cles.items():
        if count > 0:
            print(f"  - '{mot}': {count} occurrence(s)")
    
    print(f"\n📝 Sections:")
    sections = ["STYLE SPINOZIEN", "SCHÈMES LOGIQUES", "MÉTHODE", "TRANSITIONS", "RÈGLES"]
    for section in sections:
        present = section in prompt
        print(f"  {'✅' if present else '❌'} {section}")
    
    print("=" * 80 + "\n")

# =============================================================================
# EXÉCUTION
# =============================================================================

if __name__ == "__main__":
    print("🚀 Script de Test Prompt Système - Option 1\n")
    
    # Test 1: Tous les contextes avec RAG
    print("=" * 80)
    print("TEST 1: TOUS LES CONTEXTES (avec RAG)")
    print("=" * 80 + "\n")
    resultats_avec_rag = test_prompt_contextes(use_rag_instruction=True)
    
    # Test 2: Comparaison avec/sans RAG
    print("\n" + "=" * 80)
    print("TEST 2: COMPARAISON AVEC/SANS RAG")
    print("=" * 80 + "\n")
    comparer_avec_rag("confusion")
    
    # Test 3: Tous les contextes sans RAG (si besoin)
    print("\n" + "=" * 80)
    print("TEST 3: TOUS LES CONTEXTES (sans RAG)")
    print("=" * 80 + "\n")
    resultats_sans_rag = test_prompt_contextes(use_rag_instruction=False)
    
    # Test 4: Détection contexte
    print("\n" + "=" * 80)
    print("TEST 4: DÉTECTION CONTEXTE")
    print("=" * 80 + "\n")
    tester_detection_contexte()
    
    # Test 5: Analyse détaillée (exemple confusion)
    print("\n" + "=" * 80)
    print("TEST 5: ANALYSE DÉTAILLÉE (exemple)")
    print("=" * 80 + "\n")
    analyser_prompt_detail("confusion")
    
    print("✅ Tests terminés !")

# =============================================================================
# UTILISATION DANS COLAB
# =============================================================================

"""
ORDRE RECOMMANDÉ DANS COLAB :

1. CELLULE 1 : Installation dépendances
   !pip install -q ...

2. CELLULE 2 : Imports + Prompt système (ce script)
   # Copier-coller tout ce script
   # Exécuter pour tester le prompt AVANT de charger le modèle

3. CELLULE 3 : Chargement modèle
   model, tokenizer = load_model()

4. CELLULE 4 : API FastAPI + ngrok
   # Code API avec spinoza_repond() qui utilise le prompt testé

AVANTAGE : Tester le prompt d'abord (rapide) avant de charger le modèle (lent)
"""

