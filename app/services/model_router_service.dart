// lib/services/model_router_service.dart

import 'gpt_service.dart';
import '../screens/input_screen.dart';
import '../middle_layer/emotion_detector.dart';
import '../middle_layer/profile_manager.dart';
import '../middle_layer/smart_tag_orchestrator.dart';

class ModelRouterService {
  static Future<Map<String, dynamic>> getResponse({
    required List<Message> messages,
    required String userId,
  }) async {
    final userInput = messages.last.content.trim();
    final EmotionDetector emotionDetector = EmotionDetector();
    await emotionDetector.loadRules();

    // 🧠 Run smart tag engine
    final List<Map<String, dynamic>> smartTags = await SmartTagOrchestrator.getSmartTags(userInput);
    final List<String> finalTagStrings = smartTags.map((t) => t['tag'].toString()).toList();

    // 🎭 Run emotion detection
    final Map<String, double> detectedEmotions = emotionDetector.detectEmotions(userInput);

    // 🧾 Update profile
    ProfileManager.updateScoredTags(userId, smartTags, source: 'chat');
    ProfileManager.updateEmotionalScores(userId, detectedEmotions);

    // 🤖 Call GPT model with full context
    try {
      final response = await GPTService.askGPT(
        messages,
        detectedTags: finalTagStrings,
        detectedEmotions: detectedEmotions,
        userId: userId,
        includeSystemPrompt: true,
      );

      return {
        'model': 'gpt',
        'systemPromptIncluded': true,
        'response': response,
      };
    } catch (e) {
      print('❌ Error in GPT call: $e');
      return {
        'model': 'gpt',
        'systemPromptIncluded': true,
        'response': 'Something went wrong while processing your request.',
      };
    }
  }
}
