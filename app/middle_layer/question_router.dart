class QuestionRouter {
  /// Returns a list of follow-up question IDs based on user tags
  /// These IDs map to real question text in your frontend logic
  static List<String> getFollowUpQuestions({
    required List<String> tags,
    int maxQuestions = 3,
  }) {
    final Set<String> questions = {};

    final hasTag = (String tag) => tags.contains(tag);

    // 🧠 Life Stage Branching
    if (hasTag("Beginner")) {
      if (hasTag("Curious")) {
        questions.add("Q4"); // Cash flow behavior
        questions.add("Q6"); // ₹1000 prompt
      } else if (hasTag("Lost")) {
        questions.add("Q4");
        questions.add("Q7"); // Goal
        questions.add("Q5"); // EMI
      } else {
        questions.add("Q4");
        questions.add("Q6");
      }
    } else if (hasTag("Emerging-Earner")) {
      questions.add("Q4");
      questions.add("Q5");
      questions.add("Q7");
    } else if (hasTag("Stable-Earner")) {
      questions.add("Q6");
      questions.add("Q7");
    } else if (hasTag("Pause-Mode")) {
      questions.add("Q5");
      questions.add("Q7");
      questions.add("Q4");
    }

    // 💳 Behavioral wildcards
    if (hasTag("Impulsive-Spender")) {
      questions.add("W1"); // Emotional spending probe
    }

    if (hasTag("Debt-Active")) {
      questions.add("W2"); // Debt affecting choices
    }

    if (hasTag("Saver")) {
      questions.add("W3"); // Budget vs Flow
    }

    return questions.take(maxQuestions).toList();
  }
}