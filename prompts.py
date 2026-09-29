EDUCATION_SYSTEM = """
You are EduGenie, a careful educational assistant.
Explain concepts accurately, use simple language appropriate to the requested level,
avoid pretending to know uncertain facts, and structure answers for learning.
When useful, include examples, a short recap, and one practical study tip.
"""

QA_PROMPT = """
Answer this student's question.

Student level: {level}
Question: {question}

Return:
1. Direct answer
2. Short explanation
3. Example (if useful)
4. One-line takeaway
"""

EXPLAIN_PROMPT = """
Explain the following concept to a {level} learner.

Topic: {topic}

Use very simple language. Start with the core idea, then explain step-by-step,
give one everyday analogy or example, and finish with a 2-line recap.
"""

SUMMARY_PROMPT = """
Summarize the following educational text for a {level} learner.

Keep the essential facts and relationships. Remove repetition.
Use a short title, 5-8 bullet points, and a final "In short" sentence.

TEXT:
{text}
"""

QUIZ_PROMPT = """
Create exactly 3 multiple-choice questions from the passage below.

Student level: {level}

Return ONLY valid JSON matching this shape:
{{
  "questions": [
    {{
      "question": "string",
      "options": ["A", "B", "C", "D"],
      "answer": "A",
      "explanation": "short explanation"
    }}
  ]
}}

Rules:
- Exactly 3 questions.
- Exactly 4 options per question.
- "answer" must be exactly one of the option strings.
- Questions must be answerable from the passage.
- Avoid trick questions.

PASSAGE:
{text}
"""

LEARNING_PATH_PROMPT = """
Create a personalized learning path for the topic below.

Topic: {topic}
Learner level: {level}
Available time: {hours_per_week} hours/week

Return:
- Goal
- Prerequisites
- Beginner stage
- Intermediate stage
- Advanced stage
- A practical weekly schedule
- 5 project/practice ideas
- Useful resource types (videos, articles, books, documentation)
- A simple progress checklist

Keep it realistic and actionable.
"""
