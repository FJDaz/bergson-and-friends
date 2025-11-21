// === CONFIGURATION API ===
// URL de l'API Netlify Functions
// Si le site est sur fjdaz.com, utiliser l'URL complète Netlify
// Exemple: 'https://votre-site.netlify.app/.netlify/functions/philosopher_rag'
// Ou si proxy configuré: '/api/philosopher_rag'
const API_BASE_URL = window.location.hostname === 'fjdaz.com' 
    ? 'https://chimerical-kashata-65179e.netlify.app/.netlify/functions'
    : '/.netlify/functions';  // Chemin relatif si sur Netlify

// === DÉTECTION MOBILE ===
function isMobile() {
    return window.innerWidth <= 768;
}

// === GESTION OUVERTURE/FERMETURE PHILOSOPHES ===
const philosophers = document.querySelectorAll('.philosopher');

document.querySelectorAll('.philosopher-trigger').forEach(trigger => {
  trigger.addEventListener('click', () => {
    const article = trigger.closest('.philosopher');
    const isActive = article.classList.contains('active');

    // Fermer tous les autres et reset leurs translations
    philosophers.forEach(philo => {
      philo.classList.remove('active');
      philo.style.transform = '';
      philo.querySelector('.dialogue').hidden = true;
    });

    if (!isActive) {
      article.classList.add('active');
      article.querySelector('.dialogue').hidden = false;

      // === LOGIQUE DIFFÉRENTE SELON DESKTOP/MOBILE ===
      if (!isMobile()) {
        // === DESKTOP : Comportement original avec translateX ===
        const scale = 2;
        const rect = article.getBoundingClientRect();

        philosophers.forEach(philo => {
          if (philo !== article) {
            const philoRect = philo.getBoundingClientRect();
            const dx = (rect.width * (scale - 1)) / 2;

            if (philoRect.left < rect.left) {
              philo.style.transform = `translateX(-${dx}px)`;
            } else if (philoRect.left > rect.left) {
              philo.style.transform = `translateX(${dx}px)`;
            }
          }
        });
      }
      // === MOBILE : Pas de translateX, le CSS order s'occupe du layout ===
      // (rien à faire, le CSS gère via order: -1)
    }
  });
});

// === GESTION RESIZE WINDOW ===
// Nettoyer les transforms si on passe de desktop à mobile
window.addEventListener('resize', () => {
  if (isMobile()) {
    philosophers.forEach(philo => {
      // Nettoyer les translateX qui pourraient traîner
      if (philo.style.transform && philo.style.transform.includes('translateX')) {
        philo.style.transform = '';
      }
    });
  }
});

// === AUTO-SCROLL INTELLIGENT ===
function scrollToLatestResponse(qaHistory) {
    const lastResponse = qaHistory.lastElementChild;
    if (!lastResponse) return;
    
    // Position pour afficher la dernière réponse juste sous le bord supérieur
    const lastResponseTop = lastResponse.offsetTop;
    const targetScrollTop = Math.max(0, lastResponseTop - 20);
    
    qaHistory.scrollTo({
        top: targetScrollTop,
        behavior: 'smooth'
    });
}

