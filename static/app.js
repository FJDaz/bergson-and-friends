// === UTILITAIRES GLOBAUX ===
const philosopherLabels = {
  bergson: 'Bergson',
  kant: 'Kant',
  spinoza: 'Spinoza'
};

function getPhilosopherLabel(id) {
  if (!id || typeof id !== 'string') return 'Le philosophe';
  return philosopherLabels[id] || id.charAt(0).toUpperCase() + id.slice(1);
}

// Questions amorces par philosophe
const INTRO_QUESTIONS = {
  spinoza: [
    "La liberté est-elle une illusion ?",
    "Peut-on maîtriser nos émotions ?",
    "Sommes-nous esclaves de nos désirs ?",
    "La connaissance rend-elle libre ?",
    "La joie accroît-elle notre puissance d'agir ?"
  ],
  bergson: [
    "Le temps intérieur peut-il se mesurer ?",
    "La durée est-elle la vraie nature du temps ?",
    "L'intuition dépasse-t-elle l'intelligence ?",
    "La conscience crée-t-elle le réel ?",
    "Peut-on saisir le mouvement autrement que par l'intellect ?"
  ],
  kant: [
    "Que puis-je savoir avec certitude ?",
    "Sommes-nous libres dans un monde déterminé ?",
    "L'impératif catégorique peut-il guider toutes nos actions ?",
    "L'expérience suffit-elle à fonder la connaissance ?",
    "La raison a-t-elle des limites ?"
  ],
  default: [
    "Quelle question philosophique t'intrigue aujourd'hui ?"
  ]
};

const INTRO_TEMPLATES = {
  spinoza: (question) => `Bonjour ! Je suis Spinoza. Discutons ensemble de cette question : <strong>${question}</strong>.<br><br>Qu'en penses-tu ?`,
  bergson: (question) => `Salut ! Je suis Bergson. Plongeons dans cette intuition : <strong>${question}</strong>.<br><br>Quel est ton ressenti ?`,
  kant: (question) => `Bonjour, je suis Kant. Examinons ce problème critique : <strong>${question}</strong>.<br><br>Quelle est ta position ?`,
  default: (question, label) => `Bonjour ! Je suis ${label}. Explorons ensemble : <strong>${question}</strong>.`
};

function pickIntroQuestion(philosopherId) {
  const list = INTRO_QUESTIONS[philosopherId] || INTRO_QUESTIONS.default;
  if (!list || list.length === 0) {
    return "Quelle question philosophique souhaites-tu explorer ?";
  }
  return list[Math.floor(Math.random() * list.length)];
}

function getIntroMessage(philosopherId) {
  const label = getPhilosopherLabel(philosopherId);
  const question = pickIntroQuestion(philosopherId);
  const template = INTRO_TEMPLATES[philosopherId] || ((q) => INTRO_TEMPLATES.default(q, label));
  return {
    question,
    html: template(question, label),
    label
  };
}

function injectDesktopIntro(philosopherId, qaHistory) {
  if (!qaHistory || qaHistory.dataset.introInjected === 'true') {
    return;
  }
  const intro = getIntroMessage(philosopherId);
  const introBlock = document.createElement('div');
  introBlock.className = 'qa-pair intro';
  introBlock.innerHTML = `<div class="answer"><strong>${intro.label} :</strong> ${intro.html}</div>`;
  qaHistory.appendChild(introBlock);
  qaHistory.dataset.introInjected = 'true';
  qaHistory.style.display = 'block';
}

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

      const qaHistory = article.querySelector('.qa-history');
      injectDesktopIntro(article.id, qaHistory);

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
        const label = getPhilosopherLabel(philosopherId);
        
        // Ajouter Q&R à l'historique
        const qaBlock = document.createElement('div');
        qaBlock.className = 'qa-pair';
        qaBlock.innerHTML = `
            <div class="question"><strong>Q:</strong> ${question}</div>
            <div class="answer loading"><strong>R:</strong> <em>${label} se réveille… (démarrage en cours)</em></div>
        `;
        qaHistory.appendChild(qaBlock);
        
        // Auto-scroll vers la nouvelle question
        setTimeout(() => scrollToLatestResponse(qaHistory), 100);
        
        // Vider le textarea
        textarea.value = '';
        
        let slowWakeHint;

        try {
            slowWakeHint = setTimeout(() => {
                const answerDiv = qaBlock.querySelector('.answer');
                if (answerDiv && answerDiv.classList.contains('loading')) {
                    answerDiv.innerHTML = `<strong>R:</strong> <em>${label} s'étire... encore quelques secondes.</em>`;
                }
            }, 8000);

            const response = await fetch(`/.netlify/functions/${philosopherId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
            });

            if (!response.ok) {
                throw new Error(`${response.status} ${response.statusText}`);
            }
            
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
            answerDiv.className = 'answer error';
            answerDiv.innerHTML = `<strong>R:</strong> <em>${label} est encore en train de se réveiller. Réessaie dans quelques instants. (${error.message})</em>`;
        }

        if (slowWakeHint) {
            clearTimeout(slowWakeHint);
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

  function injectMobileIntro(philosopher) {
    if (!mobileQaHistory) return;
    const intro = getIntroMessage(philosopher);
    const introBlock = document.createElement('div');
    introBlock.className = 'mobile-qa-pair intro';
    introBlock.innerHTML = `<div class="mobile-answer"><strong>${intro.label} :</strong> ${intro.html}</div>`;
    mobileQaHistory.appendChild(introBlock);
    mobileQaHistory.classList.add('has-content');
  }
  
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
    
    // Vider l'historique et injecter l'amorce
    if (mobileQaHistory) {
      mobileQaHistory.innerHTML = '';
      mobileQaHistory.classList.remove('has-content');
      injectMobileIntro(philosopher);
    }
    
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
      
      const label = getPhilosopherLabel(currentPhilosopher);

      // Ajouter la question à l'historique
      const qaBlock = document.createElement('div');
      qaBlock.className = 'mobile-qa-pair';
      qaBlock.innerHTML = `
        <div class="mobile-question">Q: ${question}</div>
        <div class="mobile-answer loading">${label} se réveille… (démarrage en cours)</div>
      `;
      mobileQaHistory.appendChild(qaBlock);
      mobileQaHistory.classList.add('has-content');
      
      // Scroll vers le bas
      mobileQaHistory.scrollTop = mobileQaHistory.scrollHeight;
      
      // Vider le textarea
      textarea.value = '';
      
      let slowWakeHint;

      try {
        slowWakeHint = setTimeout(() => {
          const answerDiv = qaBlock.querySelector('.mobile-answer');
          if (answerDiv && answerDiv.classList.contains('loading')) {
            answerDiv.textContent = `${label} s'étire... encore quelques secondes.`;
          }
        }, 8000);

        // Appel API
        const response = await fetch(`/.netlify/functions/${currentPhilosopher}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question })
        });

        if (!response.ok) {
          throw new Error(`${response.status} ${response.statusText}`);
        }
        
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
        answerDiv.className = 'mobile-answer error';
        answerDiv.textContent = `${label} est encore en train de se réveiller. Réessaie dans quelques instants. (${error.message})`;
      }

      if (slowWakeHint) {
        clearTimeout(slowWakeHint);
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
  
});