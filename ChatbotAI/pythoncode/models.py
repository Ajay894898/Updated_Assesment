from pydantic import BaseModel

# Request model
class ChatRequest(BaseModel):
    user_input: str
