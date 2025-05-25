// lib/middle_layer/smart_tag_orchestrator.dart

import '../services/semantic_service.dart';
import '../middle_layer/tagging_engine.dart';

class SmartTagOrchestrator {
  static const double _semanticScoreThreshold = 0.78;

  /// Returns structured tags from semantic → NLI → rule fallback
  static Future<List<Map<String, dynamic>>> getSmartTags(String inputText) async {
    final List<Map<String, dynamic>> results = [];

    // 1️⃣ Try semantic tagging via backend API
    final semanticMatches = await SemanticService.getTagsFromText(inputText);

    for (final tag in semanticMatches) {
      final score = tag['score'] ?? 0.0;
      final isConfident = score >= _semanticScoreThreshold;

      results.add({
        'tag': tag['tag'],
        'score': score,
        'category': tag['category'],
        'origin': 'semantic',
        'isTentative': !isConfident,
      });
    }

    if (results.any((t) => t['isTentative'] == false)) {
      return results;
    }

    // 2️⃣ If nothing confident, fall back to rule-based keyword matching
    final TaggingEngine fallbackEngine = TaggingEngine();
    await fallbackEngine.loadRules();
    final fallbackTags = fallbackEngine.detectTags(inputText);

    fallbackTags.forEach((category, tag) {
      results.add({
        'tag': tag,
        'score': 0.5,
        'category': category,
        'origin': 'rule',
        'isTentative': true,
      });
    });

    return results;
  }
}
