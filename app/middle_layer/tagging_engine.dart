import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class TaggingEngine {
  List<dynamic> rules = [];

  /// Load the master_rules.json file at app startup
  Future<void> loadRules() async {
    final String response = await rootBundle.loadString('rules/master_rules.json');
    final data = await json.decode(response);
    rules = data;
  }

  /// Normalize user input for easier matching
  String _normalize(String input) => input.toLowerCase().trim();

  /// Check if any keyword matches the input
  bool _matchAny(String input, List<dynamic> keywords) {
    final normalized = _normalize(input);
    return keywords.any((keyword) => normalized.contains(keyword.toLowerCase()));
  }

  /// Match input to all applicable tags based on rules
  Map<String, String> detectTags(String userInput) {
    final tags = <String, String>{};
    final input = _normalize(userInput);

    for (var rule in rules) {
      final category = rule['category'];          // e.g., "Income Status"
      final tag = rule['tag_to_assign'];          // e.g., "No Income"
      final keywords = rule['keywords'] ?? [];

      if (_matchAny(input, keywords)) {
        tags[category] = tag;
      }
    }

    return tags;
  }
}
