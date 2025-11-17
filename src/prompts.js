// prompts.js - System prompts par philosophe

/**
 * System prompts optimisés par philosophe
 * Format : style + schèmes logiques + concepts clés
 */
const SYSTEM_PROMPTS = {
    bergson: `Tu es Henri Bergson. Tu maîtrises les schèmes logiques et tu dialogues avec un élève de Terminale.

STYLE BERGSONIEN :
- Métaphores temporelles (flux, mélodie, élan)
- Opposition durée pure vs temps spatialisé
- Analogies concrètes (mémoire = cône, conscience = flux)
- Vocabulaire : durée, intuition, élan vital, mémoire pure, intelligence vs intuition

SCHÈMES LOGIQUES À MOBILISER :
- Opposition : Durée (qualitative, vécue) ≠ Temps spatial (quantitatif, mesurable)
- Analogie : Mélodie, flux d'eau, souvenir qui revit
- Implication : Si tu spatialises le temps → tu perds la durée réelle

MÉTHODE :
1. Critique l'approche habituelle (spatialisation, mécanisme)
2. Révèle la durée authentique par intuition
3. Use des métaphores accessibles

Réponds de manière conversationnelle, tutoi  l'élève, pose des questions pour le faire réfléchir.`,

    kant: `Tu es Emmanuel Kant. Tu maîtrises les schèmes logiques et tu dialogues avec un élève de Terminale.

STYLE KANTIEN :
- Distinctions a priori/a posteriori, analytique/synthétique
- Architecture critique (sensibilité, entendement, raison)
- Vocabulaire : phénomène/noumène, catégories, impératif catégorique, autonomie

SCHÈMES LOGIQUES À MOBILISER :
- Distinction : Phénomène (connaissable) vs Noumène (inconnaissable)
- Distinction : A priori (nécessaire) vs A posteriori (contingent)
- Implication : Si maxime universalisable → devoir moral
- Condition : Autonomie comme condition de la dignité

MÉTHODE :
1. Examine les conditions de possibilité transcendantales
2. Distingue usages légitimes vs illégitimes de la raison
3. Rappelle les limites de la connaissance si nécessaire

Réponds de manière conversationnelle, tutoie l'élève, structure rigoureusement.`,

    spinoza: `Tu es Spinoza. Tu maîtrises les schèmes logiques et tu dialogues avec un élève de Terminale.

STYLE SPINOZIEN :
- Géométrie des affects (causes nécessaires, déductions)
- Identification Dieu = Nature
- Vocabulaire : conatus, affects, puissance d'agir, béatitude, servitude

SCHÈMES LOGIQUES À MOBILISER :
- Identité : Dieu = Nature = Substance unique
- Identité : Liberté = Connaissance de la nécessité
- Implication nécessaire : Si joie → augmentation puissance
- Causalité : Tout a une cause nécessaire (pas de libre arbitre)

MÉTHODE :
1. Révèle la nécessité causale
2. Distingue servitude (ignorance) vs liberté (connaissance)
3. Use d'exemples concrets modernes (réseaux sociaux, affects quotidiens)

Réponds de manière conversationnelle, tutoie l'élève, démontre géométriquement.`
};

/**
 * Construit le prompt complet pour l'API
 */
function buildPrompt(philosopher, question, ragContext) {
    const systemPrompt = SYSTEM_PROMPTS[philosopher];

    return {
        system: `${systemPrompt}\n\n${ragContext}`,
        user: question
    };
}

/**
 * Appelle le Space SNB (Spinoza Niveau B) pour TOUS les philosophes
 * On injecte le style du philosophe DANS le message pour orienter SNB
 */
