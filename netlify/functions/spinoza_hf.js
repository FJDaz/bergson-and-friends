const { Client } = require("@gradio/client");

const QUESTIONS_BAC = [
  "La liberté est-elle une illusion ?",
  "Suis-je esclave de mes désirs ?",
  "La raison peut-elle tout expliquer ?"
];

let gradioClient = null;

async function getClient() {
  if (!gradioClient) {
    gradioClient = await Client.connect("FJDaz/bergsonAndFriends");
  }
  return gradioClient;
}

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') return { statusCode: 200, headers, body: '' };
  if (event.httpMethod !== 'POST') return { statusCode: 405, headers, body: '{}' };

  try {
    const { action, message, history } = JSON.parse(event.body);

    if (action === 'init') {
      const question = QUESTIONS_BAC[Math.floor(Math.random() * QUESTIONS_BAC.length)];
      const greeting = `Bonjour ! Je suis Spinoza.\n\n**${question}**\n\nQu'en penses-tu ?`;
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ question, greeting, history: [[null, greeting]] })
      };
    }

    if (action === 'chat') {
      const client = await getClient();
      const result = await client.predict("/chat_function", {
        message,
        history: history || []
      });
      const updatedHistory = result.data[1];
      const reply = updatedHistory[updatedHistory.length - 1][1];
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ reply, history: updatedHistory })
      };
    }

    return { statusCode: 400, headers, body: '{"error":"Invalid action"}' };
  } catch (err) {
    return { statusCode: 500, headers, body: JSON.stringify({ error: err.message }) };
  }
};
