# Simple in-memory chat storage
# (industry note: later replace with Redis)

from collections import defaultdict

chat_memory = defaultdict(list)

def get_history(user_id: str):
    return chat_memory[user_id]

def add_message(user_id: str, role: str, content: str):
    chat_memory[user_id].append({
        "role": role,
        "content": content
    })

def clear_history(user_id: str):
    chat_memory[user_id] = []