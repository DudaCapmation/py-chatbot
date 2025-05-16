# FastAPI backend

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.concurrency import run_in_threadpool
from openai import OpenAI
import os
import asyncio
from dotenv import load_dotenv

from app.memory import add_to_history, get_history
from app.auth import register_user, authenticate_user

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

# Endpoints

# Register new user
@app.post("/register")
async def register(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    try:
        register_user(username, password)
        return {"message": "User registered successfully"}
    except HTTPException as e:
        raise e

# Login
@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    if authenticate_user(username, password):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Chat endpoint. Returns a streaming response from OpenAI.
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message")
    add_to_history("user", user_input)

    queue = asyncio.Queue()
    full_response = ""

    def sync_stream():
        nonlocal full_response
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=get_history(),
                stream=True
            )
            for chunk in response:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    content = delta.content
                    full_response += content
                    asyncio.run(queue.put(content))
        finally:
            asyncio.run(queue.put(None))  # Signal end of stream

    # Start streaming in a background thread using run_in_threadpool
    asyncio.create_task(run_in_threadpool(sync_stream))

    async def stream_generator():
        while True:
            chunk = await queue.get()
            if chunk is None:
                break
            yield chunk.encode("utf-8")

        add_to_history("assistant", full_response)

    return StreamingResponse(stream_generator(), media_type="text/plain")