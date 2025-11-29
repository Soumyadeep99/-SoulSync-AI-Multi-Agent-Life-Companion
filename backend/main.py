# ==========================
#  SoulSync AI - Backend API
#  Fixed & Windows-friendly
# ==========================

import sys
import os

# Ensure backend folder is added to Python PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Import Agents
from agents.core_orchestrator import CoreOrchestrator
from agents.memory_agent import MemoryAgent

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="SoulSync AI Backend")

# Allow frontend (Vite) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
#   FIXED — Properly initialize orchestrator
# ==========================================

# Core orchestrator instance
orchestrator = CoreOrchestrator()
memory = MemoryAgent()

# Request model for chat
class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"


# ==========================
#     ROUTES
# ==========================

@app.get("/")
def home():
    return {"status": "SoulSync AI Backend Running ✔"}


@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    # Store user message
    memory.add_note(req.user_id, req.message)

    # Orchestrator responds
    result = orchestrator.handle_message(req.user_id, req.message)

    # Store bot response
    memory.add_note(req.user_id, result["reply"])

    return result

@app.get("/memory/{user_id}")
def get_user_memory(user_id: str):
    """
    Returns stored chat history for a given user.
    """
    try:
        return memory.get_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================
#     STARTUP LOG
# ==========================

@app.on_event("startup")
def startup_event():
    print("🔥 SoulSync AI Backend started successfully!")
    print("Ready at: http://localhost:8000")
