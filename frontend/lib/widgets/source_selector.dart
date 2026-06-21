// EduVoice FR™ - Sélecteur de Source
// Fichier: frontend/lib/widgets/source_selector.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class SourceSelector extends StatelessWidget {
  const SourceSelector({super.key});

  @override
  Widget build(BuildContext context) {
    final audioController = Provider.of<AudioController>(context);
    final List<String> sources = [
      'YouTube',
      'Udemy',
      'Coursera',
      'Twitch',
      'Zoom',
      'Google Meet',
      'Podcast',
      'Fichier Local',
    ];

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Sélectionnez la source audio:',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            DropdownButton<String>(
              value: audioController.currentSource,
              hint: const Text('Choisissez une source'),
              items: sources.map((String source) {
                return DropdownMenuItem<String>(
                  value: source,
                  child: Text(source),
                );
              }).toList(),
              onChanged: (String? newValue) {
                if (newValue != null) {
                  audioController.setSource(newValue);
                  // TODO: Connecter à la source sélectionnée
                }
              },
            ),
          ],
        ),
      ),
    );
  }
}
