// EduVoice FR™ - Capture Audio Android (Kotlin)
// Fichier: mobile/android/app/src/main/java/com/eduvoice/fr/AudioCaptureService.kt

package com.eduvoice.fr

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import android.os.Build
import android.os.IBinder
import android.util.Log
import androidx.annotation.RequiresApi
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import java.util.concurrent.TimeUnit

class AudioCaptureService : Service() {
    
    private val TAG = "AudioCaptureService"
    private val SAMPLE_RATE = 16000 // 16kHz pour Faster-Whisper
    private val CHANNEL_CONFIG = AudioFormat.CHANNEL_IN_MONO
    private val AUDIO_FORMAT = AudioFormat.ENCODING_PCM_16BIT
    private val BUFFER_SIZE = AudioRecord.getMinBufferSize(SAMPLE_RATE, CHANNEL_CONFIG, AUDIO_FORMAT)
    
    private var audioRecord: AudioRecord? = null
    private var isRecording = false
    private var webSocket: WebSocket? = null
    private val scope = CoroutineScope(Dispatchers.IO)
    private var captureJob: Job? = null
    
    // WebSocket Client
    private val client = OkHttpClient.Builder()
        .readTimeout(0, TimeUnit.MILLISECONDS)
        .build()
    
    private val backendUrl = "ws://10.0.2.2:8000/ws/audio" // À adapter (localhost pour émulateur)
    
    override fun onBind(intent: Intent?): IBinder? = null
    
    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        startForeground(1, createNotification())
    }
    
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == "START") {
            startCapture()
        } else if (intent?.action == "STOP") {
            stopCapture()
        }
        return START_STICKY
    }
    
    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                "audio_capture_channel",
                "Audio Capture",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }
    }
    
    private fun createNotification(): Notification {
        return Notification.Builder(this, "audio_capture_channel")
            .setContentTitle("EduVoice FR™")
            .setContentText("Capture audio en cours...")
            .setSmallIcon(android.R.drawable.ic_media_play)
            .build()
    }
    
    private fun startCapture() {
        if (isRecording) return
        
        try {
            audioRecord = AudioRecord(
                MediaRecorder.AudioSource.MIC, // ou VOICE_CALL pour capturer l'audio système
                SAMPLE_RATE,
                CHANNEL_CONFIG,
                AUDIO_FORMAT,
                BUFFER_SIZE
            )
            
            audioRecord?.startRecording()
            isRecording = true
            
            // Connexion WebSocket
            connectWebSocket()
            
            // Lancer la capture audio
            captureJob = scope.launch {
                val buffer = ByteArray(BUFFER_SIZE)
                while (isRecording) {
                    val bytesRead = audioRecord?.read(buffer, 0, BUFFER_SIZE) ?: 0
                    if (bytesRead > 0) {
                        // Envoyer les données audio au backend
                        webSocket?.send(ByteString.of(*buffer.copyOf(bytesRead)).toByteArray())
                    }
                }
            }
            
            Log.d(TAG, "Capture audio démarrée")
            
        } catch (e: Exception) {
            Log.e(TAG, "Erreur lors du démarrage de la capture audio", e)
            stopCapture()
        }
    }
    
    private fun connectWebSocket() {
        val request = Request.Builder()
            .url(backendUrl)
            .build()
        
        webSocket = client.newWebSocket(request, object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: okhttp3.Response) {
                Log.d(TAG, "Connecté au backend WebSocket")
            }
            
            override fun onMessage(webSocket: WebSocket, bytes: okio.ByteString) {
                // Recevoir l'audio traduit et le jouer
                // TODO: Utiliser AudioTrack pour jouer l'audio
            }
            
            override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                Log.d(TAG, "WebSocket fermé: $reason")
            }
            
            override fun onFailure(webSocket: WebSocket, t: Throwable, response: okhttp3.Response?) {
                Log.e(TAG, "Erreur WebSocket", t)
            }
        })
    }
    
    private fun stopCapture() {
        isRecording = false
        captureJob?.cancel()
        audioRecord?.stop()
        audioRecord?.release()
        audioRecord = null
        webSocket?.close(1000, "Arrêt de la capture")
        webSocket = null
        
        Log.d(TAG, "Capture audio arrêtée")
    }
    
    override fun onDestroy() {
        super.onDestroy()
        stopCapture()
        scope.cancel()
    }
}
