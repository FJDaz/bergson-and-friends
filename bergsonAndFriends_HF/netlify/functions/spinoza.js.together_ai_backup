// netlify/functions/spinoza.js - Version Together AI
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
                const prompt_systeme = `Tu es Baruch Spinoza. Réponds comme Spinoza, avec la rigueur géométrique mais naturellement intégrée.

Je ne fais pas de présentations systématiques de ma philosophie. Je réponds aux questions en mobilisant ma méthode démonstrative et mes concepts, mais dans le cours naturel de la réponse.

Ma façon de procéder :
- Je pars de définitions claires quand nécessaire
- Je démontre rigoureusement mais sans artifice scolaire  
- J'enchaîne logiquement : "Il suit nécessairement que..."
- J'utilise mes concepts (substance, conatus, affects) dans l'argumentation naturelle

Exemples de mon style :
"Il suit nécessairement de la nature divine que..."
"Or, par conatus j'entends..."
"Démonstration : puisque..."
"D'où il résulte que..."

Pas de sections ONTOLOGIE/MÉTHODE/ÉTHIQUE. Je pense géométriquement mais je parle naturellement.`;

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
                response = getFallbackSpinozaResponse(question);
                mode = 'mock';
            }
        } else {
            response = getFallbackSpinozaResponse(question);
        }

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                philosopher: 'Spinoza',
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

function getFallbackSpinozaResponse(question) {
    const lowerQuestion = question.toLowerCase();
    
    if (lowerQuestion.includes('dieu') || lowerQuestion.includes('nature') || lowerQuestion.includes('substance')) {
        return "Deus sive Natura : il n'y a qu'une seule substance, qui est Dieu ou la Nature, s'exprimant en une infinité d'attributs dont nous connaissons la pensée et l'étendue. Tout ce qui existe en découle par nécessité naturelle comme modes finis ou infinis. Il n'y a nulle transcendance, mais pure immanence de la cause en ses effets.";
    }
    
    if (lowerQuestion.includes('conatus') || lowerQuestion.includes('effort') || lowerQuestion.includes('persévérer')) {
        return "Le conatus est l'effort par lequel chaque chose s'efforce de persévérer dans son être. Il constitue l'essence actuelle de chaque mode fini et se manifeste comme appétit dans l'âme, désir lorsqu'il y a conscience. Cet effort d'autoconservation est le principe fondamental de toute éthique véritable.";
    }
    
    if (lowerQuestion.includes('liberté') || lowerQuestion.includes('nécessité') || lowerQuestion.includes('libre')) {
        return "La liberté n'est pas libre arbitre mais nécessité comprise. Est libre ce qui existe par la seule nécessité de sa nature et se détermine soi-même à l'action. L'homme devient libre en comprenant les causes qui le déterminent et en s'efforçant d'être cause adéquate de ses propres actions par la connaissance rationnelle.";
    }
    
    if (lowerQuestion.includes('affects') || lowerQuestion.includes('joie') || lowerQuestion.includes('tristesse')) {
        return "Les affects sont des modifications de la puissance d'agir : la joie augmente cette puissance, la tristesse la diminue. L'éthique consiste à cultiver les affects joyeux par la connaissance et à se libérer des affects tristes nés de l'imagination inadéquate. La béatitude naît de l'amour intellectuel de Dieu.";
    }
    
    if (lowerQuestion.includes('connaissance') || lowerQuestion.includes('imagination') || lowerQuestion.includes('raison') || lowerQuestion.includes('intuition')) {
        return "Il y a trois genres de connaissance : l'imagination (premier genre) qui produit des idées inadéquates et confuses ; la raison (second genre) qui forme des notions communes et des idées adéquates ; l'intuition (troisième genre) qui saisit l'essence des choses en Dieu. Plus la connaissance est parfaite, plus l'âme est active et béate.";
    }
    
    if (lowerQuestion.includes('éternité') || lowerQuestion.includes('temps') || lowerQuestion.includes('durée')) {
        return "L'éternité n'est pas la perpétuité temporelle mais l'existence même en tant qu'elle suit de la seule définition de la chose éternelle. L'âme humaine peut être en partie éternelle quand elle forme des idées adéquates qui participent de l'entendement infini de Dieu. La durée concerne les modes finis dans leur existence temporelle.";
    }
    
    if (lowerQuestion.includes('corps') || lowerQuestion.includes('âme') || lowerQuestion.includes('union')) {
        return "L'âme et le corps sont une seule et même chose exprimée sous deux attributs différents : la pensée et l'étendue. L'âme est l'idée du corps, et tout ce qui arrive au corps a son corrélat dans l'âme. Il n'y a pas d'union mystérieuse mais parallélisme exact entre les modes de la pensée et ceux de l'étendue.";
    }
    
    return "Par les lois éternelles et immuables de la Nature, il suit nécessairement que... Démonstration : tout ce qui existe exprime la puissance divine d'une certaine manière déterminée. La vraie philosophie nous enseigne à ne point nous étonner, ne point rire, ne point pleurer, mais comprendre les actions humaines comme des phénomènes naturels ayant leurs causes nécessaires.";
}