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
    const SPACE_URL = process.env.SNB_BACKEND_URL || "fjdaz-bergsonandfriends.hf.space";
    const API_PREFIX = process.env.SNB_API_PREFIX || "/gradio_api";

    // Styles courts pour injecter dans le message (TU ES le philosophe)
    const STYLE_INJECTION = {
        bergson: "Tu es Henri Bergson. Utilise des métaphores temporelles, distingue durée vécue vs temps spatialisé.",
        kant: "Tu es Emmanuel Kant. Utilise les distinctions a priori/a posteriori, phénomène vs noumène.",
        spinoza: "Tu es Spinoza. Utilise la géométrie des affects, montre les causes nécessaires."
    };

    // Message enrichi : Style + Contexte RAG + Question (comme la version qui fonctionnait)
    const enrichedMessage = `${STYLE_INJECTION[philosopher]}

Contexte pertinent :
${ragContext}

Question de l'élève : ${userMessage}`;

    try {
        // Import https pour Node.js
        const https = require('https');

        // Fallback synchrone si l'API SSE échoue ou n'est pas disponible
        async function predictSync(apiName, payloadObj) {
            const payload = JSON.stringify(payloadObj);
            return new Promise((resolve, reject) => {
                // Gradio expose les endpoints avec api_name comme //endpoint (double slash)
                const path = `${API_PREFIX}/predict//${apiName.replace(/^\//, '')}`;
                const options = {
                    hostname: SPACE_URL,
                    port: 443,
                    path,
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Content-Length': Buffer.byteLength(payload)
                    },
                    timeout: 60000
                };
                console.log(`[SNB] POST (predict) https://${SPACE_URL}${path}`);
                const req = https.request(options, (res) => {
                    let data = '';
                    res.on('data', (chunk) => { data += chunk; });
                    res.on('end', () => {
                        try {
                            const result = JSON.parse(data);
                            const output = result?.data;
                            // Forme attendue: [text, history]
                            if (output && output.length > 1 && Array.isArray(output[1])) {
                                const lastMessage = output[1][output[1].length - 1];
                                if (lastMessage && lastMessage[1]) {
                                    let response = lastMessage[1];
                                    response = response.replace(/\n\n\*\[Contexte:.*?\]\*$/g, '');
                                    resolve(response);
                                    return;
                                }
                            }
                            // Fallback: premier champ en texte
                            if (output && typeof output[0] === 'string') {
                                resolve(output[0]);
                                return;
                            }
                            reject(new Error('Unexpected predict output format'));
                        } catch (e) {
                            reject(new Error(`Predict parse error: ${e.message}`));
                        }
                    });
                });
                req.on('error', reject);
                req.on('timeout', () => {
                    req.destroy();
                    reject(new Error('Predict request timeout'));
                });
                req.write(payload);
                req.end();
            });
        }

        // Utiliser /call/ avec SSE (format standard pour endpoints nommés)
        console.log('[SNB] Calling Space bergsonAndFriends via /call/chat_function (SSE)');
        try {
            // Fallback vers SSE si predict échoue
            const payload = JSON.stringify({
                data: [enrichedMessage, []],
                session_hash: Math.random().toString(36).substring(2, 15)
            });

            const eventId = await new Promise((resolve, reject) => {
                // Gradio expose les endpoints nommés avec // (double slash)
                const callPath = `${API_PREFIX}/call//chat_function`;
                const options = {
                    hostname: SPACE_URL,
                    port: 443,
                    path: callPath,
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Content-Length': Buffer.byteLength(payload)
                    },
                    timeout: 8000  // 8s max (Netlify timeout 10s)
                };
                console.log(`[SNB] POST https://${SPACE_URL}${callPath}`);

                const req = https.request(options, (res) => {
                    let data = '';
                    res.on('data', (chunk) => { data += chunk; });
                    res.on('end', async () => {
                        try {
                            const result = JSON.parse(data);
                            if (result.event_id) {
                                resolve(result.event_id);
                            } else {
                                reject(new Error('No event_id returned'));
                            }
                        } catch (e) {
                            reject(new Error(`Parse error: ${e.message}`));
                        }
                    });
                });

                req.on('error', reject);
                req.on('timeout', () => {
                    req.destroy();
                    reject(new Error('Request timeout (Netlify 10s limit)'));
                });

                req.write(payload);
                req.end();
            });

            // Étape 2: Écouter les résultats SSE
        return await new Promise((resolve, reject) => {
            const ssePath = `${API_PREFIX}/call//chat_function/${eventId}`;
            const options = {
                hostname: SPACE_URL,
                port: 443,
                path: ssePath,
                method: 'GET',
                timeout: 120000  // 120s (2min) pour Space Pro
            };
            console.log(`[SNB] GET https://${SPACE_URL}${ssePath}`);

            const req = https.request(options, (res) => {
                let buffer = '';

                res.on('data', (chunk) => {
                    buffer += chunk.toString();
                    const lines = buffer.split('\n');
                    buffer = lines.pop();

                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            try {
                                const data = JSON.parse(line.substring(6));
                                console.log('[SNB SSE]', data.msg, JSON.stringify(data).substring(0, 200));

                                if (data.msg === 'process_completed') {
                                    const output = data.output?.data;
                                    console.log('[SNB] Output:', JSON.stringify(output));

                                    if (output && output.length > 1 && Array.isArray(output[1])) {
                                        const lastMessage = output[1][output[1].length - 1];
                                        console.log('[SNB] Last message:', lastMessage);

                                        if (lastMessage && lastMessage[1]) {
                                            let response = lastMessage[1];
                                            response = response.replace(/\n\n\*\[Contexte:.*?\]\*$/g, '');
                                            console.log('[SNB] Final response:', response.substring(0, 100));
                                            resolve(response);
                                            req.destroy();
                                            return;
                                        }
                                    }

                                    console.error('[SNB] Unexpected output format:', output);
                                    reject(new Error('Unexpected output format'));
                                    req.destroy();
                                    return;
                                }

                                if (data.msg === 'process_error') {
                                    reject(new Error(`Space error: ${data.error}`));
                                    req.destroy();
                                    return;
                                }
                            } catch (e) {
                                // Ligne SSE non-JSON, ignorer
                            }
                        }
                    }
                });

                res.on('end', async () => {
                    // Fallback si le flux SSE se termine sans résultat
                    console.warn('[SNB] SSE ended; trying predict sync fallback');
                    try {
                        const response = await predictSync("//chat_function", { data: [enrichedMessage, []] });
                        resolve(response);
                    } catch (e) {
                        reject(new Error('SSE stream ended without completion'));
                    }
                });
            });

            req.on('error', reject);
            req.on('timeout', () => {
                req.destroy();
                reject(new Error('SSE timeout'));
            });

            req.end();
        });

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
