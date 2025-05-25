class QuestionBank {
  static const Map<String, String> questions = {
    // Fixed Questions
    "Q1": "How do you want me to talk to you?",
    "Q2": "What should I call you?",
    "Q3": "Which of these sounds most like your current vibe?",

    // Dynamic Questions
    "Q4": "After spending on basics such as rent, groceries, bills — what's your money vibe?",
    "Q5": "Are there any payments you’re juggling right now?",
    "Q6": "Imagine I quietly slipped ₹1,000 into your account today. What would you do with it?",
    "Q7": "What’s one money thing you’d love help with right now?",

    // Wildcards
    "W1": "Ever bought something just to feel better?",
    "W2": "Do these payments ever stop you from doing things you really want?",
    "W3": "Do you usually set a budget or just go with the flow?",
  };

  static String? getText(String id) => questions[id];
}
