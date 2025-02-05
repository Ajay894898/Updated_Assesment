from fastapi import APIRouter
from models import ChatRequest
from services import execute_workflow



router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest):
    user_input = request.user_input
    result = execute_workflow(user_input)
    return {"response": result["response"]}
