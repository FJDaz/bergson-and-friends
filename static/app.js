// === MODIFICATIONS À APPORTER DANS app.js ===

// === DÉTECTION MOBILE ===
function isMobile() {
    return window.innerWidth <= 768;
}

// === GESTION OUVERTURE/FERMETURE PHILOSOPHES (MODIFIÉE) ===
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

// === AUTO-SCROLL INTELLIGENT (INCHANGÉ) ===
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

// === GESTION FORMULAIRES UNIFIÉE (INCHANGÉE) ===
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
            const response = await fetch(`/.netlify/functions/${philosopherId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
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
    
    // === ENVOI PAR ENTER (INCHANGÉ) ===
    textarea.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendQuestion();
        }
    });
    
    // === ENVOI PAR BOUTON (INCHANGÉ) ===
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        sendQuestion();
    });
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

// === GESTION FORMULAIRES UNIFIÉE (REMPLACE LES 3 ANCIENS) ===
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
            const response = await fetch(`/.netlify/functions/${philosopherId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
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
    
    // === ENVOI PAR ENTER (NOUVEAU) ===
    textarea.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendQuestion();
        }
    });
    
    // === ENVOI PAR BOUTON (NETTOYÉ) ===
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        sendQuestion();
    });
});

// === CSS AUTO-INJECTION POUR SCROLL ===
const style = document.createElement('style');
style.textContent = `
.qa-history {
    max-height: 400px;
    overflow-y: auto;
    scroll-behavior: smooth;
    padding: 10px;
}

.qa-pair {
    margin-bottom: 15px;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
}

.question, .answer {
    margin-bottom: 5px;
    line-height: 1.4;
}

.answer.loading {
    opacity: 0.7;
    font-style: italic;
}
`;
document.head.appendChild(style);