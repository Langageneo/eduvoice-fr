# EduVoice FR™ - Synthèse Vocale (Piper TTS)
# Fichier: backend/app/models/tts.py

from piper import PiperVoice
import numpy as np
import soundfile as sf
import io
import logging
from typing import Optional

# --- Config ---
# Modèles Piper pour le français (à télécharger via `piper download fr_FEMALE`)
MODEL_PATHS = {
    "fr_FEMALE": "/app/models/piper/fr_FEMALE.onnx",
    "fr_MALE": "/app/models/piper/fr_MALE.onnx",
}

# Charger les modèles au démarrage
voices = {}
for voice_name, model_path in MODEL_PATHS.items():
    try:
        voices[voice_name] = PiperVoice.load(model_path)
        logging.info(f"Modèle Piper TTS ({voice_name}) chargé avec succès.")
    except Exception as e:
        logging.error(f"Erreur lors du chargement du modèle Piper ({voice_name}): {e}")
        voices[voice_name] = None

# --- Fonctions ---
async def generate_tts(
    text: str,
    voice: str = "fr_FEMALE",
    speed: float = 1.0,
    pitch: float = 1.0,
) -> bytes:
    """
    Génère un audio à partir de texte en utilisant Piper TTS.
    
    Args:
        text: Texte à convertir en audio.
        voice: Voix à utiliser ('fr_FEMALE' ou 'fr_MALE').
        speed: Vitesse de lecture (1.0 = normale).
        pitch: Tonalité (1.0 = normale).
    
    Returns:
        bytes: Audio généré (WAV, 16kHz, 16-bit PCM).
    """
    if voice not in voices or voices[voice] is None:
        raise RuntimeError(f"Modèle Piper TTS ({voice}) non disponible.")
    
    # Générer l'audio avec Piper
    audio_data = voices[voice].synthesize(text)
    
    # Appliquer vitesse et tonalité (simplifié ici, à améliorer)
    # Note: Piper ne supporte pas directement speed/pitch, donc on utilise soundfile pour ajuster
    audio_array = np.frombuffer(audio_data, dtype=np.float32)
    
    # Ajuster la vitesse (résampling simplifié)
    if speed != 1.0:
        audio_array = np.interp(
            np.linspace(0, len(audio_array) - 1, num=int(len(audio_array) / speed)),
            np.arange(len(audio_array)),
            audio_array,
        )
    
    # Convertir en bytes (WAV 16kHz, 16-bit PCM)
    buffer = io.BytesIO()
    sf.write(
        buffer,
        audio_array,
        samplerate=16000,
        format="WAV",
        subtype="PCM_16",
    )
    buffer.seek(0)
    
    return buffer.read()

# --- Test ---
if __name__ == "__main__":
    import asyncio
    
    async def test():
        audio = await generate_tts("Bonjour, comment ça va ?", voice="fr_FEMALE")
        with open("test_tts.wav", "wb") as f:
            f.write(audio)
        print("Audio TTS généré et sauvegardé dans test_tts.wav")
    
    asyncio.run(test())
