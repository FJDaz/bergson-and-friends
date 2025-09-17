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

        // Appeler l'API HuggingFace
        console.log('HF_KEY exists:', !!process.env.HF_KEY);
        console.log('HF_KEY length:', process.env.HF_KEY ? process.env.HF_KEY.length : 0);
        
        const response = await fetch('https://api-inference.huggingface.co/models/microsoft/DialoGPT-small', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${process.env.HF_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                inputs: promptComplet
            })
        });

        if (!response.ok) {
            throw new Error(`HuggingFace API error: ${response.status}`);
        }

        const data = await response.json();
        
        // Extraire la réponse générée
        let reponse = '';
        if (data && data[0] && data[0].generated_text) {
            const texteComplet = data[0].generated_text;
            // Extraire seulement la partie après "Réponse:"
            if (texteComplet.includes('Réponse:')) {
                reponse = texteComplet.split('Réponse:')[1].trim();
            } else {
                reponse = texteComplet;
            }
        } else {
            throw new Error('Invalid response format from HuggingFace');
        }

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({ 
                philosopher: 'Bergson',
                question: question,
                answer: reponse,
                timestamp: new Date().toISOString()
            })
        };

    } catch (error) {
        console.error('Error in bergson function:', error);
        
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ 
                error: 'Internal server error',
                message: error.message 
            })
        };
    }
};