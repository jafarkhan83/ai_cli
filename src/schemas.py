from pydantic import BaseModel, Field
from typing import List

class ChatHistory(BaseModel):
    user_asked: str
    short_answer: str

class Metadata(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int
    tool_used: str | None
    chat_history: List[ChatHistory]

class ResponseSchema(BaseModel):
    answer: str
    short_answer: str
    metadata: Metadata
