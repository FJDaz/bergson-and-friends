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

      // Calculer déplacement des voisins
      const scale = 2;
      const rect = article.getBoundingClientRect();

      philosophers.forEach(philo => {
        if (philo !== article) {
          const philoRect = philo.getBoundingClientRect();
          const dx = (rect.width * (scale - 1)) / 2; // ajustement horizontal simple
          const dy = (rect.height * (scale - 1)) / 2; // ajustement vertical si nécessaire

          // Déplacement selon la position relative
          if (philoRect.left < rect.left) {
            philo.style.transform = `translateX(-${dx}px)`;
          } else if (philoRect.left > rect.left) {
            philo.style.transform = `translateX(${dx}px)`;
          }

          // Si besoin, tu peux ajuster verticalement
          // if (philoRect.top < rect.top) philo.style.transform += ` translateY(-${dy}px)`;
          // else if (philoRect.top > rect.top) philo.style.transform += ` translateY(${dy}px)`;
        }
      });
    }
  });
});

// Gestion formulaire Q/R
document.querySelectorAll('.qa-form').forEach(form => {
  form.addEventListener('submit', e => {
    e.preventDefault();
    const textarea = form.querySelector('textarea');
    const text = textarea.value.trim();
    if (!text) return;

    const qaHistory = form.parentElement.querySelector('.qa-history');
    const div = document.createElement('div');
    div.className = 'qa';
    div.textContent = "Vous : " + text;
    qaHistory.appendChild(div);

    textarea.value = '';
  });
});

// Gestion des formulaires
document.querySelectorAll('.qa-form').forEach(form => {
  form.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const textarea = form.querySelector('textarea');
      const question = textarea.value.trim();
      const philosopherId = form.closest('.philosopher').id;
      
      if (!question) return;
      
      try {
          const response = await fetch(`/.netlify/functions/${philosopherId}`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ question })
          });
          
          const data = await response.json();
          
          // Afficher la réponse dans qa-history
          const history = form.parentElement.querySelector('.qa-history');
          const qaBlock = document.createElement('div');
          qaBlock.innerHTML = `
              <div class="question">Q: ${question}</div>
              <div class="answer">R: ${data.answer}</div>
          `;
          history.appendChild(qaBlock);
          
          // Vider le textarea
          textarea.value = '';
          
      } catch (error) {
          console.error('Erreur:', error);
      }
  });
});
