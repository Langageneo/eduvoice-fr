// EduVoice FR™ - Frontend Flutter
// Fichier: frontend/lib/main.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'screens/home_screen.dart';
import 'screens/history_screen.dart';
import 'screens/settings_screen.dart';
import 'themes/app_theme.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AudioController()),
        ChangeNotifierProvider(create: (_) => TranslationHistory()),
        ChangeNotifierProvider(create: (_) => Settings()),
      ],
      child: const EduVoiceApp(),
    ),
  );
}

class EduVoiceApp extends StatelessWidget {
  const EduVoiceApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EduVoice FR™',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: Provider.of<Settings>(context).themeMode,
      initialRoute: '/',
      routes: {
        '/': (context) => const HomeScreen(),
        '/history': (context) => const HistoryScreen(),
        '/settings': (context) => const SettingsScreen(),
      },
    );
  }
}

// --- Modèles ---
class AudioController with ChangeNotifier {
  IO.Socket? _socket;
  bool _isConnected = false;
  bool _isPlaying = false;
  double _volume = 1.0;
  String _currentSource = "Aucune source";

  IO.Socket? get socket => _socket;
  bool get isConnected => _isConnected;
  bool get isPlaying => _isPlaying;
  double get volume => _volume;
  String get currentSource => _currentSource;

  void connectToBackend(String url) {
    _socket = IO.io(url, <String, dynamic>{
      'transports': ['websocket'],
      'autoConnect': true,
    });
    _socket?.on('connect', (_) {
      _isConnected = true;
      notifyListeners();
    });
    _socket?.on('disconnect', (_) {
      _isConnected = false;
      notifyListeners();
    });
    _socket?.on('audio_chunk', (data) {
      // TODO: Lire le chunk audio reçu
      // Utiliser audioplayers pour jouer l'audio
    });
  }

  void togglePlayPause() {
    _isPlaying = !_isPlaying;
    notifyListeners();
  }

  void setVolume(double volume) {
    _volume = volume;
    notifyListeners();
  }

  void setSource(String source) {
    _currentSource = source;
    notifyListeners();
  }
}

class TranslationHistory with ChangeNotifier {
  final List<Map<String, dynamic>> _history = [];

  List<Map<String, dynamic>> get history => _history;

  void addEntry(String title, String date, String originalText, String translatedText) {
    _history.add({
      'title': title,
      'date': date,
      'original': originalText,
      'translated': translatedText,
    });
    notifyListeners();
  }
}

class Settings with ChangeNotifier {
  ThemeMode _themeMode = ThemeMode.system;
  String _selectedVoice = "fr_FEMALE";
  double _playbackSpeed = 1.0;

  ThemeMode get themeMode => _themeMode;
  String get selectedVoice => _selectedVoice;
  double get playbackSpeed => _playbackSpeed;

  void setThemeMode(ThemeMode mode) {
    _themeMode = mode;
    notifyListeners();
  }

  void setSelectedVoice(String voice) {
    _selectedVoice = voice;
    notifyListeners();
  }

  void setPlaybackSpeed(double speed) {
    _playbackSpeed = speed;
    notifyListeners();
  }
}
