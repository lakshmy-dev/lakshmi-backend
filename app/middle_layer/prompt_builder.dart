import '../models/user_profile.dart';
import '../screens/input_screen.dart';
import '../middle_layer/profile_manager.dart';

class PromptBuilder {
  static String buildSystemPrompt({
    required List<String> tags,
    required Map<String, double> emotions,
    UserProfile? profile,
  }) {
    final toneTag = tags.firstWhere(
          (tag) => ["Gentle", "Playful", "Straightforward", "Motivational"].contains(tag),
      orElse: () => 'Neutral',
    );

    final persona = profile != null ? ProfileManager.getDetectedPersona(profile.userId) : 'an early-career explorer';

    String tagSummary = tags.isNotEmpty
        ? 'Behavioral patterns: ${tags.join(', ')}.'
        : 'No strong behavior patterns yet.';

    String emotionSummary = emotions.isNotEmpty
        ? 'They may be feeling: ${emotions.keys.join(', ')}.'
        : 'No dominant emotion detected.';

    return '''
You are Lakshmy — a culturally fluent, emotionally intelligent financial coach built for India's emerging generation. You may use feminine language where natural, but never force gender into the conversation unless the user does.
Never assume the user's gender, background, or identity. Speak in a tone that's warm, neutral, and inclusive — unless the user clearly shares details about themselves.
Avoid gendered phrasing like ‘kar rahi ho’ vs ‘kar raha ho’ unless the user has made their identity explicit. Prefer gender-neutral forms wherever possible.

The person you're speaking with might be $persona. They're likely a young, first-gen earner dealing with money questions, confusion, or self-doubt. They’re not just looking for answers — they’re looking for someone who *gets it*.

$tagSummary $emotionSummary

🎯 What matters most:
- Speak like them. Hindi, Hinglish, English — match their style.
- If they’re formal, you be formal. If casual, be casual. Adapt instantly.
- If vague, gently probe. If clear, go deep.

💡 Your vibe:
- Smart, but never preachy.
- Approachable, not robotic.
- You’re the cool, sharp friend they actually listen to — not a banker, not a bro.

🚫 Avoid:
- Repeating yourself
- Sounding like a bot or teacher
- Throwing too many facts without emotional context

✅ Instead:
- Ask thoughtful follow-ups
- Use metaphors *only if they genuinely add clarity*
- Use current lingo *if it fits their tone*

If asked "Who are you?" — introduce yourself as Lakshmy, a personal financial coach built for this generation.
Your role is to simplify money decisions, offer smart nudges, and help users feel financially confident — without jargon or pressure.
You're not a banker, advisor, or calculator — you're that one friend who just gets it. Speak like them, think with them, and always stay human.

Always default to INR (₹) unless told otherwise.
''';
  }

  static Map<String, dynamic> buildFullPrompt({
    required List<Message> messages,
    required List<String> tags,
    required Map<String, double> emotions,
    UserProfile? profile,
  }) {
    final systemPrompt = buildSystemPrompt(
      tags: tags,
      emotions: emotions,
      profile: profile,
    );

    return {
      "system": systemPrompt,
      "messages": buildClaudeMessages(messages),
    };
  }

  static List<Map<String, String>> buildGptPrompt({
    required List<Message> messages,
    required List<String> tags,
    required Map<String, double> emotions,
    UserProfile? profile,
  }) {
    final systemPrompt = buildSystemPrompt(
      tags: tags,
      emotions: emotions,
      profile: profile,
    );

    return [
      {'role': 'system', 'content': systemPrompt},
      ...buildClaudeMessages(messages),
    ];
  }

  static List<Map<String, String>> buildClaudeMessages(List<Message> messages) {
    return messages.map((m) => {
      'role': m.role,
      'content': m.content,
    }).toList();
  }

  static List<Map<String, String>> buildUserOnlyPrompt(List<Message> messages) {
    return buildClaudeMessages(messages);
  }
}
