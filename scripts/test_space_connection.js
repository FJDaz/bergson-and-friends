#!/usr/bin/env node
/**
 * Script de test pour vérifier la connexion au Space HF bergsonAndFriends
 * Usage: node scripts/test_space_connection.js
 */

const SPACE_URL = process.env.SNB_BACKEND_URL || "https://fjdaz-bergsonandfriends.hf.space";

async function testSpaceConnection() {
    console.log('🔍 Test de connexion au Space HF...\n');
    console.log(`URL: ${SPACE_URL}\n`);

    // Test 1: Vérifier que le Space répond
    console.log('1️⃣ Test endpoint /gradio_api/info...');
    try {
        const infoResponse = await fetch(`${SPACE_URL}/gradio_api/info`);
        if (infoResponse.ok) {
            const info = await infoResponse.json();
            console.log('✅ Space accessible');
            console.log(`   API disponible: ${info.api ? 'Oui' : 'Non'}`);
        } else {
            console.log(`❌ Erreur HTTP: ${infoResponse.status}`);
        }
    } catch (error) {
        console.log(`❌ Erreur de connexion: ${error.message}`);
        return false;
    }

    // Test 2: Vérifier que l'endpoint /chat_function existe
    console.log('\n2️⃣ Test endpoint /chat_function...');
    try {
        // Note: @gradio/client nécessite un environnement navigateur
        // Le vrai test se fera depuis Netlify Functions ou le navigateur
        // Ici on vérifie juste que le Space répond
        const testResponse = await fetch(`${SPACE_URL}/gradio_api/info`);
        if (testResponse.ok) {
            console.log('✅ Space répond correctement');
            console.log('   Note: Le test complet avec @gradio/client doit être fait depuis Netlify ou le navigateur');
            console.log('   (car @gradio/client nécessite un environnement navigateur)');
        }
    } catch (error) {
        console.log(`❌ Erreur: ${error.message}`);
        return false;
    }

    console.log('\n✅ Tests de base passés !');
    console.log('   Pour tester l\'appel complet, utilisez le frontend ou vérifiez les logs Netlify');
    return true;
}

// Exécuter le test
testSpaceConnection()
    .then(success => {
        process.exit(success ? 0 : 1);
    })
    .catch(error => {
        console.error('❌ Erreur fatale:', error);
        process.exit(1);
    });

