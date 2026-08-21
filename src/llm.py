from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from dotenv import load_dotenv
from schemas import json_schema

load_dotenv()
store = {}

llm = ChatGroq(
    model="qwen/qwen3.6-27b",
    max_tokens=4096,
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

def create_prompt():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{query}")
        ])
    return prompt

def get_session(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def get_response(query):
    prompt = create_prompt()
    chain = prompt | llm

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session,
        input_messages_key="query",
        history_messages_key="history"
    )

    return chain_with_history.invoke(
        {"query": query},
        config={"configurable" : {"session_id" : "session_1"}})