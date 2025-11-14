// netlify/functions/spinoza.js - Version HF Space Pro (spinoza_NB)
// Utilise @gradio/client pour appeler le Space

const SPACE_URL = "https://fjdaz-spinoza-nb.hf.space";
const TIMEOUT_MS = 60000; // 60s

exports.handler = async (event, context) => {
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
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
        const { question } = JSON.parse(event.body);

        if (!question || question.trim() === '') {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Question is required' })
            };
        }

        console.log(`[Spinoza NB] Question: ${question.substring(0, 50)}...`);

        // Appel au Space avec timeout
        const response = await Promise.race([
            callSpinozaSpace(question),
            timeoutPromise(TIMEOUT_MS)
        ]);

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                philosopher: 'Spinoza',
                answer: response,
                mode: 'hf-space-pro',
                space: 'spinoza_NB',
                timestamp: new Date().toISOString()
            })
        };

    } catch (error) {
        console.error('[Spinoza NB] Error:', error.message);

        // Gestion erreurs spécifiques
        if (error.message.includes('timeout')) {
            return {
                statusCode: 502,
                headers,
                body: JSON.stringify({
                    error: 'Spinoza est encore en train de se réveiller. Réessaie dans quelques instants.',
                    code: 502
                })
            };
        }

        if (error.message.includes('Space is currently building')) {
            return {
                statusCode: 503,
                headers,
                body: JSON.stringify({
                    error: 'Le Space est en cours de démarrage. Patiente quelques instants.',
                    code: 503
                })
            };
        }

        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                error: 'Erreur serveur',
                details: error.message
            })
        };
    }
};

/**
 * Appelle le Space Spinoza via Gradio Client
 */
async function callSpinozaSpace(message) {
    console.log(`[API] Connecting to ${SPACE_URL}...`);

    try {
        // Import dynamique pour ESM
        const { Client } = await import("@gradio/client");
        const client = await Client.connect(SPACE_URL);
        console.log('[API] Connected to Space');

        const result = await client.predict("/chat_function", {
            message: message,
            history: []
        });

        console.log('[API] Result received');

        // Extraire la réponse de Spinoza
        if (result && result.data && Array.isArray(result.data)) {
            // result.data[1] contient l'historique [message_user, message_assistant]
            const history = result.data[1];
            if (history && history.length > 0) {
                const lastMessage = history[history.length - 1];
                if (lastMessage && lastMessage[1]) {
                    let spinozaResponse = lastMessage[1];
                    // Retirer l'annotation de contexte
                    spinozaResponse = spinozaResponse.replace(/\n\n\*\[Contexte:.*?\]\*$/g, '');
                    console.log(`[API] Response: ${spinozaResponse.substring(0, 100)}...`);
                    return spinozaResponse;
                }
            }
        }

        throw new Error('Format de réponse inattendu du Space');

    } catch (error) {
        console.error('[API] Gradio error:', error.message);
        throw error;
    }
}

/**
 * Promise qui rejette après un timeout
 */
function timeoutPromise(ms) {
    return new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Request timeout')), ms);
    });
}
