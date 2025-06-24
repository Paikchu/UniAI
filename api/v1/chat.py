from fastapi import APIRouter
from models import ChatRequest, ChatResponse
from services import ChatService

router = APIRouter()


@router.post(
    "/chat/completions",
    tags=["Chat"],
    summary="Chat Completion",
    description="Get chat completions from a specified model.",
    response_model=ChatResponse,
)
def chat_completions(request: ChatRequest):
    """Chat completion endpoint"""
    return ChatService.process_chat_request(request)
