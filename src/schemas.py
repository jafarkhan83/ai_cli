from pydantic import BaseModel, Field
from typing import List

json_schema = {
    "type": "object",
    "properties" : {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "content": {"type": "string"},
        "metadata": {
            "type": "object",
            "properties": {
                "input_user_tokens": {"type": "integer"},
                "input_system_tokens": {"type": "integer"},
                "output_tokens": {"type": "integer"},
                "total_tokens": {"type": "integer"},
                "chat_history": {
                    "type": "array", 
                    "items": {"type": "object",
                                "properties": {
                                    "user_asked": {"type": "string"},
                                    "answer": {"type": "string"}
                                    },
                                    "required": ["user_asked", "answer"]
                                }}
            },
            "required": ["input_user_tokens", "input_system_tokens", "output_tokens", "total_tokens", "chat_history"]
        }
    },
    "required": ["title", "description", "content", "metadata"]
}

class ChatHistory(BaseModel):
    user_asked: str
    short_answer: str

class Metadata(BaseModel):
    input_user_tokens: int
    input_system_tokens: int
    output_tokens: int
    total_tokens: int
    chat_history: List[ChatHistory]

class ResponseSchema(BaseModel):
    answer: str
    short_answer: str
    metadata: Metadata
