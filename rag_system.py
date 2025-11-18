"""
Système RAG (Retrieval-Augmented Generation) pour Bergson and Friends
Port Python du rag_system.js
"""
from pathlib import Path
from typing import List, Dict
import re

# Mapping des fichiers corpus par philosophe
CORPUS_FILES = {
    "spinoza": "Corpus Spinoza Dialogique 18k - Éthique II-IV.md",
    "bergson": "corpus_bergson_27k_dialogique.md",
    "kant": "corpus_kant_20k.txt.md",
}

GLOSSAIRE_FILES = {
    "spinoza": "Glossaire Conversationnel Spinoza - 12 Concepts.md",
    "bergson": "glossaire_bergson_conversationnel.md",
    "kant": "glossaire_kant_conversationnel.md",
}

def load_corpus(philosopher: str) -> Dict[str, str]:
    """Charge le corpus et glossaire pour un philosophe"""
    project_root = Path(__file__).resolve().parent
    rag_dir = project_root / "data" / "RAG"

    corpus_file = CORPUS_FILES.get(philosopher)
    glossaire_file = GLOSSAIRE_FILES.get(philosopher)

    corpus = ""
    glossaire = ""

    if corpus_file:
        corpus_path = rag_dir / corpus_file
        if corpus_path.exists():
            corpus = corpus_path.read_text(encoding="utf-8")

    if glossaire_file:
        glossaire_path = rag_dir / glossaire_file
        if glossaire_path.exists():
            glossaire = glossaire_path.read_text(encoding="utf-8")

    return {"corpus": corpus, "glossaire": glossaire}

def split_into_sections(text: str) -> List[Dict[str, str]]:
    """Découpe un texte markdown en sections (basé sur ## headers)"""
    sections = []
    lines = text.split('\n')
    current_section = {"title": "", "content": ""}

    for line in lines:
        if line.startswith('##'):
            # Sauvegarder la section précédente si elle a du contenu
            if current_section["content"].strip():
                sections.append(current_section)
            # Commencer une nouvelle section
            current_section = {
                "title": re.sub(r'^#+\s*', '', line),
                "content": ""
            }
        else:
            current_section["content"] += line + '\n'

    # Ajouter la dernière section
    if current_section["content"].strip():
        sections.append(current_section)

    return sections

def relevance_score(section: Dict[str, str], concepts: List[str]) -> int:
    """Calcule un score de pertinence basé sur les mots-clés"""
    section_text = (section["title"] + " " + section["content"]).lower()
    score = 0

    for concept in concepts:
        concept_lower = concept.lower()
        # Compter les occurrences
        matches = section_text.count(concept_lower)
        score += matches * 2  # Poids 2 par occurrence

        # Bonus si dans le titre
        if concept_lower in section["title"].lower():
            score += 5

    return score

def rag_lookup(philosopher: str, concepts: List[str], top_k: int = 3) -> List[Dict]:
    """
    Récupère les passages les plus pertinents du corpus

    Args:
        philosopher: "spinoza", "bergson", ou "kant"
        concepts: Liste de mots-clés/concepts à rechercher
        top_k: Nombre de passages à retourner

    Returns:
        Liste de dictionnaires avec title, content, source, score
    """
    data = load_corpus(philosopher)
    corpus = data["corpus"]
    glossaire = data["glossaire"]

    # Découper en sections
    corpus_sections = split_into_sections(corpus)
    glossaire_sections = split_into_sections(glossaire)

    # Marquer la source
    all_sections = []
    for section in glossaire_sections:
        all_sections.append({**section, "source": "glossaire"})
    for section in corpus_sections:
        all_sections.append({**section, "source": "corpus"})

    # Scorer chaque section
    scored = []
    for section in all_sections:
        score = relevance_score(section, concepts)
        scored.append({
            "title": section["title"],
            "content": section["content"].strip()[:800],  # Limiter à 800 chars
            "source": section["source"],
            "score": score
        })

    # Trier par score décroissant
    scored.sort(key=lambda x: x["score"], reverse=True)

    # Retourner les top K
    return scored[:top_k]

def format_rag_context(passages: List[Dict]) -> str:
    """Formatte les passages RAG pour inclusion dans le prompt"""
    if not passages:
        return "Aucun passage spécifique trouvé. Réponds selon ta connaissance philosophique générale."

    context = "Passages pertinents du corpus :\n\n"

    for idx, passage in enumerate(passages, 1):
        context += f"[{idx}] {passage['title']}\n"
        context += f"{passage['content']}\n\n"

    return context

def extract_concepts(user_message: str) -> List[str]:
    """
    Extrait les concepts-clés d'un message utilisateur
    Version simple : mots de 4+ caractères (peut être amélioré)
    """
    # Nettoyer et tokenizer
    words = re.findall(r'\b\w{4,}\b', user_message.lower())

    # Filtrer les mots courants
    stop_words = {
        "pour", "dans", "avec", "sans", "entre", "être", "avoir",
        "faire", "dire", "aller", "voir", "savoir", "pouvoir",
        "cette", "celui", "celle", "ceux", "cela", "quel", "quelle",
        "comment", "pourquoi", "quand", "alors", "mais", "donc"
    }

    concepts = [w for w in words if w not in stop_words]

    # Dédupliquer en préservant l'ordre
    seen = set()
    unique_concepts = []
    for c in concepts:
        if c not in seen:
            seen.add(c)
            unique_concepts.append(c)

    return unique_concepts

if __name__ == "__main__":
    # Test du système RAG
    print("🧪 Test système RAG Spinoza\n")

    # Test 1 : Charger corpus
    print("1. Chargement corpus Spinoza...")
    data = load_corpus("spinoza")
    print(f"   Corpus: {len(data['corpus'])} caractères")
    print(f"   Glossaire: {len(data['glossaire'])} caractères\n")

    # Test 2 : Extraire concepts
    test_message = "La liberté est-elle une illusion ou la joie augmente-t-elle la puissance d'agir ?"
    concepts = extract_concepts(test_message)
    print(f"2. Concepts extraits de: '{test_message}'")
    print(f"   → {concepts}\n")

    # Test 3 : RAG lookup
    print("3. Recherche passages pertinents...")
    passages = rag_lookup("spinoza", concepts, top_k=2)
    for p in passages:
        print(f"   [{p['source']}] {p['title']} (score: {p['score']})")
        print(f"   {p['content'][:100]}...\n")

    # Test 4 : Format context
    print("4. Contexte formaté:")
    context = format_rag_context(passages)
    print(f"   {context[:300]}...")
