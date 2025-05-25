import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class TaggingEngine {
  List<dynamic> rules = [];

  // Load the master_rules.json file at app startup
  Future<void> loadRules() async {
    final String response = await rootBundle.loadString('rules/master_rules.json');
    final data = await json.decode(response);
    rules = data;
  }

  // Match user input to a tag
  String? matchTag(String userInput) {
    String input = userInput.toLowerCase();

    for (var rule in rules) {
      List<dynamic> keywords = rule['keywords'];
      for (var keyword in keywords) {
        if (input.contains(keyword.toLowerCase())) {
          return rule['tag_to_assign'];
        }
      }
    }
    return null; // No match found
  }
}
