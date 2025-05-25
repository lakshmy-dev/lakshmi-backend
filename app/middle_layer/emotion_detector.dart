import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class EmotionDetector {
  List<dynamic> emotionRules = [];

  /// Load emotion_rules.json from assets
  Future<void> loadRules() async {
    final String response = await rootBundle.loadString('rules/emotion_rules.json');
    final data = await json.decode(response);
    emotionRules = data;
  }

  /// Normalize input
  String _normalize(String input) => input.toLowerCase().trim();

  /// Check if any keyword matches the input
  bool _matchAny(String input, List<dynamic> keywords) {
    final normalized = _normalize(input);
    return keywords.any((keyword) => normalized.contains(keyword.toLowerCase()));
  }

  /// Detect strongest matching emotion
  Map<String, double> detectEmotions(String userInput) {
    final input = _normalize(userInput);
    final matchedEmotions = <String, double>{};

    for (var rule in emotionRules) {
      final emotion = rule['emotion'];
      final confidence = rule['confidence'] ?? 0.7;
      final keywords = rule['keywords'] ?? [];

      if (_matchAny(input, keywords)) {
        matchedEmotions[emotion] = confidence;
      }
    }

    // Sort by confidence and return the strongest one
    if (matchedEmotions.isNotEmpty) {
      final top = matchedEmotions.entries.toList()
        ..sort((a, b) => b.value.compareTo(a.value));
      return {top.first.key: top.first.value};
    }

    return {};
  }
}
