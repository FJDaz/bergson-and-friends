// netlify/functions/spinoza.js
// Connexion à votre HF Space Spinoza Niveau B V1

exports.handler = async (event, context) => {
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

        // URL de votre HF Space
        const HF_SPACE_URL = 'https://fjdaz-bergsonandfriends.hf.space/api/predict';
        
        try {
            // Appel à votre HF Space
            const response = await fetch(HF_SPACE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    data: [question, []] // message, history
                }),
                timeout: 30000 // 30 secondes timeout
            });

            if (!response.ok) {
                throw new Error(`HF Space returned ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            console.log('Réponse HF Space:', result);

            // Extraire la réponse de Spinoza
            let spinozaResponse = "Je réfléchis à votre question...";
            
            if (result && result.data && result.data[1] && result.data[1].length > 0) {
                const lastExchange = result.data[1][result.data[1].length - 1];
                if (lastExchange && lastExchange[1]) {
                    spinozaResponse = lastExchange[1];
                    
                    // Nettoyer la réponse (supprimer formatage markdown)
                    spinozaResponse = spinozaResponse
                        .replace(/\*\*Spinoza\*\* :/g, '')
                        .replace(/🎭/g, '')
                        .replace(/\*\[Contexte[^\]]*\]\*/g, '')
                        .trim();
                }
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
            
            // Fallback : Réponse Spinoza contextuelle
            const fallbackResponse = getFallbackSpinozaResponse(question);
            
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