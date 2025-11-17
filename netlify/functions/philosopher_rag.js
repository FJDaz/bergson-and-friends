// netlify/functions/philosopher_rag.js
// Fonction Netlify pour tester le système RAG complet avec SNB

const { detectPhilosopher, extractConcepts } = require('../../src/detection');
const { ragLookup, formatRAGContext } = require('../../src/rag_system');
const { callSNB, getMockResponse } = require('../../src/prompts');

/**
 * Questions bac par philosophe (pour initialisation)
 */
const QUESTIONS_BAC = {
    bergson: [
        "Le temps passe-t-il vraiment ?",
        "Se souvenir, est-ce revivre ?",
        "L'art requiert-il de l'inspiration ?",
        "Peut-on se connaître soi-même ?",
        "La conscience fait-elle notre identité ?"
    ],
    kant: [
        "Agir moralement, est-ce agir par devoir ?",
        "Être libre, est-ce faire ce qui nous plaît ?",
        "Que puis-je savoir du monde ?",
        "La morale est-elle universelle ?",
        "Qu'est-ce qu'une société juste ?"
    ],
    spinoza: [
        "La liberté est-elle une illusion ?",
        "Suis-je esclave de mes désirs ?",
        "Peut-on désirer sans souffrir ?",
        "La joie procure-t-elle un pouvoir ?",
        "La raison peut-elle tout expliquer ?"
    ]
};

exports.handler = async (event, context) => {
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const body = JSON.parse(event.body);
        const { action, philosopher, message, history } = body;

        // ACTION 1 : Initialisation - Le philosophe pose une question
        if (action === 'init') {
            const phil = philosopher || 'spinoza';
            const questions = QUESTIONS_BAC[phil];
            const randomQuestion = questions[Math.floor(Math.random() * questions.length)];

            const greeting = {
                bergson: `Bonjour ! Je suis Henri Bergson. Discutons ensemble de cette question :\n\n**${randomQuestion}**\n\nQu'en penses-tu ?`,
                kant: `Bonjour ! Je suis Emmanuel Kant. Examinons ensemble cette question :\n\n**${randomQuestion}**\n\nQuelle est ta réflexion ?`,
                spinoza: `Bonjour ! Je suis Spinoza. Discutons ensemble de cette question :\n\n**${randomQuestion}**\n\nQu'en penses-tu ?`
            };

            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({
                    philosopher: phil,
                    question: randomQuestion,
                    greeting: greeting[phil],
                    history: [[null, greeting[phil]]]
                })
            };
        }

        // ACTION 2 : Réponse - L'élève a répondu, le philosophe adapte
        if (action === 'respond') {
            if (!message || !philosopher) {
                return {
                    statusCode: 400,
                    headers,
                    body: JSON.stringify({ error: 'message and philosopher required' })
                };
            }

            console.log(`[RAG] Question élève pour ${philosopher}: ${message.substring(0, 50)}...`);

            // Extraction concepts pour RAG
            const concepts = extractConcepts(message);
            console.log(`[RAG] Concepts extraits: ${concepts.join(', ')}`);

            // RAG Lookup
            const passages = ragLookup(philosopher, concepts, 3);
            const ragContext = formatRAGContext(passages);

            console.log(`[RAG] ${passages.length} passages trouvés`);

            // Appel SNB (ou mock si USE_MOCK=true)
            // SNB réactivé : Space HF configuré avec show_api=True
            const useMock = process.env.USE_MOCK === 'true';
            let answer;

            if (useMock) {
                answer = getMockResponse(philosopher, message);
                console.log('[RAG] Mode MOCK (USE_MOCK=true)');
            } else {
                try {
                    console.log('[RAG] Appel SNB Space (peut prendre 30-60s si cold start)...');
                    console.log('[RAG] Philosopher:', philosopher);
                    console.log('[RAG] Message preview:', message.substring(0, 50));
                    answer = await callSNB(philosopher, ragContext, message);
                    console.log('[RAG] Mode SNB Space OK - Réponse reçue:', answer.substring(0, 100));
                } catch (error) {
                    console.error('[RAG] Erreur SNB, fallback mock:', error.message);
                    console.error('[RAG] Stack trace:', error.stack);
                    answer = getMockResponse(philosopher, message);
                }
            }

            // Mise à jour historique
            const updatedHistory = history || [];
            updatedHistory.push([message, answer]);

            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({
                    philosopher,
                    answer,
                    history: updatedHistory,
                    concepts,
                    passages: passages.map(p => ({ title: p.title, score: p.score }))
                })
            };
        }

        return {
            statusCode: 400,
            headers,
            body: JSON.stringify({ error: 'Invalid action. Use "init" or "respond"' })
        };

    } catch (error) {
        console.error('[RAG Error]:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                error: 'Internal error',
                details: error.message
            })
        };
    }
};
