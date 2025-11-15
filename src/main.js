// main.js - Orchestration complète du système RAG
const { detectPhilosopher, extractConcepts } = require('./detection');
const { ragLookup, formatRAGContext } = require('./rag_system');
const { buildPrompt, callSNB, getMockResponse } = require('./prompts');

/**
 * Pipeline complet : Question → Philosophe → RAG → Prompt → Réponse
 */
async function processQuestion(question, options = {}) {
    const useMock = options.mock !== false; // Mock par défaut

    console.log(`\n${'='.repeat(60)}`);
    console.log(`QUESTION : "${question}"`);
    console.log('='.repeat(60));

    // Étape 1 : Détection du philosophe
    console.log('\n[1/4] Détection du philosophe...');
    const detection = detectPhilosopher(question);

    console.log(`   → Philosophe : ${detection.philosopher.toUpperCase()}`);
    console.log(`   → Confidence : ${(detection.confidence * 100).toFixed(1)}%`);
    console.log(`   → Mots-clés : ${detection.keywords.join(', ') || 'aucun'}`);
    console.log(`   → Raison : ${detection.reason}`);

    // Étape 2 : Extraction concepts pour RAG
    console.log('\n[2/4] Extraction des concepts...');
    const concepts = extractConcepts(question);
    console.log(`   → Concepts : ${concepts.join(', ') || 'aucun'}`);

    // Étape 3 : RAG Lookup
    console.log('\n[3/4] RAG Lookup dans le corpus...');
    const passages = ragLookup(detection.philosopher, concepts, 3);
    console.log(`   → ${passages.length} passages trouvés`);

    for (const [idx, p] of passages.entries()) {
        console.log(`   [${idx + 1}] ${p.title} (score: ${p.score}, source: ${p.source})`);
    }

    const ragContext = formatRAGContext(passages);

    // Étape 4 : Génération avec SNB
    console.log('\n[4/4] Génération de la réponse...');

    let answer;
    if (useMock) {
        answer = getMockResponse(detection.philosopher, question);
        console.log('   → Mode : MOCK (pas d\'appel Space SNB)');
    } else {
        // Appel au Space SNB (MÊME MODÈLE pour les 3 philosophes)
        console.log('   → Mode : SNB Space (Spinoza Niveau B)');
        console.log(`   → Philosophe : ${detection.philosopher.toUpperCase()}`);

        try {
            answer = await callSNB(detection.philosopher, ragContext, question);
        } catch (error) {
            console.error(`   ⚠️  Erreur SNB, fallback mock : ${error.message}`);
            answer = getMockResponse(detection.philosopher, question);
        }
    }

    // Résultat final
    console.log(`\n${'='.repeat(60)}`);
    console.log(`RÉPONSE (${detection.philosopher.toUpperCase()}) :`);
    console.log('='.repeat(60));
    console.log(answer);
    console.log('='.repeat(60));

    return {
        question,
        philosopher: detection.philosopher,
        confidence: detection.confidence,
        keywords: detection.keywords,
        concepts,
        passages,
        answer,
        ragContext
    };
}

/**
 * Interface CLI interactive
 */
async function interactiveCLI() {
    const readline = require('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    console.log('\n🎓 BERGSON & FRIENDS - Test RAG Local\n');
    console.log('Pose une question philosophique (ou "exit" pour quitter)\n');

    const askQuestion = () => {
        rl.question('Question > ', async (input) => {
            const question = input.trim();

            if (question.toLowerCase() === 'exit') {
                console.log('\n👋 À bientôt !\n');
                rl.close();
                return;
            }

            if (!question) {
                askQuestion();
                return;
            }

            try {
                await processQuestion(question, { mock: true });
            } catch (error) {
                console.error('Erreur:', error.message);
            }

            console.log('\n');
            askQuestion();
        });
    };

    askQuestion();
}

module.exports = {
    processQuestion,
    interactiveCLI
};

// Exécution CLI si lancé directement
if (require.main === module) {
    interactiveCLI();
}
