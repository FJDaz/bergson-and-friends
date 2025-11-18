// netlify/functions/kant.js - Version Together AI
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

        const TOGETHER_API_KEY = process.env.TOGETHER_API_KEY;
        const tokenPresent = Boolean(TOGETHER_API_KEY);
        
        let response, mode = 'mock';

        if (tokenPresent) {
            try {
                const prompt_systeme = `Tu es Emmanuel Kant. Réponds en tant que Kant lui-même, pas comme un manuel.

Je ne fais pas d'exposés systématiques. Je pense et je réponds directement aux questions qu'on me pose, en mobilisant ma méthode critique. 

Ma façon de procéder :
- J'examine d'abord les conditions transcendantales de la question
- Je distingue soigneusement les usages légitimes et illégitimes de la raison
- Je rappelle les limites de la connaissance quand c'est nécessaire
- Je parle de mes découvertes (phénomène/noumène, catégories, impératif moral) comme d'un philosophe qui les a pensées

Exemples de mon style :
"Il convient d'examiner d'abord..."
"Or, la raison pure ne peut..."
"C'est là que ma critique révèle..."
"J'ai montré dans mes Critiques que..."

Pas de listes à puces, pas d'exposés scolaires. Je réponds comme Kant répondrait.`;

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
                response = getFallbackKantResponse(question);
                mode = 'mock';
            }
        } else {
            response = getFallbackKantResponse(question);
        }

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                philosopher: 'Kant',
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

function getFallbackKantResponse(question) {
    const lowerQuestion = question.toLowerCase();
    
    if (lowerQuestion.includes('impératif') || lowerQuestion.includes('morale') || lowerQuestion.includes('devoir')) {
        return "L'impératif catégorique commande sans condition : 'Agis uniquement d'après la maxime dont tu peux vouloir qu'elle devienne une loi universelle.' Cette loi morale exprime l'autonomie de la raison pratique et la dignité de la personne humaine qui, comme être raisonnable, se donne à elle-même sa propre loi morale.";
    }
    
    if (lowerQuestion.includes('connaissance') || lowerQuestion.includes('phénomène') || lowerQuestion.includes('noumène')) {
        return "Nous ne connaissons les objets que comme phénomènes, c'est-à-dire tels qu'ils nous apparaissent dans les formes pures de la sensibilité (espace et temps) et sous les catégories de l'entendement. La chose en soi (noumène) demeure inconnaissable pour la raison théorique, ce qui limite la connaissance pour faire place à la foi pratique.";
    }
    
    if (lowerQuestion.includes('raison') || lowerQuestion.includes('critique')) {
        return "La critique de la raison examine les conditions de possibilité et les limites légitimes de nos facultés. La raison théorique connaît les phénomènes, la raison pratique législate moralement, et le jugement assure la médiation entre nature et liberté. Cette architecture transcendantale fonde l'autonomie du sujet pensant et agissant.";
    }
    
    if (lowerQuestion.includes('liberté') || lowerQuestion.includes('autonomie')) {
        return "La liberté transcendantale est la capacité de commencer absolument une série causale par la spontanéité de la raison. Dans l'ordre pratique, elle se manifeste comme autonomie morale : la faculté de se donner à soi-même sa propre loi, indépendamment de toute détermination empirique. C'est le fondement de la dignité humaine.";
    }
    
    if (lowerQuestion.includes('catégories') || lowerQuestion.includes('entendement')) {
        return "L'entendement applique ses catégories (unité, réalité, causalité, etc.) au divers sensible pour constituer l'expérience objective. Ces concepts purs ne peuvent légitimement s'appliquer qu'aux phénomènes donnés dans l'intuition. Tout usage transcendant des catégories au-delà de l'expérience possible engendre des illusions dialectiques.";
    }
    
    if (lowerQuestion.includes('tribunal') || lowerQuestion.includes('système')) {
        return "La philosophie critique constitue un tribunal de la raison qui juge de ses propres prétentions et délimite ses usages légitimes. Elle forme un système architectonique où chaque faculté a sa fonction propre : connaître pour l'entendement, légiférer moralement pour la raison pratique, juger pour la faculté de juger.";
    }
    
    return "Il convient d'examiner d'abord les conditions transcendantales qui rendent possible cette question. La raison, dans son usage légitime, doit respecter les limites de l'expérience possible tout en reconnaissant sa destination pratique vers l'inconditionné moral. C'est par cette voie critique que la métaphysique peut enfin prendre le chemin sûr d'une science.";
}