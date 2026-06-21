// EduVoice FR™ - Content Script (Injecté dans les pages YouTube, Udemy, etc.)
// Fichier: extension/content_script.js

// Créer et injecter le bouton "Écouter en FR" dans la page
function injectButton() {
  // Vérifier si le bouton existe déjà
  if (document.getElementById('eduvoice-button')) return;

  // Créer le bouton
  const button = document.createElement('button');
  button.id = 'eduvoice-button';
  button.innerHTML = '🎧 Écouter en Français';
  button.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 9999;
    padding: 10px 16px;
    background-color: #1976d2;
    color: white;
    border: none;
    border-radius: 20px;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    transition: background-color 0.3s, transform 0.2s;
  `;

  // Effets au survol
  button.addEventListener('mouseenter', () => {
    button.style.backgroundColor = '#1565c0';
    button.style.transform = 'scale(1.05)';
  });
  button.addEventListener('mouseleave', () => {
    button.style.backgroundColor = '#1976d2';
    button.style.transform = 'scale(1)';
  });

  // Gestion du clic
  button.addEventListener('click', () => {
    // Envoyer un message au background script pour démarrer la traduction
    chrome.runtime.sendMessage({ 
      action: "startTranslation", 
      tabId: null // Le background script utilisera l'onglet actuel
    }, (response) => {
      if (response.status === "started") {
        button.style.backgroundColor = '#4caf50';
        button.textContent = '✓ Traduction active';
      } else {
        button.style.backgroundColor = '#f44336';
        button.textContent = '✗ Erreur';
        setTimeout(() => {
          button.style.backgroundColor = '#1976d2';
          button.textContent = '🎧 Écouter en Français';
        }, 2000);
      }
    });
  });

  // Ajouter le bouton à la page
  document.body.appendChild(button);
}

// Attendre que la page soit complètement chargée
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', injectButton);
} else {
  injectButton();
}

// Écouter les messages du background script (pour mettre à jour le bouton)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "translationStatus") {
    const button = document.getElementById('eduvoice-button');
    if (button) {
      if (request.status === "started") {
        button.style.backgroundColor = '#4caf50';
        button.textContent = '✓ Traduction active';
      } else if (request.status === "stopped") {
        button.style.backgroundColor = '#1976d2';
        button.textContent = '🎧 Écouter en Français';
      }
    }
  }
});
