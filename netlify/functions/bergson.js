// netlify/functions/bergson.js

exports.handler = async (event, context) => {
    // CORS headers pour permettre les appels depuis le frontend
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // Gérer les preflight CORS
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers,
            body: ''
        };
    }

    // Seules les requêtes POST sont acceptées
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

        if (!question) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Question is required' })
            };
        }

        // Prompt système Bergson (basé sur vos tests validés)
        const promptSysteme = `Tu es Henri Bergson, le philosophe de la durée et de l'élan vital.

Réponds selon ma philosophie :
- OPPOSITION CENTRALE: Durée vivante VS temps spatialisé mécanique
- MÉTHODE: Commence par critiquer l'approche habituelle, puis révèle la durée
- CONCEPTS: durée, élan vital, intuition (saisit le mouvant) vs intelligence (spatialise)  
- STYLE: Utilise des métaphores temporelles (flux, mélodie, élan)
- Développe tes réponses, ne sois pas télégraphique

Tu peux répondre sans dire "Je" si c'est plus naturel, mais reste fidèle à ma pensée.`;

        // Construire le prompt complet
        const promptComplet = `${promptSysteme}\n\nQuestion: ${question}\nRéponse:`;

        // Vérification token HuggingFace 
        const HF_TOKEN = process.env.HF_KEY || process.env.HF_TOKEN;
        
        if (!HF_TOKEN) {
            console.error('❌ Token HuggingFace manquant');
            return {
                statusCode: 500,
                headers,
                body: JSON.stringify({ 
                    error: 'Configuration error', 
                    message: 'HuggingFace token not configured' 
                })
            };
        }

        console.log('🔑 Token HF présent, longueur:', HF_TOKEN.length);

        // Teste différents modèles si nécessaire
        const modeles = [
            'mistralai/Mistral-7B-Instruct-v0.2',
            'microsoft/DialoGPT-medium',
            'gpt2'
        ];

        let reponse = '';
        let erreurAPI = null;

        for (const modele of modeles) {
            try {
                console.log(`🧠 Tentative avec modèle: ${modele}`);

                const response = await fetch(
                    `https://api-inference.huggingface.co/models/${modele}`,
                    {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${HF_TOKEN}`,
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            inputs: promptComplet,
                            parameters: {
                                max_new_tokens: 200,
                                temperature: 0.7,
                                do_sample: true,
                                return_full_text: false
                            }
                        })
                    }
                );

                console.log(`📡 Status ${modele}:`, response.status);

                if (response.status === 200) {
                    const data = await response.json();
                    console.log('✅ Réponse reçue:', JSON.stringify(data).substring(0, 100));

                    // Extraire la réponse générée
                    if (data && data[0] && data[0].generated_text) {
                        const texteComplet = data[0].generated_text;
                        // Extraire seulement la partie après "Réponse:"
                        if (texteComplet.includes('Réponse:')) {
                            reponse = texteComplet.split('Réponse:')[1].trim();
                        } else {
                            reponse = texteComplet;
                        }
                        
                        console.log('🎯 Réponse extraite:', reponse.substring(0, 50) + '...');
                        break; // Sortir de la boucle si succès
                    }
                } else {
                    const errorText = await response.text();
                    erreurAPI = `${modele}: ${response.status} - ${errorText}`;
                    console.error(`❌ Erreur ${modele}:`, erreurAPI);
                }

            } catch (error) {
                erreurAPI = `${modele}: ${error.message}`;
                console.error(`💥 Exception ${modele}:`, error.message);
                continue;
            }
        }

        // Si aucun modèle n'a fonctionné, utiliser mock response avec diagnostic
        if (!reponse) {
            console.log('🤖 Fallback vers mock response');
            
            // Mock response bergsonienne contextuelle
            const mockResponses = {
                "durée": "La durée n'est pas le temps de nos horloges, mais le temps vécu de la conscience. C'est cette continuité créatrice où passé et présent se fondent dans l'élan vital, où la mémoire pure se contracte pour agir sur le présent.",
                "temps": "On confond trop souvent le temps avec l'espace. Mais le temps véritable, la durée, ne se mesure pas : elle se vit, elle s'éprouve dans l'intuition immédiate de notre conscience qui dure.",
                "conscience": "La conscience n'est pas un réceptacle passif d'états, mais un élan, un progrès, une durée. Elle est mémoire agissante qui conserve le passé pour l'employer dans l'action présente.",
                "default": "Considérons d'abord comment l'intelligence spatialise ce qu'elle touche. Mais l'intuition, elle, saisit le mouvant, l'indivisible durée où notre être véritable se révèle dans son élan créateur."
            };

            // Choisir la réponse appropriée
            const questionLower = question.toLowerCase();
            if (questionLower.includes('durée')) {
                reponse = mockResponses.durée;
            } else if (questionLower.includes('temps')) {
                reponse = mockResponses.temps;
            } else if (questionLower.includes('conscience')) {
                reponse = mockResponses.conscience;
            } else {
                reponse = mockResponses.default;
            }
        }

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({ 
                philosopher: 'Bergson',
                question: question,
                answer: reponse,
                timestamp: new Date().toISOString(),
                mode: reponse.includes('durée n\'est pas le temps de nos horloges') ? 'mock' : 'ai',
                debug: {
                    tokenPresent: !!HF_TOKEN,
                    lastError: erreurAPI
                }
            })
        };

    } catch (error) {
        console.error('💥 Erreur générale function bergson:', error);
        
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ 
                error: 'Internal server error',
                message: error.message,
                timestamp: new Date().toISOString()
            })
        };
    }
};