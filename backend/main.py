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
        # Get or create thread
        if request.thread_id:
            thread = agent_manager.get_or_create_thread(request.thread_id)
        else:
            thread = agent_manager.get_or_create_thread()
        
        # Get agent (you can hardcode or store agent_id in env)
        agent_id = os.getenv("AGENT_ID")
        agent = agent_manager.get_or_create_agent(agent_id)

        # Process message
        response_text = agent_manager.send_message_and_run(
            thread_id=thread.id,
            agent_id=agent["id"] if isinstance(agent, dict) else agent.id,
            user_message=request.message
        )

        return ChatResponse(
            response=response_text,
            thread_id=thread.id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}