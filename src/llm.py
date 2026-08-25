from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage
from langchain.agents import create_agent
from dotenv import load_dotenv
from schemas import ChatHistory, Metadata, ResponseSchema
from utilities import get_whether
import re

load_dotenv()
store = {}

llm = ChatGroq(
    model="openai/gpt-oss-safeguard-20b",
    max_tokens=4096,
    )

agent = create_agent(
    model=llm,
    tools=[get_whether],
    system_prompt = (
    "You are a helpful assistant. Questions apart from tools must be answered by yourself. "
    "At the very end of your response, on a new line, include a short summary in this exact format:\n"
    "[SHORT_ANSWER]your summary here[/SHORT_ANSWER]\n"
    "The short answer must preserve all important words/facts (names, numbers, dates) "
    "so the full answer could be reasonably reconstructed from it, "
    "and must be between 150-200 characters. "
    "Do not include the [SHORT_ANSWER] tags anywhere else in your response."
    )
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

def extract_tool_usage(response):
    for msg in response["messages"]:
        if getattr(msg, 'tool_calls', None):
            return msg.tool_calls[0]["name"]
    return None

def extract_token_usage(response):
    for msg in response["messages"]:
        if isinstance(msg, AIMessage) and getattr(msg, 'usage_metadata', None):
            u = msg.usage_metadata
            return u.get("input_tokens", 0), u.get("output_tokens", 0), u.get("total_tokens", 0)
    return None

def create_metadata(response, session_id):
    tool_call = extract_tool_usage(response)
    input_tokens, output_tokens, total_tokens = extract_token_usage(response)
    history = get_session(session_id)
    chat_history = [
        ChatHistory(user_asked=history.messages[i].content, short_answer=history.messages[i + 1].content)
        for i in range(0, len(history.messages), 2)
    ]
    return Metadata(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        tool_used=tool_call if tool_call else None,
        chat_history=chat_history
    )

SHORT_ANSWER_PATTERN = re.compile(r"\[SHORT_ANSWER\](.*?)\[/SHORT_ANSWER\]", re.DOTALL)

def extract_short_answer(content: str) -> tuple[str, str]:
    """
    Returns (main_answer, short_answer).
    main_answer has the [SHORT_ANSWER] block stripped out.
    short_answer is extracted if present, else derived from the first 3 sentences.
    """
    match = SHORT_ANSWER_PATTERN.search(content)

    if match:
        short_answer = match.group(1).strip()
        main_answer = SHORT_ANSWER_PATTERN.sub("", content).strip()
        return main_answer, short_answer

    # Fallback: first 3 sentences by "." — guard against decimals/abbreviations naively
    sentences = re.split(r"(?<!\d)\.(?!\d)\s+", content.strip())
    fallback = ". ".join(sentences[:3]).strip()
    if fallback and not fallback.endswith("."):
        fallback += "."

    return content.strip(), fallback

def create_structured_response(response, session_id):
    metadata = create_metadata(response, session_id)
    answer = response["messages"][-1].content
    main_answer, short_answer = extract_short_answer(answer)
    return ResponseSchema(
        answer=main_answer,
        short_answer=short_answer,
        metadata=metadata
    )

def get_response(query, session_id):
    messages = create_messages(query, session_id)

    try:
        response = agent.invoke({"messages": messages})
    except Exception as e:
        raise e

    # structured_response = get_structured_response(response, query)

    response_schema = create_structured_response(response, session_id)
    update_chat_history(query, response_schema.short_answer, session_id)

    return response_schema
