// EduVoice FR™ - Background Script (Service Worker)
// Fichier: extension/background.js

// Connexion WebSocket au backend
let socket;
let isConnected = false;
let currentTabId = null;

// Configuration du backend (à adapter)
const BACKEND_WS_URL = "ws://localhost:8000/ws/audio"; // ou l'URL de votre serveur

// Écouter les messages de l'extension (popup ou content script)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "connect") {
    connectToBackend();
    sendResponse({ status: "connecting" });
  } else if (request.action === "disconnect") {
    disconnectFromBackend();
    sendResponse({ status: "disconnected" });
  } else if (request.action === "startTranslation") {
    startTranslation(sender.tab.id);
    sendResponse({ status: "started" });
  } else if (request.action === "stopTranslation") {
    stopTranslation();
    sendResponse({ status: "stopped" });
  } else if (request.action === "getStatus") {
    sendResponse({ 
      isConnected, 
      isTranslating: currentTabId !== null 
    });
  }
  return true; // Pour sendResponse asynchrone
});

// Connexion au backend WebSocket
function connectToBackend() {
  if (isConnected) return;
  
  socket = new WebSocket(BACKEND_WS_URL);
  
  socket.onopen = () => {
    isConnected = true;
    console.log("Connecté au backend EduVoice FR™");
    chrome.runtime.sendMessage({ action: "connectionStatus", status: "connected" });
  };
  
  socket.onmessage = (event) => {
    // Recevoir l'audio traduit du backend et le jouer
    const audioBlob = new Blob([event.data], { type: "audio/wav" });
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play().catch(e => console.error("Erreur de lecture audio:", e));
  };
  
  socket.onclose = () => {
    isConnected = false;
    console.log("Déconnecté du backend");
    chrome.runtime.sendMessage({ action: "connectionStatus", status: "disconnected" });
  };
  
  socket.onerror = (error) => {
    console.error("Erreur WebSocket:", error);
    isConnected = false;
  };
}

// Déconnexion du backend
function disconnectFromBackend() {
  if (socket && isConnected) {
    socket.close();
    isConnected = false;
  }
}

// Démarrer la traduction pour un onglet
async function startTranslation(tabId) {
  if (!isConnected) {
    connectToBackend();
    // Attendre la connexion
    await new Promise(resolve => {
      const checkConnection = setInterval(() => {
        if (isConnected) {
          clearInterval(checkConnection);
          resolve();
        }
      }, 100);
    });
  }
  
  currentTabId = tabId;
  
  // Capturer l'audio de l'onglet
  try {
    const streamId = await chrome.tabCapture.captureAudio(tabId);
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: { mandatory: { chromeMediaSource: 'tab', chromeMediaSourceId: streamId } }
    });
    
    // Créer un MediaRecorder pour capturer l'audio
    const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
    let audioChunks = [];
    
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
        // Envoyer le chunk audio au backend
        const reader = new FileReader();
        reader.onload = () => {
          const audioData = new Uint8Array(reader.result);
          if (socket && isConnected) {
            socket.send(JSON.stringify({
              audio_data: Array.from(audioData),
              source: "youtube",
              language: "en"
            }));
          }
        };
        reader.readAsArrayBuffer(event.data);
      }
    };
    
    mediaRecorder.start(1000); // Envoyer des chunks toutes les 1s
    
    // Arrêter la capture si l'onglet est fermé ou la traduction arrêtée
    chrome.tabs.onRemoved.addListener((closedTabId) => {
      if (closedTabId === tabId) {
        mediaRecorder.stop();
        stopTranslation();
      }
    });
    
  } catch (error) {
    console.error("Erreur de capture audio:", error);
    stopTranslation();
  }
}

// Arrêter la traduction
function stopTranslation() {
  currentTabId = null;
  if (socket && isConnected) {
    socket.send(JSON.stringify({ action: "stop" }));
  }
}

// Gérer la fermeture de l'extension
chrome.runtime.onSuspend.addListener(() => {
  disconnectFromBackend();
});
