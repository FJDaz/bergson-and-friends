// netlify/functions/bergson.js
// Endpoint Bergson - Système B unifié (RAG + SNB)

const philosopherRag = require('./philosopher_rag');

exports.handler = async (event, context) => {
    // Rediriger vers philosopher_rag avec philosophe fixé
    const body = event.body ? JSON.parse(event.body) : {};

    // Si c'est une simple question (ancien format), convertir en nouveau format
    if (body.question && !body.action) {
        const modifiedEvent = {
            ...event,
            body: JSON.stringify({
                action: 'respond',
                philosopher: 'bergson',
                message: body.question,
                history: []
            })
        };
        return philosopherRag.handler(modifiedEvent, context);
    }

    // Sinon, passer tel quel avec philosophe fixé
    const modifiedEvent = {
        ...event,
        body: JSON.stringify({
            ...body,
            philosopher: 'bergson'
        })
    };

    return philosopherRag.handler(modifiedEvent, context);
};
