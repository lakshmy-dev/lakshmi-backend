import '../models/user_profile.dart';
import '../models/tag_score.dart';

class ProfileManager {
  static final Map<String, UserProfile> _userProfiles = {};

  // Initialize profile
  static UserProfile initializeProfile(String userId) {
    if (!_userProfiles.containsKey(userId)) {
      _userProfiles[userId] = UserProfile(
        userId: userId,
        activeTags: [],
        emotionalScores: {},
      );
    }
    return _userProfiles[userId]!;
  }

  // ✅ Update detected tags with score, weight, and source (basic version)
  static void updateTagScores(String userId, List<String> detectedTags, {String source = 'unknown'}) {
    final profile = initializeProfile(userId);

    for (final tag in detectedTags) {
      final existing = profile.activeTags.where((t) => t.tag == tag).toList();
      if (existing.isNotEmpty) {
        final tagScore = existing.first;
        tagScore.score = (tagScore.score + 0.1).clamp(0.0, 1.0);
        tagScore.weight += 1;
        tagScore.sources.add(source);
      } else {
        profile.activeTags.add(TagScore(
          tag: tag,
          score: 0.1,
          weight: 1,
          sources: {source},
        ));
      }
    }

    profile.lastUpdated = DateTime.now();
  }

  // ✅ Update tag scores from structured semantic input
  static void updateScoredTags(String userId, List<Map<String, dynamic>> tagObjects, {String source = 'semantic'}) {
    final profile = initializeProfile(userId);

    for (final tagMap in tagObjects) {
      final tag = tagMap['tag'];
      final score = (tagMap['score'] ?? 0.1).toDouble();

      final existing = profile.activeTags.where((t) => t.tag == tag).toList();
      if (existing.isNotEmpty) {
        final tagScore = existing.first;
        tagScore.score = (tagScore.score + score).clamp(0.0, 1.0);
        tagScore.weight += 1;
        tagScore.sources.add(source);
      } else {
        profile.activeTags.add(TagScore(
          tag: tag,
          score: score,
          weight: 1,
          sources: {source},
        ));
      }
    }

    profile.lastUpdated = DateTime.now();
  }

  // Update detected emotions
  static void updateEmotionalScores(String userId, Map<String, double> detectedEmotions) {
    final profile = initializeProfile(userId);

    detectedEmotions.forEach((emotion, score) {
      if (profile.emotionalScores.containsKey(emotion)) {
        profile.emotionalScores[emotion] =
            (profile.emotionalScores[emotion]! + score).clamp(0.0, 1.0);
      } else {
        profile.emotionalScores[emotion] = score;
      }
    });

    profile.lastUpdated = DateTime.now();
  }

  // Fetch full user profile
  static UserProfile getUserProfile(String userId) {
    return initializeProfile(userId);
  }

  // Return top tags sorted by score
  static List<String> getTopTags(String userId, {int limit = 5}) {
    final profile = initializeProfile(userId);
    final sorted = profile.activeTags.toList()
      ..sort((a, b) => b.score.compareTo(a.score));
    return sorted.take(limit).map((t) => t.tag).toList();
  }

  // Return dominant emotion
  static String? getDominantEmotion(String userId) {
    final profile = initializeProfile(userId);
    if (profile.emotionalScores.isEmpty) return null;

    return profile.emotionalScores.entries
        .reduce((a, b) => a.value > b.value ? a : b)
        .key;
  }

  // Simple persona matcher (rule-based)
  static String getDetectedPersona(String userId) {
    final profile = initializeProfile(userId);
    final tags = getTopTags(userId);

    if (tags.contains('No Savings') && tags.contains('Fixed Income')) {
      return 'Stuck Spender';
    } else if (tags.contains('Irregular Saver') && tags.contains('Hopeful')) {
      return 'Aspiring Saver';
    } else if (tags.contains('Disciplined Saver') && tags.contains('Goal Setter')) {
      return 'Cautious Climber';
    } else if (tags.contains('Debt Active') && tags.contains('Confused')) {
      return 'Struggling Borrower';
    }

    return 'Default Persona';
  }

  // 🧾 Print user profile to console
  static void debugPrintProfile(String userId) {
    final profile = getUserProfile(userId);
    print('🧾 User Profile for $userId:');
    print('🏷️ Tags:');
    for (final tag in profile.activeTags) {
      print(' - ${tag.tag}: ${tag.score.toStringAsFixed(2)} '
          '(weight: ${tag.weight}, sources: ${tag.sources.join(', ')})');
    }
    print('🎭 Emotions:');
    profile.emotionalScores.forEach((emotion, score) {
      print(' - $emotion: ${score.toStringAsFixed(2)}');
    });
    print('🕒 Last Updated: ${profile.lastUpdated}');
  }

  static UserProfile? getProfile(String userId) {
    return _userProfiles[userId];
  }

  // ✅ Save profile from onboarding responses
  static void setFromOnboarding(String userId, Map<String, dynamic> responses) {
    final profile = initializeProfile(userId);

    profile.language = responses['Q1'];
    profile.name = responses['Q2'];
    profile.lifeStage = responses['Q3'];

    if (responses['Q4'] != null) {
      profile.tagScores['money_flow'] = responses['Q4'];
    }
    if (responses['Q5'] != null) {
      profile.tagScores['debt_load'] = responses['Q5'];
    }
    if (responses['Q6'] != null) {
      profile.tagScores['spender_type'] = responses['Q6'];
    }
    if (responses['Q7'] != null) {
      profile.tagScores['goal_focus'] = responses['Q7'];
    }

    // ✅ New: scored semantic tags
    if (responses['Q7_semantic_structured'] != null) {
      final List<Map<String, dynamic>> structuredTags =
      List<Map<String, dynamic>>.from(responses['Q7_semantic_structured']);
      updateScoredTags(userId, structuredTags, source: 'Q7_structured');
    }

    _userProfiles[userId] = profile;
    print('🧠 UserProfile set from onboarding: ${profile.toJson()}');
  }
}
