from fastapi import APIRouter
from ai.llm_chatbot import ask_llm

router: APIRouter = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
def chat(query: dict):
    message = query.get("message")
    user_id = query.get("user_id", "default")

    answer = ask_llm(message, user_id=user_id)

    return {"response": answer}