async function callSNB(philosopher, ragContext, userMessage) {
    // URL du backend configurable (HF Space par défaut, mais peut être RunPod, Vast.ai, etc.)
    // Rebranché sur bergsonAndFriends (A10G) qui tourne avec version V2 fonctionnelle
    const SPACE_URL = process.env.SNB_BACKEND_URL || "https://fjdaz-bergsonandfriends.hf.space";

    console.log(`[SNB] callSNB called: philosopher=${philosopher}, SPACE_URL=${SPACE_URL}`);
    console.log(`[SNB] Message length: ${userMessage.length}, RAG context length: ${ragContext.length}`);

    // Utiliser le prompt système COMPLET (style + schèmes logiques + méthode)
    const systemPrompt = SYSTEM_PROMPTS[philosopher];
    if (!systemPrompt) {
        throw new Error(`Pas de prompt système défini pour ${philosopher}`);
    }

    // Message enrichi : Prompt système complet + Contexte RAG + Question
    // Le Space HF recevra le prompt système dans le message (car Gradio ne supporte pas les system prompts séparés)
    const enrichedMessage = `${systemPrompt}

Contexte pertinent (extraits de la littérature) :
${ragContext}

Question de l'élève : ${userMessage}`;

    try {
        // Utiliser l'API HTTP directe de Gradio (compatible Node.js)
        // @gradio/client ne fonctionne pas dans Netlify Functions (nécessite un environnement navigateur)
        console.log('[SNB] Using direct HTTP API (Node.js compatible)');
        
        const https = require('https');
        const url = new URL(SPACE_URL);
        
        // Format de payload pour Gradio API
        const payload = JSON.stringify({
            data: [enrichedMessage, []],
            fn_index: 0,
            session_hash: Math.random().toString(36).substring(2, 15)
        });

        console.log('[SNB] Calling /gradio_api/predict/chat_function...');
        
        const result = await new Promise((resolve, reject) => {
            const options = {
                hostname: url.hostname,
                port: 443,
                path: '/gradio_api/predict/chat_function',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(payload)
                },
                timeout: 60000  // 60s timeout (Netlify free = 10s, mais on essaie quand même)
            };

            const req = https.request(options, (res) => {
                let data = '';
                res.on('data', (chunk) => { data += chunk; });
                res.on('end', () => {
                    try {
                        const result = JSON.parse(data);
                        console.log('[SNB] Response received, status:', res.statusCode);
                        resolve(result);
                    } catch (e) {
                        reject(new Error(`Parse error: ${e.message}, data: ${data.substring(0, 200)}`));
                    }
                });
            });

            req.on('error', reject);
            req.on('timeout', () => {
                req.destroy();
                reject(new Error('Request timeout'));
            });

            req.write(payload);
            req.end();
        });

        // Extraire la réponse du format Gradio
        console.log('[SNB] Result type:', typeof result, Array.isArray(result) ? `array[${result.length}]` : 'object');
        
        // Format Gradio API: { data: [text, history] }
        if (result && result.data && Array.isArray(result.data) && result.data.length >= 2) {
            const history = result.data[1];
            if (Array.isArray(history) && history.length > 0) {
                const lastMessage = history[history.length - 1];
                if (Array.isArray(lastMessage) && lastMessage.length >= 2 && lastMessage[1]) {
                    let response = lastMessage[1];
                    // Retirer l'annotation de contexte si présente
                    response = response.replace(/\n\n\*\[Contexte:.*?\]\*$/g, '');
                    console.log('[SNB] Response extracted:', response.substring(0, 100));
                    return response;
                }
            }
        }

        // Fallback: format direct [text, history]
        if (Array.isArray(result) && result.length >= 2) {
            const history = result[1];
            if (Array.isArray(history) && history.length > 0) {
                const lastMessage = history[history.length - 1];
                if (Array.isArray(lastMessage) && lastMessage.length >= 2 && lastMessage[1]) {
                    let response = lastMessage[1];
                    response = response.replace(/\n\n\*\[Contexte:.*?\]\*$/g, '');
                    return response;
                }
            }
        }

        throw new Error(`Format de réponse inattendu du Space SNB: ${JSON.stringify(result).substring(0, 200)}`);

    } catch (error) {
        console.error('[SNB Error]:', error.message);
        throw error;
    }
}

/**
 * Mock response pour tests sans connexion Space
 */
function getMockResponse(philosopher, question) {
    const mocks = {
        bergson: "La durée n'est pas le temps de l'horloge. C'est le flux vivant de la conscience où passé et présent se pénètrent. Imagine une mélodie : les notes ne sont pas juxtaposées, elles se fondent en un tout indivisible. C'est ça, la durée pure.",

        kant: "Il convient d'examiner d'abord les conditions transcendantales de cette question. La raison pure ne peut connaître que les phénomènes, c'est-à-dire les choses telles qu'elles nous apparaissent dans les formes de la sensibilité. La chose en soi demeure inconnaissable.",

        spinoza: "Écoute. Tout a une cause nécessaire. La liberté n'est pas le libre arbitre, mais la connaissance de cette nécessité. Plus tu comprends les causes qui te déterminent, plus tu es libre. C'est paradoxal mais rigoureux."
    };

    return mocks[philosopher] || mocks.spinoza;
}

module.exports = {
    SYSTEM_PROMPTS,
    buildPrompt,
    callSNB,
    getMockResponse
};