// === GESTION FORMULAIRES UNIFIÉE ===
document.querySelectorAll('.qa-form').forEach(form => {
    const textarea = form.querySelector('textarea');
    const qaHistory = form.parentElement.querySelector('.qa-history');
    
    // Fonction pour envoyer la question
    async function sendQuestion() {
        const question = textarea.value.trim();
        if (!question) return;

        const philosopherId = form.closest('.philosopher').id;
        
        // Ajouter Q&R à l'historique
        const qaBlock = document.createElement('div');
        qaBlock.className = 'qa-pair';
        qaBlock.innerHTML = `
            <div class="question"><strong>Q:</strong> ${question}</div>
            <div class="answer loading"><strong>R:</strong> <em>Réflexion en cours...</em></div>
        `;
        qaHistory.appendChild(qaBlock);
        
        // Auto-scroll vers la nouvelle question
        setTimeout(() => scrollToLatestResponse(qaHistory), 100);
        
        // Vider le textarea
        textarea.value = '';
        
        try {
            // Récupérer l'historique actuel
            const historyPairs = Array.from(qaHistory.querySelectorAll('.qa-pair'));
            const history = historyPairs.map(pair => {
                const q = pair.querySelector('.question')?.textContent.replace(/^Q:\s*/, '') || '';
                const a = pair.querySelector('.answer')?.textContent.replace(/^R:\s*/, '') || '';
                return q && a ? [q, a] : null;
            }).filter(h => h !== null);
            
            const response = await fetch(`${API_BASE_URL}/philosopher_rag`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    action: 'respond',
                    philosopher: philosopherId,
                    message: question,
                    history: history
                })
            });
            
            const data = await response.json();
            
            // Remplacer le "loading" par la vraie réponse
            const answerDiv = qaBlock.querySelector('.answer');
            answerDiv.className = 'answer';
            answerDiv.innerHTML = `<strong>R:</strong> ${data.answer || 'Erreur: Pas de réponse'}`;
            
            // Auto-scroll vers la réponse complète
            setTimeout(() => scrollToLatestResponse(qaHistory), 100);
            
        } catch (error) {
            console.error('Erreur API:', error);
            const answerDiv = qaBlock.querySelector('.answer');
            answerDiv.innerHTML = `<strong>R:</strong> <em>Erreur technique: ${error.message}</em>`;
        }
        
        // Focus sur le textarea pour la prochaine question
        textarea.focus();
    }
    
    // === ENVOI PAR ENTER ===
    textarea.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendQuestion();
        }
    });
    
    // === ENVOI PAR BOUTON ===
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        sendQuestion();
    });
});

