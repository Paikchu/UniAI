from fastapi import APIRouter
from app.models import ChatRequest
from app.services import ChatService

router = APIRouter()

@router.post("/chat/completions")
def chat_completions(request: ChatRequest):
    """Chat completion endpoint"""
    return ChatService.process_chat_request(request)