from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3.6-27b"
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
    return llm.stream(response)