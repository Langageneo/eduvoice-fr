# EduVoice FR™ - Capture Audio Linux (PulseAudio)
# Fichier: linux/audio_capture.py

import subprocess
import asyncio
import websockets
import json
import logging

# Config
BACKEND_WS_URL = "ws://localhost:8000/ws/audio"
SAMPLE_RATE = 16000  # 16kHz pour Faster-Whisper
CHANNELS = 1  # Mono

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Commande pour capturer l'audio avec PulseAudio (pacat)
# Installez pacat si nécessaire: sudo apt install pulseaudio-utils
PULSEAUDIO_CMD = [
    "pacat",
    "--record",
    "--format=s16le",
    "--rate=16000",
    "--channels=1",
    "--latency=1",
    "--process-time-msec=100",
    "--file=-"
]

async def capture_audio():
    """Capture l'audio système via PulseAudio et l'envoie au backend."""
    websocket = None
    process = None
    
    try:
        # Connexion WebSocket au backend
        websocket = await websockets.connect(BACKEND_WS_URL)
        logger.info("Connecté au backend WebSocket")
        
        # Démarrer la capture avec PulseAudio
        process = subprocess.Popen(
            PULSEAUDIO_CMD,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        logger.info("Capture audio démarrée (PulseAudio)")
        
        # Lire les chunks audio et les envoyer au backend
        while True:
            # Lire un chunk de données audio (1024 bytes = 64ms à 16kHz)
            chunk = process.stdout.read(1024)
            if not chunk:
                break
            
            # Envoyer au backend
            try:
                await websocket.send(json.dumps({
                    "audio_data": list(chunk),
                    "source": "linux",
                    "language": "en"
                }))
            except Exception as e:
                logger.error(f"Erreur lors de l'envoi audio: {e}")
                break
                
    except Exception as e:
        logger.error(f"Erreur dans capture_audio: {e}")
    finally:
        if websocket:
            await websocket.close()
        if process:
            process.terminate()

if __name__ == "__main__":
    try:
        asyncio.run(capture_audio())
    except KeyboardInterrupt:
        logger.info("Arrêt de la capture audio")
