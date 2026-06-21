// EduVoice FR™ - Activité Principale (Kotlin)
// Fichier: mobile/android/app/src/main/java/com/eduvoice/fr/MainActivity.kt

package com.eduvoice.fr

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {
    
    private val REQUEST_RECORD_AUDIO_PERMISSION = 200
    private val permissions = arrayOf(
        android.Manifest.permission.RECORD_AUDIO,
        android.Manifest.permission.CAPTURE_AUDIO_OUTPUT,
        android.Manifest.permission.FOREGROUND_SERVICE
    )
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Bouton pour démarrer la capture
        val startButton = findViewById<Button>(R.id.startButton)
        val stopButton = findViewById<Button>(R.id.stopButton)
        
        startButton.setOnClickListener {
            if (checkPermissions()) {
                startAudioCapture()
            } else {
                requestPermissions()
            }
        }
        
        stopButton.setOnClickListener {
            stopAudioCapture()
        }
    }
    
    private fun checkPermissions(): Boolean {
        return permissions.all { 
            ContextCompat.checkSelfPermission(this, it) == android.content.pm.PackageManager.PERMISSION_GRANTED 
        }
    }
    
    private fun requestPermissions() {
        ActivityCompat.requestPermissions(
            this,
            permissions,
            REQUEST_RECORD_AUDIO_PERMISSION
        )
    }
    
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQUEST_RECORD_AUDIO_PERMISSION) {
            if (grantResults.all { it == android.content.pm.PackageManager.PERMISSION_GRANTED }) {
                startAudioCapture()
            } else {
                Toast.makeText(
                    this,
                    "Permissions requises pour la capture audio",
                    Toast.LENGTH_SHORT
                ).show()
            }
        }
    }
    
    private fun startAudioCapture() {
        val intent = Intent(this, AudioCaptureService::class.java).apply {
            action = "START"
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
        Toast.makeText(this, "Capture audio démarrée", Toast.LENGTH_SHORT).show()
    }
    
    private fun stopAudioCapture() {
        val intent = Intent(this, AudioCaptureService::class.java).apply {
            action = "STOP"
        }
        stopService(intent)
        Toast.makeText(this, "Capture audio arrêtée", Toast.LENGTH_SHORT).show()
    }
}
