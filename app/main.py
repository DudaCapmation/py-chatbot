# FastAPI backend

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

from app.memory import add_to_history, get_history
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# To allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")

async def chat (request: Request):
    data = await request.json()
    user_input = data.get("message")
    add_to_history("user", user_input)

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = get_history()
    )

    assistant_reply = response.choices[0].message.content
    add_to_history("assistant", assistant_reply)

    return {"reply": assistant_reply}