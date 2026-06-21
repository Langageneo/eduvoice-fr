// EduVoice FR™ - Écran Principal
// Fichier: frontend/lib/screens/home_screen.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../widgets/audio_controls.dart';
import '../widgets/source_selector.dart';
import '../widgets/subtitles.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final audioController = Provider.of<AudioController>(context);
    final settings = Provider.of<Settings>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('EduVoice FR™'),
        actions: [
          IconButton(
            icon: const Icon(Icons.history),
            onPressed: () => Navigator.pushNamed(context, '/history'),
          ),
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () => Navigator.pushNamed(context, '/settings'),
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Sélecteur de source
              const SourceSelector(),
              const SizedBox(height: 20),
              
              // Contrôles audio
              AudioControls(
                isPlaying: audioController.isPlaying,
                volume: audioController.volume,
                onPlayPause: audioController.togglePlayPause,
                onVolumeChange: audioController.setVolume,
              ),
              const SizedBox(height: 20),
              
              // Affichage des sous-titres
              const Subtitles(),
              const SizedBox(height: 20),
              
              // Statut de connexion
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Row(
                    children: [
                      Icon(
                        audioController.isConnected ? Icons.check_circle : Icons.error,
                        color: audioController.isConnected ? Colors.green : Colors.red,
                      ),
                      const SizedBox(width: 10),
                      Text(
                        audioController.isConnected
                            ? 'Connecté au backend'
                            : 'Déconnecté',
                        style: Theme.of(context).textTheme.bodyLarge,
                      ),
                    ],
                  ),
                ),
              ),
              
              // Source actuelle
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Row(
                    children: [
                      const Icon(Icons.source),
                      const SizedBox(width: 10),
                      Text(
                        'Source: ${audioController.currentSource}',
                        style: Theme.of(context).textTheme.bodyLarge,
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
