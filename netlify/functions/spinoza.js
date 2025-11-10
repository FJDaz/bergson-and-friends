// netlify/functions/spinoza.js
// Connexion à votre HF Space Spinoza Niveau B V1

let gradioAppPromise = null;

async function getGradioApp() {
    if (!gradioAppPromise) {
        gradioAppPromise = import("@gradio/client")
            .then(({ client }) =>
                client("FJDaz/bergsonAndFriends", {
                    hf_token: process.env.HF_TOKEN || undefined
                })
            )
            .catch((error) => {
                gradioAppPromise = null;
                throw error;
            });
    }
    return gradioAppPromise;
}

exports.handler = async (event) => {
    // Headers CORS
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // Gérer preflight CORS
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    // Seules les requêtes POST
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        // Récupérer la question du frontend
        const { question } = JSON.parse(event.body);
        
        if (!question || question.trim() === '') {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Question is required' })
            };
        }

        console.log('Question reçue:', question);

        try {
            // Appel à votre HF Space
        const app = await getGradioApp();
        const result = await app.predict("/chat_function", {
            message: question.trim(),
            history: []
        });

        const outputArray = Array.isArray(result)
            ? result
            : Array.isArray(result?.data)
                ? result.data
                : [];

        let textReply = outputArray[0];
        if (textReply && typeof textReply === 'object') {
            textReply = textReply.text ?? textReply.message ?? JSON.stringify(textReply);
        }
        if (typeof textReply !== 'string') {
            textReply = String(textReply ?? '');
        }

        let spinozaResponse = textReply.trim();
        if (!spinozaResponse) {
            spinozaResponse = "Je réfléchis à ta question...";
        }

            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({
                    philosopher: 'Spinoza',
                    answer: spinozaResponse,
                    timestamp: new Date().toISOString(),
                    source: 'huggingface_space'
                })
            };

        } catch (hfError) {
            console.error('Erreur HF Space:', hfError);
            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({
                    philosopher: 'Spinoza',
                    answer: "Je suis encore en train de me réveiller depuis Hugging Face. Patiente quelques instants et relance ta question.",
                    timestamp: new Date().toISOString(),
                    source: 'warmup',
                    note: 'Space HF en cours de démarrage — réessaie bientôt.'
                })
            };
        }

    } catch (error) {
        console.error('Erreur générale:', error);
        
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                error: 'Erreur interne du serveur',
                message: error.message
            })
        };
    }
};