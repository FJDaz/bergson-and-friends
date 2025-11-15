// detection.js - Détection du philosophe selon mots-clés

/**
 * Mots-clés par philosophe (validés selon annales bac + concepts)
 */
const PHILOSOPHER_KEYWORDS = {
    bergson: {
        primary: [
            'durée', 'temps', 'mémoire', 'intuition', 'élan vital',
            'conscience', 'perception', 'souvenir', 'instant',
            'mouvement', 'création', 'créateur', 'vie', 'vivant',
            'art', 'inspiration', 'connaître soi'
        ],
        secondary: [
            'spatial', 'qualitatif', 'flux', 'mélodie', 'image',
            'matière', 'esprit', 'instantané', 'évolution',
            'esthétique', 'artiste', 'œuvre', 'identité', 'moi'
        ]
    },

    kant: {
        primary: [
            'devoir', 'impératif', 'catégorique', 'morale', 'raison',
            'phénomène', 'noumène', 'a priori', 'synthétique', 'analytique',
            'liberté', 'autonomie', 'loi', 'universelle', 'catégories'
        ],
        secondary: [
            'sensibilité', 'entendement', 'jugement', 'critique',
            'transcendantal', 'maxime', 'espace', 'causalité',
            'chose en soi', 'dignité', 'personne'
        ]
    },

    spinoza: {
        primary: [
            'substance', 'dieu', 'nature', 'mode', 'attribut',
            'affect', 'conatus', 'joie', 'tristesse', 'désir',
            'liberté', 'nécessité', 'puissance', 'béatitude', 'servitude'
        ],
        secondary: [
            'éthique', 'géométrique', 'déterminisme', 'cause',
            'passion', 'vertu', 'corps', 'âme', 'intellect',
            'amour intellectuel', 'haine', 'crainte'
        ]
    }
};

/**
 * Mapping thèmes bac → philosophe recommandé
 */
const THEMES_TO_PHILOSOPHER = {
    // Temps/Durée/Conscience → Bergson
    'temps': 'bergson',
    'passe': 'bergson',
    'mémoire': 'bergson',
    'souvenir': 'bergson',
    'instant': 'bergson',
    'conscience': 'bergson',
    'perception': 'bergson',
    'art': 'bergson',
    'inspiration': 'bergson',
    'création': 'bergson',
    'connaître soi': 'bergson',
    'identité': 'bergson',

    // Devoir/Morale → Kant
    'devoir': 'kant',
    'morale': 'kant',
    'agir moralement': 'kant',
    'bien et mal': 'kant',
    'juste': 'kant',

    // Liberté/Déterminisme → Spinoza (prioritaire)
    'liberté': 'spinoza',
    'libre': 'spinoza',
    'esclave': 'spinoza',
    'désir': 'spinoza',
    'bonheur': 'spinoza',
    'joie': 'spinoza'
};

/**
 * Détecte le philosophe le plus pertinent pour une question
 * @param {string} question - Question de l'élève
 * @returns {{philosopher: string, confidence: number, keywords: string[]}}
 */
function detectPhilosopher(question) {
    const lowerQuestion = question.toLowerCase();
    const scores = {
        bergson: { score: 0, keywords: [] },
        kant: { score: 0, keywords: [] },
        spinoza: { score: 0, keywords: [] }
    };

    // 1. Scoring par mots-clés
    for (const [phil, kw] of Object.entries(PHILOSOPHER_KEYWORDS)) {
        // Mots-clés primaires (poids 3)
        for (const keyword of kw.primary) {
            if (lowerQuestion.includes(keyword.toLowerCase())) {
                scores[phil].score += 3;
                scores[phil].keywords.push(keyword);
            }
        }

        // Mots-clés secondaires (poids 1)
        for (const keyword of kw.secondary) {
            if (lowerQuestion.includes(keyword.toLowerCase())) {
                scores[phil].score += 1;
                scores[phil].keywords.push(keyword);
            }
        }
    }

    // 2. Scoring par thèmes bac
    for (const [theme, phil] of Object.entries(THEMES_TO_PHILOSOPHER)) {
        if (lowerQuestion.includes(theme)) {
            scores[phil].score += 2;
        }
    }

    // 3. Trouver le meilleur match
    const philosophers = Object.keys(scores);
    let best = philosophers[0];
    let maxScore = scores[best].score;

    for (const phil of philosophers) {
        if (scores[phil].score > maxScore) {
            best = phil;
            maxScore = scores[phil].score;
        }
    }

    // 4. Si aucun match, fallback sur Spinoza (philosophe "généraliste")
    if (maxScore === 0) {
        return {
            philosopher: 'spinoza',
            confidence: 0.3,
            keywords: [],
            reason: 'fallback (aucun mot-clé détecté)'
        };
    }

    // 5. Calculer confidence (0-1)
    const totalScores = Object.values(scores).reduce((sum, s) => sum + s.score, 0);
    const confidence = maxScore / totalScores;

    return {
        philosopher: best,
        confidence: Math.min(confidence, 1),
        keywords: scores[best].keywords,
        reason: `${scores[best].keywords.length} mots-clés trouvés`
    };
}

/**
 * Extrait les concepts clés de la question pour le RAG lookup
 */
function extractConcepts(question) {
    const lowerQuestion = question.toLowerCase();
    const concepts = [];

    // Extraire tous les mots-clés philosophiques
    for (const kw of Object.values(PHILOSOPHER_KEYWORDS)) {
        for (const keyword of [...kw.primary, ...kw.secondary]) {
            if (lowerQuestion.includes(keyword.toLowerCase())) {
                concepts.push(keyword);
            }
        }
    }

    return [...new Set(concepts)]; // Dédoublonner
}

module.exports = {
    detectPhilosopher,
    extractConcepts,
    PHILOSOPHER_KEYWORDS,
    THEMES_TO_PHILOSOPHER
};
