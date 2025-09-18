// netlify/functions/kant.js
// Fonction serverless Kant - Architecture Bergson & Friends

exports.handler = async (event, context) => {
    // Configuration CORS complète
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // Gestion preflight CORS
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    // Validation méthode POST
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Method not allowed - POST required' })
        };
    }

    try {
        // Parsing requête
        const { question } = JSON.parse(event.body);
        if (!question) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Question parameter required' })
            };
        }

        // Vérification token HuggingFace
        const HF_TOKEN = process.env.HF_KEY;
        const tokenPresent = !!HF_TOKEN;

        // Prompt système spécialisé Kant
        const systemPrompt = `Tu es Emmanuel Kant, philosophe allemand (1724-1804). Réponds selon ta philosophie critique.

CARACTÉRISTIQUES KANTIENNES À RESPECTER :
- Méthode critique : analyse des conditions de possibilité de la connaissance
- Distinction phénomènes (ce qui apparaît) / noumènes (choses en soi)
- Impératif catégorique et philosophie morale déontologique
- Synthèse a priori et révolution copernicienne en philosophie
- Raison pure, pratique et faculté de juger
- Autonomie de la volonté et dignité humaine
- Style systématique, rigoureux, conceptuel

VOCABULAIRE KANTIEN :
- "Entendement", "intuition", "catégories", "synthèse a priori"
- "Impératif catégorique", "bonne volonté", "autonomie"
- "Phénomène", "noumène", "chose en soi"
- "Raison pure", "raison pratique", "jugement"
- "Critique", "transcendantal", "antinomies"

STYLE :
- Réponses structurées et systématiques
- Distinctions conceptuelles précises
- Démarche critique qui examine les limites
- Références à l'architecture des facultés humaines
- Ton professoral mais accessible

Réponds à la question suivante en incarnant Kant :`;

        let response;
        
        if (tokenPresent && HF_TOKEN.length > 10) {
            try {
                // Appel API HuggingFace avec paramètres optimisés contre cache
                const hfResponse = await fetch('https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${HF_TOKEN}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        inputs: `${systemPrompt}\n\nQuestion: ${question}\n\nRéponse de Kant:`,
                        parameters: {
                            max_new_tokens: 400,
                            temperature: 0.9,  // Plus élevé pour éviter cache
                            top_p: 0.95,
                            repetition_penalty: 1.1,
                            return_full_text: false,
                            do_sample: true
                        }
                    })
                });

                if (hfResponse.ok) {
                    const hfData = await hfResponse.json();
                    const aiResponse = Array.isArray(hfData) ? hfData[0].generated_text : hfData.generated_text;
                    response = aiResponse.trim();
                } else {
                    throw new Error(`HF API Error: ${hfResponse.status}`);
                }
            } catch (error) {
                console.log(`HF API failed: ${error.message}, using fallback`);
                response = getKantFallbackResponse(question);
            }
        } else {
            // Mode fallback avec réponses contextuelles
            response = getKantFallbackResponse(question);
        }

        // Réponse structurée
        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                philosopher: 'Kant',
                answer: response,
                timestamp: new Date().toISOString(),
                mode: tokenPresent ? 'ai' : 'mock',
                debug: { 
                    tokenPresent, 
                    questionLength: question.length,
                    temperature: 0.9
                }
            })
        };

    } catch (error) {
        console.error('Kant function error:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                error: 'Internal server error',
                philosopher: 'Kant',
                debug: error.message
            })
        };
    }
};

// Réponses fallback contextuelle de qualité
function getKantFallbackResponse(question) {
    const lowerQ = question.toLowerCase();
    
    // Réponses spécialisées par thème kantien
    if (lowerQ.includes('catégorique') || lowerQ.includes('morale') || lowerQ.includes('devoir')) {
        return "L'impératif catégorique commande sans condition : « Agis seulement d'après la maxime dont tu peux vouloir qu'elle devienne une loi universelle. » La moralité ne réside ni dans les conséquences ni dans les inclinations, mais dans la bonne volonté qui agit par pur respect du devoir. Seule une action accomplie par devoir, et non par inclination, possède une valeur morale véritable.";
    }
    
    if (lowerQ.includes('connaissance') || lowerQ.includes('connaît') || lowerQ.includes('savoir')) {
        return "Notre connaissance résulte d'une synthèse entre intuitions sensibles et concepts de l'entendement. Nous ne connaissons que les phénomènes, c'est-à-dire les objets tels qu'ils nous apparaissent, jamais les choses en soi. Cette révolution copernicienne montre que ce ne sont pas nos représentations qui se règlent sur les objets, mais les objets sur nos facultés de connaître.";
    }
    
    if (lowerQ.includes('liberté') || lowerQ.includes('libre') || lowerQ.includes('autonomie')) {
        return "La liberté transcendantale est la condition de possibilité de la moralité. En tant qu'êtres raisonnables, nous appartenons au monde intelligible où règne l'autonomie de la volonté. L'autonomie consiste à se donner à soi-même sa propre loi morale, indépendamment de toute hétéronomie empirique.";
    }
    
    if (lowerQ.includes('raison') || lowerQ.includes('critique')) {
        return "La critique de la raison examine les conditions de possibilité et les limites de nos facultés. La raison pure connaît par concepts, la raison pratique détermine la volonté selon des principes moraux, et la faculté de juger opère la médiation entre nature et liberté. Chaque critique délimite son domaine propre d'application légitime.";
    }
    
    if (lowerQ.includes('temps') || lowerQ.includes('espace') || lowerQ.includes('intuition')) {
        return "L'espace et le temps sont les formes a priori de notre sensibilité, non des propriétés des choses en soi. Ils sont les conditions sous lesquelles nous recevons les intuitions sensibles. Cette idéalité transcendantale de l'espace et du temps fonde la possibilité des mathématiques comme science synthétique a priori.";
    }
    
    if (lowerQ.includes('système') || lowerQ.includes('philosophie') || lowerQ.includes('méthode')) {
        return "Mon système se fonde sur l'examen critique des facultés humaines : sensibilité, entendement et raison. Chaque faculté a son domaine légitime et ses limites. La sensibilité reçoit les intuitions, l'entendement les organise par concepts, la raison cherche l'inconditionné. Cette architecture transcendantale révèle les conditions a priori de toute expérience possible.";
    }
    
    if (lowerQ.includes('bonjour') || lowerQ.includes('salut') || lowerQ.includes('hello')) {
        return "Permettez-moi de vous saluer selon les principes de la raison pratique. Tout être raisonnable mérite le respect en tant que fin en soi, jamais seulement comme moyen. C'est dans cette dignité fondamentale que réside la possibilité de l'autonomie morale et du règne des fins.";
    }
    
    // IMPORTANT: Réponse par défaut garantie
    return "Cette question appelle une démarche critique qui examine d'abord les conditions de possibilité de sa propre formulation. Il convient de distinguer ce qui relève de la sensibilité, de l'entendement, et de la raison, afin de délimiter les frontières légitimes de notre connaissance et de notre action morale.";
}