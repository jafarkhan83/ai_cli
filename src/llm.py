from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage
from langchain.agents import create_agent
from dotenv import load_dotenv
from schemas import ResponseSchema
from utilities import get_whether

load_dotenv()
store = {}

llm = ChatGroq(
    model="openai/gpt-oss-safeguard-20b",
    max_tokens=4096,
    )

agent = create_agent(
    model=llm,
    tools=[get_whether],
    system_prompt="you are a helpful assistant. Questions apart from tools must be answered by yourself."
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

def update_chat_history(query, answer, session_id):
    history = get_session(session_id)
    history.add_user_message(query)
    history.add_ai_message(answer)

def get_structured_response(response):
    response_agent = create_agent(
    model=llm,
    response_format=ResponseSchema,
    system_prompt="Your task is to convert the given list object to a structured response as given response format.\nAlso generate a short answer in range 150-200 characters for short_answer field.\nThe metadata field must be field by the metada provide in the list object."
    )

    result = response_agent.invoke({"messages": response['messages']})
    return result['structured_response']

def get_response(query):
    session_id = "session_1"
    messages = create_messages(query, session_id)

    try:
        response = agent.invoke({"messages": messages})
    except Exception as e:
        raise e

    structured_response = get_structured_response(response)
    update_chat_history(query, structured_response.short_answer, session_id)

    return structured_response
