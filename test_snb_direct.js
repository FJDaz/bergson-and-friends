#!/usr/bin/env node
// Test direct de l'appel SNB pour diagnostiquer

const https = require('https');

const SPACE_URL = "fjdaz-spinoza-nb.hf.space";
const API_PREFIX = "/gradio_api";

async function testSNB() {
    console.log('🧪 Test direct SNB Space...\n');

    const message = "La liberté est-elle une illusion ?";

    try {
        // Étape 1: Initier la prédiction
        const payload = JSON.stringify({
            data: [message, []],
            session_hash: Math.random().toString(36).substring(2, 15)
        });

        console.log('📤 Envoi requête initiale...');
        const eventId = await new Promise((resolve, reject) => {
            const options = {
                hostname: SPACE_URL,
                port: 443,
                path: `${API_PREFIX}/call/chat_function`,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(payload)
                },
                timeout: 30000  // 30s
            };

            const req = https.request(options, (res) => {
                console.log(`   Status: ${res.statusCode}`);
                let data = '';
                res.on('data', (chunk) => { data += chunk; });
                res.on('end', () => {
                    console.log(`   Response: ${data}\n`);
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
                reject(new Error('Request timeout'));
            });

            req.write(payload);
            req.end();
        });

        console.log(`✅ Event ID reçu: ${eventId}\n`);

        // Étape 2: Écouter SSE
        console.log('📡 Écoute SSE stream...');
        const response = await new Promise((resolve, reject) => {
            const options = {
                hostname: SPACE_URL,
                port: 443,
                path: `${API_PREFIX}/call/chat_function/${eventId}`,
                method: 'GET',
                timeout: 120000  // 2min
            };

            const req = https.request(options, (res) => {
                console.log(`   SSE Status: ${res.statusCode}`);
                let buffer = '';

                res.on('data', (chunk) => {
                    buffer += chunk.toString();
                    const lines = buffer.split('\n');
                    buffer = lines.pop();

                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            try {
                                const data = JSON.parse(line.substring(6));
                                console.log(`   Event: ${data.msg}`);

                                if (data.msg === 'process_completed') {
                                    const output = data.output?.data;
                                    if (output && output.length > 1 && Array.isArray(output[1])) {
                                        const lastMessage = output[1][output[1].length - 1];
                                        if (lastMessage && lastMessage[1]) {
                                            resolve(lastMessage[1]);
                                            req.destroy();
                                            return;
                                        }
                                    }
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

                res.on('end', () => {
                    reject(new Error('SSE stream ended without completion'));
                });
            });

            req.on('error', reject);
            req.on('timeout', () => {
                req.destroy();
                reject(new Error('SSE timeout (90s)'));
            });

            req.end();
        });

        console.log('\n✅ SUCCÈS!\n');
        console.log('Réponse SNB:');
        console.log('─'.repeat(70));
        console.log(response);
        console.log('─'.repeat(70));

    } catch (error) {
        console.error('\n❌ ERREUR:', error.message);
        process.exit(1);
    }
}

testSNB();
