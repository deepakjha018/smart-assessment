import json
from groq import Groq
from django.conf import settings


def generate_quiz_questions(topic, difficulty, num_questions):
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)

        prompt = f"""
        Generate {num_questions} multiple choice questions on the topic "{topic}"
        with difficulty level "{difficulty}".

        STRICT RULES:
        1. Each question must have exactly 4 options labeled A, B, C, and D.
        2. The correct_answer must ALWAYS be the LETTER (A, B, C, or D).
        3. Never return the full answer text in correct_answer.
        4. All options must be different.
        5. Questions must be factually correct.

        Return ONLY valid JSON in this format:

        [
            {{
                "question": "Question text",
                "options": {{
                    "A": "Option A",
                    "B": "Option B",
                    "C": "Option C",
                    "D": "Option D"
                }},
                "correct_answer": "A"
            }}
        ]

        Do NOT include explanations.
        Do NOT include markdown.
        Do NOT include anything outside JSON.
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a quiz generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()

        # Remove accidental markdown
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        questions = json.loads(content)

        validated_questions = []

        for q in questions:
            options = q.get("options", {})
            correct = q.get("correct_answer")

            # Ensure correct answer is A/B/C/D
            if correct not in ["A", "B", "C", "D"]:
                for key, value in options.items():
                    if value.strip().lower() == str(correct).strip().lower():
                        correct = key
                        break

            q["correct_answer"] = correct
            validated_questions.append(q)

        return validated_questions
    
    except Exception as e:
        print("GROQ ERROR:", e)
        return None

def generate_explanation(question_text, correct_option, options_dict):
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)

        correct_answer_text = correct_option

        prompt = f"""
        You are explaining a multiple choice quiz question.

        Question:
        {question_text}

        Options:
        A: {options_dict['A']}
        B: {options_dict['B']}
        C: {options_dict['C']}
        D: {options_dict['D']}

        The correct option is already determined.

        Correct Option Text:
        {correct_answer_text}

        IMPORTANT RULES:
        - Assume the provided option is correct.
        - Do NOT question or verify the correctness.
        - Do NOT say the answer is missing.
        - Do NOT say the options are incorrect.
        - Do NOT solve the question again.

        Simply explain WHY the provided correct option makes sense in 2–3 sentences.
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful educational assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        explanation = response.choices[0].message.content.strip()
        return explanation

    except Exception as e:
        print("GROQ EXPLANATION ERROR:", e)
        return "Explanation could not be generated at this time."