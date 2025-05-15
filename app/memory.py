# Stores conversation history so the chatbot remembers what was said

conversation_history = []

def add_to_history(role, content):
    conversation_history.append({"role": role, "content": content})

def get_history():
    return conversation_history