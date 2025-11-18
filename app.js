// app.js - Version production avec backend Railway

// Configuration API production
const API_BASE_URL = 'https://bergson-api-production.up.railway.app';

// État global
const philosopherStates = {
  bergson: { history: [], active: false },
  kant: { history: [], active: false },
  spinoza: { history: [], active: false }
};

// Initialisation au chargement
document.addEventListener('DOMContentLoaded', () => {
  console.log('✅ Bergson and Friends - Version locale');
  console.log(`📡 API Backend: ${API_BASE_URL}`);

  initPhilosophers();
});

function initPhilosophers() {
  const philosophers = ['bergson', 'kant', 'spinoza'];

  philosophers.forEach(phil => {
    const article = document.getElementById(phil);
    if (!article) return;

    const trigger = article.querySelector('.philosopher-trigger');
    const dialogue = article.querySelector('.dialogue');
    const form = article.querySelector('.qa-form');
    const textarea = article.querySelector('textarea');

    // Clic sur le philosophe pour ouvrir/fermer
    trigger.addEventListener('click', async () => {
      const wasHidden = dialogue.hidden;

      // Fermer tous les dialogues
      philosophers.forEach(p => {
        const d = document.getElementById(p)?.querySelector('.dialogue');
        if (d) d.hidden = true;
      });

      // Toggle le dialogue actuel
      dialogue.hidden = !wasHidden;

      // Si on ouvre et pas encore initialisé
      if (!wasHidden && !philosopherStates[phil].active) {
        await initConversation(phil);
      }

      // Focus sur textarea si ouvert
      if (!dialogue.hidden) {
        textarea.focus();
      }
    });

    // Soumission du formulaire
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      await sendMessage(phil);
    });

    // Submit sur Enter (sans Shift)
    textarea.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        form.dispatchEvent(new Event('submit'));
      }
    });
  });
}

async function initConversation(philosopher) {
  try {
    console.log(`[INIT] ${philosopher}...`);

    const response = await fetch(`${API_BASE_URL}/init/${philosopher}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    console.log(`[INIT] ${philosopher} OK`, data);
    console.log(`[INIT] Question: ${data.question}`);

    // Sauvegarder l'historique
    philosopherStates[philosopher].history = data.history;
    philosopherStates[philosopher].active = true;

    // Afficher la question du philosophe dans l'historique
    renderHistory(philosopher);

  } catch (error) {
    console.error(`[INIT ERROR] ${philosopher}:`, error);
    alert(`Erreur init ${philosopher}: ${error.message}\n\nVérifie que le backend tourne sur ${API_BASE_URL}`);
  }
}

async function sendMessage(philosopher) {
  const article = document.getElementById(philosopher);
  const textarea = article.querySelector('textarea');
  const form = article.querySelector('.qa-form');
  const submitBtn = form.querySelector('input[type="image"]');

  const userMessage = textarea.value.trim();
  if (!userMessage) return;

  // Désactiver pendant traitement
  textarea.disabled = true;
  submitBtn.style.opacity = '0.5';
  submitBtn.style.pointerEvents = 'none';

  try {
    console.log(`[CHAT] ${philosopher}: ${userMessage.substring(0, 50)}...`);

    const response = await fetch(`${API_BASE_URL}/chat/${philosopher}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: userMessage,
        history: philosopherStates[philosopher].history,
        philosopher: philosopher
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    console.log(`[CHAT] ${philosopher} réponse:`, data);

    // Afficher passages RAG en console
    if (data.rag_passages && data.rag_passages.length) {
      console.log(`[RAG] ${data.rag_passages.length} passages:`, data.rag_passages);
    }

    // Mettre à jour historique
    philosopherStates[philosopher].history = data.history;

    // Ré-afficher l'historique
    renderHistory(philosopher);

    // Réinitialiser textarea
    textarea.value = '';

  } catch (error) {
    console.error(`[CHAT ERROR] ${philosopher}:`, error);
    alert(`Erreur chat ${philosopher}: ${error.message}\n\nVérifie que le backend tourne sur ${API_BASE_URL}`);
  } finally {
    textarea.disabled = false;
    submitBtn.style.opacity = '1';
    submitBtn.style.pointerEvents = 'auto';
    textarea.focus();
  }
}

function renderHistory(philosopher) {
  const article = document.getElementById(philosopher);
  const historyDiv = article.querySelector('.qa-history');

  historyDiv.innerHTML = '';

  const history = philosopherStates[philosopher].history;

  for (const [userMsg, assistantMsg] of history) {
    // Message utilisateur
    if (userMsg) {
      const userDiv = document.createElement('div');
      userDiv.className = 'message user-message';
      userDiv.innerHTML = `<strong>Vous :</strong> ${escapeHtml(userMsg)}`;
      historyDiv.appendChild(userDiv);
    }

    // Message assistant
    if (assistantMsg) {
      const assistantDiv = document.createElement('div');
      assistantDiv.className = 'message assistant-message';

      // Nettoyer le message (enlever les métadonnées type "[Contexte: ...]")
      let cleanMsg = assistantMsg.replace(/\*\[.*?\]\*/g, '').trim();

      // Convertir markdown basique : **texte** → <strong>texte</strong>
      cleanMsg = cleanMsg.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

      // Convertir retours à la ligne
      cleanMsg = cleanMsg.replace(/\n/g, '<br>');

      assistantDiv.innerHTML = `<strong>${capitalize(philosopher)} :</strong> ${cleanMsg}`;
      historyDiv.appendChild(assistantDiv);
    }
  }

  // Scroll vers le bas
  historyDiv.scrollTop = historyDiv.scrollHeight;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

console.log('💡 Cliquez sur un philosophe pour démarrer la conversation');
console.log('⌨️  Utilisez Enter pour envoyer (Shift+Enter pour nouvelle ligne)');
