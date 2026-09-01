# LLM-Powered Chatbot with Tool Integration

A Python-based conversational AI assistant powered by Groq's LLM models, featuring real-time streaming responses, chat history management, and integrated tools for dynamic functionality.

## Features

- **Interactive CLI Interface** - Rich-formatted command-line interface with styled prompts and responses
- **LLM-Powered Conversations** - Integration with Groq's OpenAI-compatible models for intelligent responses
- **Real-time Streaming** - Stream responses in real-time with live formatting and visual separation of reasoning and content
- **Tool Integration** - Built-in weather tool for fetching real-time weather information
- **Chat History Management** - In-memory chat history storage with session management
- **Structured Output** - Pydantic-based schema validation with comprehensive metadata tracking
- **Token Usage Tracking** - Monitor input/output tokens and total token consumption per query
- **Reasoning Display** - Shows AI reasoning process separately from final responses
- **Session Management** - Support for multiple concurrent chat sessions with isolated conversation histories

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Groq API key
- WeatherAPI key (for weather tool functionality)

## Installation

### 1. Clone or Extract the Project

```bash
cd /path/to/project_1
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Packages

- **langchain-groq** - Groq integration for LangChain
- **python-dotenv** - Environment variable management
- **rich** - Beautiful terminal formatting and progress displays

## Configuration

### Environment Variables

Create a `.env` file in the project root directory with the following variables:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Weather API Configuration (for weather tool)
WHETHER_API_KEY=your_weatherapi_key_here
```

### Obtaining API Keys

1. **Groq API Key**:
   - Visit [Groq Console](https://console.groq.com)
   - Create an account and generate an API key
   - Copy the key to your `.env` file

2. **WeatherAPI Key**:
   - Visit [WeatherAPI.com](https://www.weatherapi.com/)
   - Sign up for a free account
   - Generate an API key from the dashboard
   - Copy the key to your `.env` file

## Usage

### Running the CLI Interface

```bash
cd src
python cli.py
```

Then interact with the chatbot by typing your queries at the prompt:

```
❯ What's the weather in Tokyo?
```

### Running Specific CLI Modes

The project supports multiple interaction modes:

1. **Streaming Mode** - Real-time response streaming with visual formatting
2. **Invoke Mode** - Complete response generation with reasoning extraction
3. **Structured Output Mode** - Responses with metadata and token usage

### Example Interactions

**Query with Tool Usage:**
```
❯ What's the weather in Tokyo?
```

**Query with Chat History:**
```
❯ My name is John.
❯ What's my name?
```

**General Knowledge Query:**
```
❯ Explain quantum computing in simple terms.
```

## Project Structure

```
project_1/
├── requirements.txt          # Project dependencies
├── README.md                 # This file
└── src/
    ├── cli.py               # CLI interface and user interaction
    ├── llm.py               # LLM model configuration and response handling
    ├── schemas.py           # Pydantic models for data validation
    ├── utilities.py         # Utility functions (weather tool)
    └── tests/
        ├── runner.py        # Test execution runner
        └── test_cases.json  # Test case definitions for tool routing
```

### Key Components

#### `cli.py`
Handles user interface and interaction:
- `take_input()` - Captures user queries with styled prompts
- `call_llm_and_get_response()` - Sends queries to LLM
- `get_content_reasoning()` - Extracts reasoning from AI responses
- `run_cli_stream()` - Streams responses in real-time with live formatting
- `run_cli_invoke()` - Generates complete responses with reasoning

#### `llm.py`
Core LLM integration and chat management:
- Groq ChatGroq model initialization
- Agent creation with tool integration
- Session management for chat history
- Token usage tracking and metadata generation
- Message history management for context awareness

#### `schemas.py`
Data models for type safety:
- `ChatHistory` - Stores user queries and AI responses
- `Metadata` - Tracks tokens, tools used, and conversation history
- `ResponseSchema` - Structured response format with metadata

#### `utilities.py`
Utility functions and tools:
- `get_weather()` - Weather tool that fetches current temperature for any city

## Testing

Test cases are defined in `src/tests/test_cases.json` and cover:

- **Tool Routing** - Ensures the model correctly identifies and calls the weather tool
- **Memory Checks** - Validates that the system maintains conversation context
- **Accuracy** - Prevents hallucination and ensures factual responses

### Running Tests

```bash
cd src/tests
python runner.py
```

## Model Configuration

The project uses Groq's model: `openai/gpt-oss-safeguard-20b`

- **Max Tokens**: 4096
- **Model Type**: Open-source safeguarded model
- **API Provider**: Groq (faster inference than typical OpenAI)

You can modify the model in `src/llm.py` by changing the `model` parameter in the `ChatGroq` initialization.

## Features in Detail

### Session Management

The system maintains separate chat sessions:

```python
# Each session maintains isolated chat history
session_1 = get_session("session_1")
session_2 = get_session("session_2")
# Conversations don't interfere with each other
```

### Token Tracking

Monitor your API usage:

```
Input Tokens: 125
Output Tokens: 342
Total Tokens: 467
```

### Response Formatting

Responses are displayed with:
- **AI Reasoning** - Internal thought process (in green panel)
- **AI Response** - Final answer (in blue panel)
- **Markdown Support** - Formatted content with proper styling

## Troubleshooting

### API Key Errors

**Issue**: `"Invalid API key"` or authentication errors

**Solution**: 
- Verify `.env` file exists in the project root
- Check API keys are correct and not expired
- Ensure keys don't have leading/trailing spaces

### Weather Tool Errors

**Issue**: `"Error fetching weather data"`

**Solution**:
- Verify `WHETHER_API_KEY` is set correctly
- Check internet connectivity
- Ensure city name is spelled correctly

### Import Errors

**Issue**: `"ModuleNotFoundError"`

**Solution**:
```bash
pip install -r requirements.txt
# Reinstall packages if needed
pip install --force-reinstall -r requirements.txt
```

## Contributing

Contributions are welcome! Areas for enhancement:

- Additional tools (news, calculations, translations)
- Database persistence for chat history
- User authentication system
- Web interface
- Rate limiting and usage quotas

## License

[Specify your license here, e.g., MIT, Apache 2.0, etc.]

## Support

For issues or questions:
- Check the troubleshooting section above
- Review test cases in `src/tests/test_cases.json` for expected behavior
- Verify API keys and environment configuration

## Future Enhancements

- [ ] Persistent database for chat history
- [ ] Additional weather-related tools
- [ ] Web UI with FastAPI/Flask
- [ ] Conversation export to markdown/JSON
- [ ] Custom system prompts per session
- [ ] Rate limiting and usage analytics dashboard
