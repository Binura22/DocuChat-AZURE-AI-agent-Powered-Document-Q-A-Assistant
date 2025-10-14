from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from agent_manager import AzureAIAgentManager

load_dotenv()

app = FastAPI(title="DocuChat Azure AI Agent API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent manager (singleton)
agent_manager = AzureAIAgentManager()

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    thread_id: str

class UploadResponse(BaseModel):
    message: str
    filename: str
    thread_id: str

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload a text file and create a new conversation thread"""
    try:
        # Validate file type
        if not file.filename.endswith('.txt'):
            raise HTTPException(status_code=400, detail="Only .txt files are supported")
        
        # Read file content
        content = await file.read()
        text_content = content.decode('utf-8')
        
        if not text_content.strip():
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Create a new thread with the document content
        thread_id = agent_manager.create_thread_with_document(
            filename=file.filename,
            content=text_content
        )
        
        return UploadResponse(
            message=f"File '{file.filename}' uploaded successfully. You can now ask questions about it!",
            filename=file.filename,
            thread_id=thread_id
        )
    
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be a valid UTF-8 text file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the AI agent about the uploaded document"""
    try:
        if not request.thread_id:
            raise HTTPException(
                status_code=400, 
                detail="Please upload a document first to start a conversation"
            )
        
        # Send message and get response
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