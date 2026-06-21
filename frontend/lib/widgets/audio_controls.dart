// EduVoice FR™ - Contrôles Audio
// Fichier: frontend/lib/widgets/audio_controls.dart

import 'package:flutter/material.dart';

class AudioControls extends StatelessWidget {
  final bool isPlaying;
  final double volume;
  final VoidCallback onPlayPause;
  final ValueChanged<double> onVolumeChange;

  const AudioControls({
    super.key,
    required this.isPlaying,
    required this.volume,
    required this.onPlayPause,
    required this.onVolumeChange,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            // Bouton Play/Pause
            IconButton(
              icon: Icon(isPlaying ? Icons.pause : Icons.play_arrow),
              iconSize: 48,
              onPressed: onPlayPause,
            ),
            const SizedBox(height: 16),
            
            // Curseur de volume
            Row(
              children: [
                const Icon(Icons.volume_down),
                Expanded(
                  child: Slider(
                    value: volume,
                    min: 0.0,
                    max: 1.0,
                    onChanged: onVolumeChange,
                  ),
                ),
                const Icon(Icons.volume_up),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
