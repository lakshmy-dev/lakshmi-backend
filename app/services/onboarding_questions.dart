import '../middle_layer/question_bank.dart';

final List<Map<String, dynamic>> onboardingQuestions = [
  {
    "id": "Q1",
    "type": "choice",
    "question": QuestionBank.getText("Q1"),
    "options": [
      "English",
      "Hinglish (thoda Hindi, thoda English)",
      "Hindi (pure Hindi, no English)"
    ],
  },
  {
    "id": "Q2",
    "type": "text",
    "question": QuestionBank.getText("Q2"),
  },
  {
    "id": "Q3",
    "type": "choice",
    "question": QuestionBank.getText("Q3"),
    "options": [
      "Just starting out",
      "Earning and learning",
      "Earning well, but want to grow",
      "On a break / Figuring it out"
    ],
  },
  {
    "id": "Q4",
    "type": "choice",
    "question": QuestionBank.getText("Q4"),
    "options": [
      "I manage to save a bit",
      "I try, but end up spending",
      "It’s usually all gone",
      "Honestly, I don’t track much"
    ],
  },
  {
    "id": "Q5",
    "type": "choice",
    "question": QuestionBank.getText("Q5"),
    "options": [
      "Yes — loans, EMIs, credit cards, or other repayments",
      "Just the usual bills",
      "Nope, I’m all clear",
      "It’s complicated"
    ],
  },
  {
    "id": "Q6",
    "type": "choice",
    "question": QuestionBank.getText("Q6"),
    "options": [
      "Buy something I’ve been eyeing 👀",
      "Save it for later",
      "Repay someone or something",
      "Hmm... not sure yet"
    ],
  },
  {
    "id": "Q7",
    "question": "What’s one money thing you’d love help with right now?",
    "type": "choice+text",
    "options": [
      "Buying something important",
      "Clearing a loan or payment",
      "Planning a trip or big expense",
      "Just feeling more in control",
      "Other (let me type)"
    ],
  },
];