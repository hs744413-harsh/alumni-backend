from google import genai
import os


def generate_career_advice(category, skills, mentors):

    api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    mentor_text = ""

    for mentor in mentors[:3]:
        mentor_text += f"{mentor['name']} at {mentor['company']} with skills {mentor['skills']}\n"

    prompt = f"""
You are an AI career advisor.

Resume category: {category}

Detected skills: {skills}

Recommended alumni mentors:
{mentor_text}

Provide:

1. Suitable career roles
2. Skills the student should learn next
3. How alumni mentors can help
4. Short motivational advice
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text