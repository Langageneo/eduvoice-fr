// EduVoice FR™ - Historique des Traductions
// Fichier: frontend/lib/screens/history_screen.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final history = Provider.of<TranslationHistory>(context).history;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Historique'),
      ),
      body: history.isEmpty
          ? const Center(
              child: Text(
                'Aucune traduction enregistrée.',
                style: TextStyle(fontSize: 18),
              ),
            )
          : ListView.builder(
              itemCount: history.length,
              itemBuilder: (context, index) {
                final entry = history[index];
                return Card(
                  child: ListTile(
                    title: Text(entry['title']),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Date: ${entry['date']}'),
                        const SizedBox(height: 8),
                        Text('Original: ${entry['original']}'),
                        Text('Traduction: ${entry['translated']}'),
                      ],
                    ),
                    trailing: IconButton(
                      icon: const Icon(Icons.share),
                      onPressed: () {
                        // TODO: Partager ou exporter l'entrée
                      },
                    ),
                  ),
                );
              },
            ),
    );
  }
}
