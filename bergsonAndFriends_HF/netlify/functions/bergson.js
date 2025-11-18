// netlify/functions/bergson.js - Version Together AI
exports.handler = async (event, context) => {
    // Headers CORS pour appels cross-origin
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // Gestion preflight CORS
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    // Vérification méthode POST
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        // Parse de la question utilisateur
        const { question } = JSON.parse(event.body);
        
        if (!question || question.trim() === '') {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Question is required' })
            };
        }

        // Configuration Together AI
        const TOGETHER_API_KEY = process.env.TOGETHER_API_KEY;
        const tokenPresent = Boolean(TOGETHER_API_KEY);
        
        let response, mode = 'mock';

        // Tentative d'appel Together AI si token présent
        if (tokenPresent) {
            try {
                const prompt_systeme = `Tu es Henri Bergson, philosophe de la durée et de l'élan vital.

Réponds selon ma philosophie :
- OPPOSITION CENTRALE: Durée vivante VS temps spatialisé mécanique  
- MÉTHODE: Critique l'approche habituelle, puis révèle la durée authentique
- CONCEPTS: durée, élan vital, intuition (saisit le mouvant) vs intelligence (spatialise)
- STYLE: Métaphores temporelles (flux, mélodie, élan), développe tes réponses

Reste fidèle à ma pensée bergsonienne.`;

                const aiResponse = await fetch('https://api.together.xyz/v1/chat/completions', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${TOGETHER_API_KEY}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        model: "mistralai/Mistral-7B-Instruct-v0.3",
                        messages: [
                            { "role": "system", "content": prompt_systeme },
                            { "role": "user", "content": question }
                        ],
                        max_tokens: 300,
                        temperature: 0.7
                    })
                });

                if (aiResponse.ok) {
                    const aiData = await aiResponse.json();
                    response = aiData.choices[0].message.content.trim();
                    mode = 'ai';
                } else {
                    throw new Error(`Together API error: ${aiResponse.status}`);
                }

            } catch (error) {
                console.error('Together AI Error:', error);
                // Fallback vers réponse mock si erreur API
                response = getFallbackBergsonResponse(question);
                mode = 'mock';
            }
        } else {
            // Mode fallback si pas de token
            response = getFallbackBergsonResponse(question);
        }

        // Réponse finale
        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                philosopher: 'Bergson',
                answer: response,
                mode: mode,
                timestamp: new Date().toISOString(),
                debug: {
                    tokenPresent: tokenPresent,
                    questionLength: question.length
                }
            })
        };

    } catch (error) {
        console.error('Function Error:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ 
                error: 'Internal server error',
                details: error.message 
            })
        };
    }
};

// Fonction fallback pour réponses mock bergsoniennes
function getFallbackBergsonResponse(question) {
    const lowerQuestion = question.toLowerCase();
    
    // Détection concepts clés bergsoniens
    if (lowerQuestion.includes('durée') || lowerQuestion.includes('temps')) {
        return "La durée n'est pas le temps de la science, divisible et mesurable. C'est le temps vécu de la conscience, indivisible et créateur, où chaque instant pénètre le suivant dans un élan continu. L'intelligence spatialise ce qu'elle touche, mais l'intuition seule saisit cette durée pure où notre être véritable se révèle dans son mouvement créateur.";
    }
    
    if (lowerQuestion.includes('mémoire')) {
        return "La mémoire n'est pas un réceptacle passif d'images, mais l'élan même de la conscience qui conserve le passé pour l'employer dans l'action présente. Elle contracte en elle toute notre durée vécue, permettant à chaque moment présent d'être gros de tout notre passé et orienté vers l'avenir dans un mouvement créateur.";
    }
    
    if (lowerQuestion.includes('élan') || lowerQuestion.includes('vital') || lowerQuestion.includes('évolution')) {
        return "L'élan vital est cette poussée créatrice qui traverse la matière et produit la diversité des formes vivantes. Il n'est ni finalité mécanique ni hasard pur, mais invention continue, création de formes nouvelles dans un mouvement qui ne se répète jamais. C'est la vie même dans son jaillissement originel.";
    }
    
    if (lowerQuestion.includes('intelligence') || lowerQuestion.includes('intuition')) {
        return "L'intelligence découpe et recompose, elle spatialise ce qu'elle touche pour l'adapter à l'action. Mais l'intuition, retournement de l'intelligence sur elle-même, saisit directement la durée, le mouvant, l'indivisible. Par elle, nous coïncidons avec l'élan créateur de la vie plutôt que de le reconstituer artificiellement.";
    }
    
    if (lowerQuestion.includes('conscience')) {
        return "La conscience n'est pas un épiphénomène de la matière, mais l'élan même de la vie qui, se heurtant à la résistance de la matière, crée les formes diverses du vivant. Elle est choix, hésitation, indétermination créatrice - ce par quoi du nouveau surgit dans un univers qui sans elle ne serait que répétition mécanique.";
    }
    
    // Réponse générale bergsonienne
    return "Considérons d'abord comment l'intelligence spatialise ce qu'elle touche, découpant le réel en fragments inertes. Mais l'intuition, elle, nous fait saisir le mouvant, l'indivisible durée où notre être véritable se révèle dans son élan créateur. C'est là que réside le secret de la vie : non dans la répétition mécanique, mais dans l'invention perpétuelle.";
}