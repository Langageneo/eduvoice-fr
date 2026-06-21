# EduVoice FR™ - Capture Audio Windows (WASAPI)
# Fichier: windows/audio_capture.py

import sounddevice as sd
import numpy as np
import websockets
import asyncio
import json
import logging

# Config
BACKEND_WS_URL = "ws://localhost:8000/ws/audio"
SAMPLE_RATE = 16000  # 16kHz pour Faster-Whisper
CHANNELS = 1  # Mono
BLOCKSIZE = 1024  # Taille des chunks audio

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variable globale pour le streaming
stream = None
websocket = None

async def capture_audio():
    """Capture l'audio système via WASAPI et l'envoie au backend."""
    global stream, websocket
    
    try:
        # Lister les périphériques audio (pour débogage)
        devices = sd.query_devices()
        logger.info("Périphériques audio disponibles:")
        for i, device in enumerate(devices):
            logger.info(f"{i}: {device['name']} (default: {device['default_samplerate']} Hz)")
        
        # Utiliser le périphérique par défaut (ou spécifier un ID)
        # Pour capturer l'audio système, utiliser un périphérique de type 'loopback'
        # Exemple: sur Windows, utiliser 'CABLE Input' ou 'Stereo Mix'
        input_device = None  # None = périphérique par défaut
        
        # Connexion WebSocket au backend
        websocket = await websockets.connect(BACKEND_WS_URL)
        logger.info("Connecté au backend WebSocket")
        
        # Callback pour traiter les chunks audio
        def audio_callback(indata, frames, time, status):
            if status:
                logger.warning(f"Erreur audio: {status}")
            
            # Convertir en bytes (16-bit PCM)
            audio_data = (indata * 32767).astype(np.int16).tobytes()
            
            # Envoyer au backend
            try:
                asyncio.run_coroutine_threadsafe(
                    websocket.send(json.dumps({
                        "audio_data": list(audio_data),
                        "source": "windows",
                        "language": "en"
                    })),
                    asyncio.get_event_loop()
                )
            except Exception as e:
                logger.error(f"Erreur lors de l'envoi audio: {e}")
        
        # Démarrer le streaming
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            callback=audio_callback,
            blocksize=BLOCKSIZE,
            device=input_device,
            dtype='float32'
        ):
            logger.info("Capture audio démarrée (appuyez sur Ctrl+C pour arrêter)")
            while True:
                await asyncio.sleep(0.1)
                
    except Exception as e:
        logger.error(f"Erreur dans capture_audio: {e}")
    finally:
        if websocket:
            await websocket.close()
        if stream:
            stream.close()

if __name__ == "__main__":
    try:
        asyncio.run(capture_audio())
    except KeyboardInterrupt:
        logger.info("Arrêt de la capture audio")
