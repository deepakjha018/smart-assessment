import json
from groq import Groq
from django.conf import settings


def generate_quiz_questions(topic, difficulty, num_questions):
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)

        prompt = f"""
        Generate {num_questions} multiple choice questions on the topic "{topic}"
        with difficulty level "{difficulty}".

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

        Do NOT include explanation.
        Do NOT include markdown formatting.
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

        return questions

    except Exception as e:
        print("GROQ ERROR:", e)
        return None

def generate_explanation(question_text, correct_option, options_dict):
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)

        correct_answer_text = options_dict.get(correct_option)

        prompt = f"""
        Explain why the following answer is correct.

        Question: {question_text}

        Correct Answer: {correct_answer_text}

        Give a clear and educational explanation in 4-5 lines.
        Do NOT return JSON.
        Do NOT use markdown.
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