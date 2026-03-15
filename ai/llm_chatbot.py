import os
from dotenv import load_dotenv
from google import genai
from ai.mentor_recommender import recommend_mentors
from ai.alumni_search import search_alumni
from ai.memory_store import get_history, add_message
from ai.vector_search import search_alumni as vector_search_alumni


load_dotenv()

SYSTEM_PROMPT = """
You are AlumniSphere AI Assistant.

You help users find alumni mentors, jobs, and networking opportunities.

If alumni database results are provided, always use them in your answer.

When mentors are available, list them clearly.
"""

def ask_llm(user_query: str, user_id: str = "default"):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "AI service not configured. Please contact admin."

    try:
        client = genai.Client(api_key=api_key)

        # ✅ get previous conversation
        history = get_history(user_id)

        # 🔎 Search alumni database
        alumni_results = search_alumni(user_query)

        # 🔎 AI semantic search (vector search)
        vector_results = vector_search_alumni(user_query)
        vector_context = ""

        if vector_results:
            vector_context = "\nRelevant alumni from AI semantic search:\n"

            for alum in vector_results:
                vector_context += f"{alum}\n"

        extra_context = ""

        if alumni_results:
            extra_context = "Alumni found in database:\n"

            for alum in alumni_results:
                extra_context += (
                    f"{alum['name']} works at {alum['company']} "
                    f"with skills {alum['skills']} "
                    f"(Batch {alum['batch']})\n"
                )
        # 🔎 Recommend mentors
        mentor_results = recommend_mentors(user_query)
        mentor_context = ""

        if mentor_results:
            mentor_context = "\nRecommended mentors:\n"

            for mentor in mentor_results:
                mentor_context += (
                    f"{mentor['name']} works at {mentor['company']} "
                    f"with skills {mentor['skills']}\n"
                    )

        # 🧠 build conversation context
        conversation_text = SYSTEM_PROMPT + "\n" + extra_context + "\n" + vector_context + "\n" + mentor_context + "\nConversation history:\n"

        for msg in history[-6:]:
            conversation_text += f"{msg['role']}: {msg['content']}\n"

        conversation_text += f"User: {user_query}"

        # 🤖 Gemini call
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conversation_text,
        )

        answer = response.text

        # ✅ store conversation memory
        add_message(user_id, "User", user_query)
        add_message(user_id, "Assistant", answer)

        return answer

    except Exception as e:
        return f"AI temporarily unavailable: {str(e)}"