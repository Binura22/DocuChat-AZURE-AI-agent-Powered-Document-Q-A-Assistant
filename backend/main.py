from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from agent_manager import AzureAIAgentManager

load_dotenv()

app = FastAPI(title="CineWave Azure AI Agent API")

# Initialize agent manager (singleton)
agent_manager = AzureAIAgentManager()

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None  # Allow frontend to manage thread

class ChatResponse(BaseModel):
    response: str
    thread_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Send message and get response (returns thread_id and response)
        thread_id, response = agent_manager.send_message_and_run(
            thread_id=request.thread_id,
            user_message=request.message
        )

        return ChatResponse(response=response, thread_id=thread_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}