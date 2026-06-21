// EduVoice FR™ - Popup Script
// Fichier: extension/popup/popup.js

document.addEventListener('DOMContentLoaded', () => {
  const connectButton = document.getElementById('connectButton');
  const translateButton = document.getElementById('translateButton');
  const stopButton = document.getElementById('stopButton');
  const statusIcon = document.getElementById('status-icon');
  const statusText = document.getElementById('status-text');
  const errorMessage = document.getElementById('errorMessage');
  const settingsLink = document.getElementById('settingsLink');

  let isConnected = false;
  let isTranslating = false;

  // Mettre à jour l'interface en fonction du statut
  function updateUI() {
    if (isConnected) {
      statusIcon.textContent = '✓';
      statusText.textContent = 'Connecté';
      statusIcon.className = 'status-icon status-connected';
      translateButton.disabled = false;
      connectButton.textContent = 'Déconnecter';
    } else {
      statusIcon.textContent = '✗';
      statusText.textContent = 'Non connecté';
      statusIcon.className = 'status-icon status-disconnected';
      translateButton.disabled = true;
      connectButton.textContent = 'Connecter au backend';
    }

    if (isTranslating) {
      translateButton.disabled = true;
      stopButton.disabled = false;
    } else {
      translateButton.disabled = !isConnected;
      stopButton.disabled = true;
    }
  }

  // Connexion/Déconnexion au backend
  connectButton.addEventListener('click', async () => {
    errorMessage.textContent = '';
    
    if (isConnected) {
      // Déconnecter
      chrome.runtime.sendMessage({ action: "disconnect" }, (response) => {
        isConnected = false;
        updateUI();
      });
    } else {
      // Connecter
      chrome.runtime.sendMessage({ action: "connect" }, (response) => {
        if (response.status === "connecting") {
          // Attendre la confirmation de connexion
          setTimeout(() => {
            chrome.runtime.sendMessage({ action: "getStatus" }, (response) => {
              isConnected = response.isConnected;
              updateUI();
            });
          }, 1000);
        }
      });
    }
  });

  // Démarrer la traduction
  translateButton.addEventListener('click', async () => {
    errorMessage.textContent = '';
    
    // Vérifier si on est sur une page YouTube ou autre plateforme supportée
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const tab = tabs[0];
      const url = tab.url;
      
      if (!url.includes("youtube.com") && 
          !url.includes("udemy.com") && 
          !url.includes("coursera.org") &&
          !url.includes("twitch.tv") &&
          !url.includes("zoom.us") &&
          !url.includes("meet.google.com")) {
        errorMessage.textContent = 'Plateforme non supportée';
        return;
      }

      // Demander la permission de capture audio
      chrome.permissions.request({ permissions: ['tabCapture'] }, (granted) => {
        if (!granted) {
          errorMessage.textContent = 'Permission de capture audio refusée';
          return;
        }

        // Démarrer la traduction
        chrome.runtime.sendMessage({ 
          action: "startTranslation", 
          tabId: tab.id 
        }, (response) => {
          if (response.status === "started") {
            isTranslating = true;
            updateUI();
          } else {
            errorMessage.textContent = 'Erreur de démarrage';
          }
        });
      });
    });
  });

  // Arrêter la traduction
  stopButton.addEventListener('click', () => {
    chrome.runtime.sendMessage({ action: "stopTranslation" }, (response) => {
      isTranslating = false;
      updateUI();
    });
  });

  // Lien vers les paramètres (à implémenter)
  settingsLink.addEventListener('click', () => {
    chrome.tabs.create({ url: chrome.runtime.getURL('settings.html') });
  });

  // Vérifier le statut initial
  chrome.runtime.sendMessage({ action: "getStatus" }, (response) => {
    isConnected = response.isConnected;
    isTranslating = response.isTranslating;
    updateUI();
  });
});
