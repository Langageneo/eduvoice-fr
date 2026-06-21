# EduVoice FR™ - Speech-to-Text (Faster-Whisper)
# Fichier: backend/app/models/stt.py

import numpy as np
from faster_whisper import WhisperModel
import logging
from typing import Optional

# --- Config ---
MODEL_SIZE = "base.en"  # Modèle optimisé pour l'anglais
DEVICE = "cpu"  # ou "cuda" si GPU disponible

# --- Charger le modèle ---
try:
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type="int8")
    logging.info(f"Modèle Faster-Whisper ({MODEL_SIZE}) chargé avec succès.")
except Exception as e:
    logging.error(f"Erreur lors du chargement du modèle Faster-Whisper: {e}")
    model = None

# --- Fonctions ---
async def transcribe_audio(audio_data: bytes, language: str = "en") -> str:
    """
    Transcrit un chunk audio en texte.
    
    Args:
        audio_data: Données audio brutes (16kHz, 16-bit PCM).
        language: Langue de l'audio (toujours 'en' pour ce projet).
    
    Returns:
        str: Texte transcrit.
    """
    if model is None:
        raise RuntimeError("Modèle Faster-Whisper non chargé.")
    
    # Convertir les bytes en numpy array (16kHz, float32)
    audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
    
    # Segmenter l'audio si nécessaire (pour éviter les timeouts)
    segments, _ = model.transcribe(
        audio_array,
        language=language,
        beam_size=5,
        vad_filter=True,
        word_timestamps=False,
    )
    
    # Concatenner tous les segments
    transcription = " ".join(segment.text for segment in segments)
    
    return transcription

# --- Test ---
if __name__ == "__main__":
    import asyncio
    
    async def test():
        # Exemple avec un fichier audio local (à remplacer par des données réelles)
        with open("test_audio.wav", "rb") as f:
            audio_data = f.read()
        
        result = await transcribe_audio(audio_data)
        print(f"Transcription: {result}")
    
    asyncio.run(test())
