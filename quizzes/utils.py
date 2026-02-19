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
