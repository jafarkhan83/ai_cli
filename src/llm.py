from langchain_groq import ChatGroq
from dotenv import load_dotenv
from schemas import json_schema

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3.6-27b",
    model_kwargs= {
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "Response",
                "schema": json_schema
            }
        }
    }
    )

def create_response(prompt):
    messages = [
        (
            "system",
            "You are a helpful assistant."
        ),
        (
            "user", prompt
        )
    ]
    return messages

def get_response(prompt):
    response = create_response(prompt)
    return llm.invoke(response)