// === JAVASCRIPT MOBILE DÉDIÉ ===
document.addEventListener('DOMContentLoaded', function() {
  
  // Variables globales mobile
  const mobilePhilosophers = document.querySelector('.mobile-philosophers');
  const mobileConversation = document.querySelector('.mobile-conversation');
  const mobileActiveImg = document.getElementById('mobile-active-img');
  const mobileActiveName = document.getElementById('mobile-active-name');
  const mobileQaHistory = document.getElementById('mobile-qa-history');
  const mobileQaForm = document.getElementById('mobile-qa-form');
  const mobileBackButton = document.getElementById('mobile-back-button');
  
  let currentPhilosopher = null;
  
  // Données philosophes
  const philosophersData = {
    bergson: {
      name: 'Henri Bergson',
      img: 'https://fjdaz.com/bergson/statics/img/Bergson.png',
      greeting: 'Bonjour, cher ami. Explorons ensemble les méandres de la conscience et de la durée.'
    },
    kant: {
      name: 'Immanuel Kant', 
      img: 'https://fjdaz.com/bergson/statics/img/Kant.png',
      greeting: 'Guten Tag. Questionnons ensemble les limites de la raison et les conditions de la connaissance.'
    },
    spinoza: {
      name: 'Baruch Spinoza',
      img: 'https://fjdaz.com/bergson/statics/img/Spinoza.png', 
      greeting: 'Salve. Raisonnons ensemble selon l\'ordre géométrique et la nécessité de la Nature.'
    }
  };
  
  // Affichage version mobile si nécessaire
  if (isMobile()) {
    const desktopVersion = document.querySelector('.desktop-version');
    const mobileVersion = document.querySelector('.mobile-version');
    if (desktopVersion) desktopVersion.style.display = 'none';
    if (mobileVersion) mobileVersion.style.display = 'block';
  }
  
  // Event listeners philosophes mobile
  document.querySelectorAll('.mobile-philosopher-trigger').forEach(trigger => {
    trigger.addEventListener('click', function() {
      const philosopher = this.closest('.mobile-philosopher').dataset.philosopher;
      showMobileConversation(philosopher);
    });
  });
  
  // Afficher conversation mobile
  function showMobileConversation(philosopher) {
    if (!mobileConversation || !mobileActiveImg || !mobileActiveName) return;
    
    currentPhilosopher = philosopher;
    const data = philosophersData[philosopher];
    
    // Mettre à jour le philosophe actif
    mobileActiveImg.src = data.img;
    mobileActiveImg.alt = data.name;
    mobileActiveName.textContent = data.name;
    const greetingEl = document.querySelector('.mobile-greeting');
    if (greetingEl) greetingEl.textContent = data.greeting;
    
    // Vider l'historique
    if (mobileQaHistory) mobileQaHistory.innerHTML = '';
    
    // Basculer l'affichage
    if (mobilePhilosophers) mobilePhilosophers.style.display = 'none';
    if (mobileConversation) mobileConversation.style.display = 'block';
  }
  
  // Bouton retour
  if (mobileBackButton) {
    mobileBackButton.addEventListener('click', function() {
      if (mobileConversation) mobileConversation.style.display = 'none';
      if (mobilePhilosophers) mobilePhilosophers.style.display = 'block';
      currentPhilosopher = null;
    });
  }
  
  // Formulaire mobile
  if (mobileQaForm) {
    mobileQaForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      const textarea = this.querySelector('textarea');
      const question = textarea.value.trim();
      if (!question || !currentPhilosopher) return;
      
      // Ajouter la question à l'historique
      const qaBlock = document.createElement('div');
      qaBlock.className = 'mobile-qa-pair';
      qaBlock.innerHTML = `
        <div class="mobile-question">Q: ${question}</div>
        <div class="mobile-answer loading">Réflexion en cours...</div>
      `;
      mobileQaHistory.appendChild(qaBlock);
      
      // Scroll vers le bas
      mobileQaHistory.scrollTop = mobileQaHistory.scrollHeight;
      
      // Vider le textarea
      textarea.value = '';
      
      try {
        // Récupérer l'historique actuel
        const historyPairs = Array.from(mobileQaHistory.querySelectorAll('.mobile-qa-pair'));
        const history = historyPairs.map(pair => {
          const q = pair.querySelector('.mobile-question')?.textContent.replace(/^Q:\s*/, '') || '';
          const a = pair.querySelector('.mobile-answer')?.textContent || '';
          return q && a ? [q, a] : null;
        }).filter(h => h !== null);
        
        // Appel API
        const response = await fetch(`${API_BASE_URL}/philosopher_rag`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            action: 'respond',
            philosopher: currentPhilosopher,
            message: question,
            history: history
          })
        });
        
        const data = await response.json();
        
        // Remplacer par la vraie réponse
        const answerDiv = qaBlock.querySelector('.mobile-answer');
        answerDiv.className = 'mobile-answer';
        answerDiv.textContent = data.answer || 'Erreur: Pas de réponse';
        
        // Scroll vers le bas
        mobileQaHistory.scrollTop = mobileQaHistory.scrollHeight;
        
      } catch (error) {
        console.error('Erreur API:', error);
        const answerDiv = qaBlock.querySelector('.mobile-answer');
        answerDiv.textContent = `Erreur technique: ${error.message}`;
      }
      
      // Focus sur le textarea
      textarea.focus();
    });
  }
  
  // Gestion resize
  window.addEventListener('resize', function() {
    const desktopVersion = document.querySelector('.desktop-version');
    const mobileVersion = document.querySelector('.mobile-version');
    
    if (isMobile()) {
      if (desktopVersion) desktopVersion.style.display = 'none';
      if (mobileVersion) mobileVersion.style.display = 'block';
    } else {
      if (desktopVersion) desktopVersion.style.display = 'block';
      if (mobileVersion) mobileVersion.style.display = 'none';
    }
  });

  // === AUTO-INIT GREETINGS POUR LES 3 PHILOSOPHES ===
  // Initialiser chaque philosophe au chargement de la page
  async function initPhilosopher(philosopherId) {
    try {
      const response = await fetch(`${API_BASE_URL}/philosopher_rag`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'init',
          philosopher: philosopherId
        })
      });

      const data = await response.json();

      // Afficher le greeting dans l'historique
      const qaHistory = document.querySelector(`#${philosopherId} .qa-history`);
      if (qaHistory && data.greeting) {
        qaHistory.innerHTML = `
          <div class="qa-pair initial-greeting">
            <div class="answer">${data.greeting.replace(/\n/g, '<br>')}</div>
          </div>
        `;
      }

      console.log(`✅ ${philosopherId} initialized:`, data.question);

    } catch (error) {
      console.error(`❌ Failed to init ${philosopherId}:`, error);
    }
  }

  // Initialiser les 3 philosophes au chargement
  if (!isMobile()) {
    ['bergson', 'kant', 'spinoza'].forEach(id => initPhilosopher(id));
  }

});