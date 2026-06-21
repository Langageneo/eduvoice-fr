# EduVoice FR™ - Backend FastAPI
# Fichier: backend/app/main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis.asyncio as redis
import asyncio
import logging
from typing import Optional
import os

# --- Config ---
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://user:password@postgres:5432/eduvoice")

# --- Models ---
class AudioChunk(BaseModel):
    audio_data: bytes  # Chunk audio brut (ex: 16kHz, 16-bit PCM)
    source: str = "youtube"  # Source: youtube, udemy, local, etc.
    language: str = "en"  # Toujours 'en' pour ce projet

class TranslationRequest(BaseModel):
    text: str
    context: Optional[str] = None  # Pour conserver le contexte

class TTSRequest(BaseModel):
    text: str
    voice: str = "fr_FEMALE"  # ou 'fr_MALE'
    speed: float = 1.0
    pitch: float = 1.0

# --- FastAPI App ---
app = FastAPI(title="EduVoice FR™ API", version="1.0.0")

# CORS (pour Flutter et Extension Chrome)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Redis Client ---
redis_client = redis.from_url(REDIS_URL)

# --- WebSocket Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# --- WebSocket Endpoint (Streaming Audio) ---
@app.websocket("/ws/audio")
async def websocket_audio(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            audio_chunk = AudioChunk(**data)
            
            # TODO: Intégrer Faster-Whisper ici pour la transcription
            transcription = await transcribe_audio(audio_chunk.audio_data)
            
            # TODO: Traduire avec NLLB-200
            translation = await translate_text(transcription)
            
            # TODO: Synthèse vocale avec Piper/Kokoro
            audio_fr = await generate_tts(translation, voice="fr_FEMALE")
            
            # Envoyer l'audio français au client
            await websocket.send_bytes(audio_fr)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# --- API Endpoints ---
@app.post("/transcribe")
async def transcribe(audio_chunk: AudioChunk):
    """Transcription audio → texte (Faster-Whisper)"""
    # TODO: Implémenter Faster-Whisper
    return {"text": "Transcription en cours..."}

@app.post("/translate")
async def translate(request: TranslationRequest):
    """Traduction EN → FR (NLLB-200)"""
    # Vérifier le cache Redis
    cached = await redis_client.get(request.text)
    if cached:
        return {"translation": cached.decode()}
    
    # TODO: Implémenter NLLB-200
    translation = "Traduction en cours..."
    await redis_client.set(request.text, translation, ex=3600)  # Cache 1h
    return {"translation": translation}

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """Synthèse vocale (Piper/Kokoro)"""
    # TODO: Implémenter Piper TTS
    return {"audio": b"Audio généré..."}

# --- Helper Functions (À implémenter) ---
async def transcribe_audio(audio_data: bytes) -> str:
    """Utilise Faster-Whisper pour transcrire l'audio."""
    # TODO: Intégrer Faster-Whisper
    return "Texte transcrit"

async def translate_text(text: str) -> str:
    """Utilise NLLB-200 pour traduire EN → FR."""
    # TODO: Intégrer NLLB-200
    return "Texte traduit"

async def generate_tts(text: str, voice: str = "fr_FEMALE") -> bytes:
    """Génère l'audio FR avec Piper/Kokoro."""
    # TODO: Intégrer Piper TTS
    return b"Audio TTS"

# --- Health Check ---
@app.get("/health")
async def health_check():
    return {"status": "OK", "redis": await check_redis()}

async def check_redis():
    try:
        await redis_client.ping()
        return "connected"
    except:
        return "disconnected"

# --- Run ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
