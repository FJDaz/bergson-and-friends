// rag_system.js - Système RAG simple pour récupération passages pertinents
const fs = require('fs');
const path = require('path');

/**
 * Charge un corpus depuis le dossier RAG_clean
 */
function loadCorpus(philosopher) {
    const corpusFiles = {
        bergson: 'corpus_bergson_27k_dialogique_clean.md',
        kant: 'corpus_kant_20k.txt_clean.md',
        spinoza: 'Corpus Spinoza Dialogique 18k - Éthique II-IV_clean.md'
    };

    const glossaireFiles = {
        bergson: 'glossaire_bergson_conversationnel_clean.md',
        kant: 'glossaire_kant_conversationnel_clean.md',
        spinoza: 'Glossaire Conversationnel Spinoza - 12 Concepts_clean.md'
    };

    const ragDir = path.join(__dirname, '../RAG_clean');

    const corpusPath = path.join(ragDir, corpusFiles[philosopher]);
    const glossairePath = path.join(ragDir, glossaireFiles[philosopher]);

    const corpus = fs.existsSync(corpusPath)
        ? fs.readFileSync(corpusPath, 'utf8')
        : '';

    const glossaire = fs.existsSync(glossairePath)
        ? fs.readFileSync(glossairePath, 'utf8')
        : '';

    return { corpus, glossaire };
}

/**
 * Découpe un texte en sections (basé sur les headers markdown ##)
 */
function splitIntoSections(text) {
    const sections = [];
    const lines = text.split('\n');
    let currentSection = { title: '', content: '' };

    for (const line of lines) {
        if (line.startsWith('##')) {
            if (currentSection.content) {
                sections.push(currentSection);
            }
            currentSection = {
                title: line.replace(/^#+\s*/, ''),
                content: ''
            };
        } else {
            currentSection.content += line + '\n';
        }
    }

    if (currentSection.content) {
        sections.push(currentSection);
    }

    return sections;
}

/**
 * Calcule un score de pertinence simple (nombre de mots-clés présents)
 */
function relevanceScore(section, concepts) {
    const sectionLower = (section.title + ' ' + section.content).toLowerCase();
    let score = 0;

    for (const concept of concepts) {
        const conceptLower = concept.toLowerCase();
        // Compter les occurrences
        const matches = sectionLower.split(conceptLower).length - 1;
        score += matches * 2; // Poids 2 par occurrence

        // Bonus si dans le titre
        if (section.title.toLowerCase().includes(conceptLower)) {
            score += 5;
        }
    }

    return score;
}

/**
 * RAG Lookup - Récupère les passages les plus pertinents
 */
function ragLookup(philosopher, concepts, topK = 3) {
    const { corpus, glossaire } = loadCorpus(philosopher);

    // Découper en sections
    const corpusSections = splitIntoSections(corpus);
    const glossaireSections = splitIntoSections(glossaire);

    const allSections = [
        ...glossaireSections.map(s => ({ ...s, source: 'glossaire' })),
        ...corpusSections.map(s => ({ ...s, source: 'corpus' }))
    ];

    // Scorer chaque section
    const scored = allSections.map(section => ({
        ...section,
        score: relevanceScore(section, concepts)
    }));

    // Trier par score décroissant
    scored.sort((a, b) => b.score - a.score);

    // Retourner les top K
    return scored.slice(0, topK).map(s => ({
        title: s.title,
        content: s.content.trim().substring(0, 800), // Limiter à 800 chars
        source: s.source,
        score: s.score
    }));
}

/**
 * Formatte les passages RAG pour inclusion dans le prompt
 */
function formatRAGContext(passages) {
    if (passages.length === 0) {
        return "Aucun passage spécifique trouvé. Réponds selon ta connaissance philosophique générale.";
    }

    let context = "Passages pertinents du corpus :\n\n";

    for (const [idx, passage] of passages.entries()) {
        context += `[${idx + 1}] ${passage.title}\n`;
        context += `${passage.content}\n\n`;
    }

    return context;
}

module.exports = {
    loadCorpus,
    ragLookup,
    formatRAGContext,
    splitIntoSections
};
