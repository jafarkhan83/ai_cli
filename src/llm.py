from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.agents import create_agent
from dotenv import load_dotenv
from schemas import json_schema, Response
from utilities import get_whether

load_dotenv()
store = {}

llm = ChatGroq(
    model="qwen/qwen3.6-27b",
    max_tokens=4096,
    )

agent = create_agent(
    model=llm,
    tools=[get_whether],
    response_format=Response,
    system_prompt="you are a helpful assistant."
)

def create_prompt():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{query}")
        ])
    return prompt

def create_messages(query, session_id):
    history = get_session(session_id)
    messages = history.messages + [
        ("user", query)
    ]
    return messages

def get_session(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def update_chat_history(chat_history, session_id):
    history = get_session(session_id)
    history.add_user_message(chat_history)

def get_response(query):
    session_id = "session_1"
    messages = create_messages(query, session_id)

    response = agent.invoke({"messages": messages})
    current_response = "user: " + query + ", assistant: " + str(response['structured_response'].short_answer)

    update_chat_history(current_response, session_id)

    return response
