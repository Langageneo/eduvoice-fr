// EduVoice FR™ - Sous-titres
// Fichier: frontend/lib/widgets/subtitles.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class Subtitles extends StatelessWidget {
  const Subtitles({super.key});

  @override
  Widget build(BuildContext context) {
    final settings = Provider.of<Settings>(context);
    
    // Exemple de sous-titres (à connecter au backend)
    final List<Map<String, String>> subtitles = [
      {'en': 'Hello, how are you?', 'fr': 'Bonjour, comment ça va ?'},
      {'en': 'Today we will learn about Flutter.', 'fr': 'Aujourd\'hui, nous allons apprendre Flutter.'},
    ];

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Sous-titres:',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            // Affichage des sous-titres
            ...subtitles.map((sub) => Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  sub['en']!,
                  style: const TextStyle(color: Colors.blue),
                ),
                Text(
                  sub['fr']!,
                  style: const TextStyle(color: Colors.green),
                ),
                const Divider(),
              ],
            )).toList(),
            // Boutons pour basculer entre les langues
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                FilterChip(
                  label: const Text('EN'),
                  selected: true, // Toujours afficher l'anglais
                  onSelected: (bool selected) {},
                ),
                const SizedBox(width: 8),
                FilterChip(
                  label: const Text('FR'),
                  selected: true, // Toujours afficher le français
                  onSelected: (bool selected) {},
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
