# LLMduel

An interactive web application where two configurable Large Language Models (LLMs) hold a conversation with each other in real time. Built with Streamlit, this app allows you to observe and analyze AI-to-AI dialogue on any topic you choose.

## Features

### Core Functionality
- **Dual Model Configuration**: Set up two different LLMs with unique personas and behaviors
- **Real-Time Conversation**: Watch the dialogue unfold turn by turn with visual feedback
- **Flexible API Support**: Works with OpenAI and any OpenAI-compatible API endpoints
- **Custom Personas**: Define distinct personalities and behavioral patterns for each model
- **Topic-Driven Discussions**: Guide conversations with specific discussion topics
- **Customizable System Prompts**: Fine-tune conversation flow and dynamics via `system_prompt.txt`

### User Experience
- **Visual Distinction**: Clear color-coded display distinguishing between Model A and Model B
- **Progress Tracking**: Real-time indicators showing current turn, active model, and overall progress
- **Interactive Controls**: Start, stop, and monitor conversations with intuitive buttons
- **Conversation Statistics**: View metrics including turn count, message distribution, and response times

### Export & Analysis
- **JSON Export**: Download complete conversation data with metadata and timestamps
- **Markdown Export**: Generate formatted transcripts for easy reading and sharing
- **Session Management**: Maintain conversation history and configuration throughout the session

### Robustness
- **Error Handling**: Graceful handling of API failures, timeouts, and invalid configurations
- **Input Validation**: Comprehensive validation of all user inputs before starting conversations
- **Secure API Keys**: Password-protected input fields for sensitive credentials
- **Configurable Limits**: Set maximum turn counts to prevent runaway conversations

## Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Setup

1. **Clone or download the application files**

2. **Install required dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables (recommended)**
```bash
cp .env.example .env
# Edit .env and configure your settings:
# - API keys for both models
# - Model names and endpoints
# - Default personas and discussion topics
# - Turn delay to prevent rate limiting
```

The `.env` file provides default values for all settings. You can override any of these in the GUI when running the app.

## Usage

### Starting the Application

Run the Streamlit app from the command line:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Configuration Workflow

1. **Configure Model A** (in the sidebar):
   - Enter API key (or use environment variable)
   - Optionally specify a custom base URL
   - Enter the model name (e.g., `gpt-4.1-mini`, `gpt-4`, `mistral`)
   - Define the persona/behavioral description

2. **Configure Model B** (in the sidebar):
   - Follow the same steps as Model A
   - Use different settings to create interesting dynamics

3. **Set Conversation Parameters**:
   - Enter a discussion topic
   - Set maximum number of turns (2-50)
   - Adjust temperature (0.0-2.0) for response randomness

4. **Start the Conversation**:
   - Click "▶️ Start Conversation"
   - Watch the models exchange messages in real time
   - Use "⏹️ Stop" to end the conversation early

5. **Export Results**:
   - After completion, download the transcript in JSON or Markdown format
   - Review conversation statistics

### Example Configuration

**Model A:**
- Model: `gpt-4.1-mini`
- Persona: "You are a thoughtful and analytical assistant who enjoys exploring ideas in depth."

**Model B:**
- Model: `gpt-4.1-nano`
- Persona: "You are a creative and curious assistant who likes to ask questions and challenge assumptions."

**Discussion Topic:** "The impact of artificial intelligence on society"

**Settings:** 10 turns, temperature 0.7

## Architecture

### Application Structure

```
llm-conversation-app/
├── app.py                 # Main Streamlit application
├── llm_client.py          # LLM API client utility
├── conversation.py        # Conversation orchestration logic
├── system_prompt.txt      # Customizable system prompt template
├── .env.example           # Environment variable template
└── README.md              # This file
```

### Component Overview

**Frontend (Streamlit UI)**
- Configuration sidebar for model and conversation settings
- Main conversation display area with color-coded messages
- Control buttons for starting/stopping conversations
- Statistics dashboard and export functionality

**Backend Logic**
- `LLMClient`: Handles API communication with LLM endpoints
- `ConversationOrchestrator`: Manages turn-taking and conversation flow
- Session state management for maintaining conversation history

**API Integration**
- OpenAI-compatible API client
- Support for custom endpoints and authentication
- Error handling and timeout management

## Configuration Options

### Environment Variables (.env)

All configuration can be set via environment variables in a `.env` file. This is the recommended approach for local deployment as it:
- Keeps API keys secure and out of the GUI
- Provides sensible defaults for all settings
- Allows easy switching between different configurations
- Prevents rate limiting with configurable delays

See `.env.example` for all available options. GUI values will override `.env` settings if provided.

### Model Configuration

| Parameter | Description | Example |
|-----------|-------------|---------|
| API Key | Authentication token for the LLM service | `sk-...` |
| Base URL | Custom API endpoint (optional) | `https://api.openai.com/v1` |
| Model Name | Identifier for the specific model | `gpt-4.1-mini` |
| Persona | Behavioral description for the model | "You are analytical..." |

### Conversation Settings

| Parameter | Description | Range/Type |
|-----------|-------------|------------|
| Discussion Topic | Subject matter for the conversation | Text (required) |
| Maximum Turns | Total number of exchanges | 2-50 |
| Temperature | Response randomness/creativity | 0.0-2.0 |
| Turn Delay | Delay between turns in seconds | 0.0-5.0 |

### Custom System Prompts

The application supports custom system prompts via the `system_prompt.txt` file, allowing you to fine-tune conversation dynamics and flow. This powerful feature lets you:

- **Control Conversation Style**: Define how models should interact (debate, collaboration, exploration)
- **Set Response Guidelines**: Specify length, tone, and interaction patterns
- **Influence Turn-Taking**: Guide how models build on each other's responses
- **Customize Engagement**: Create specific conversation atmospheres

#### Default System Prompt

The included `system_prompt.txt` provides a comprehensive template that:
- Encourages dynamic, thought-provoking dialogue
- Prevents repetitive or summary-style responses
- Promotes question-asking and idea-building
- Maintains conversational momentum
- Ensures responses stay focused and engaging

#### Customizing the System Prompt

To customize conversation behavior:

1. **Edit `system_prompt.txt`** with your desired conversation guidelines
2. **Use placeholders**: `{topic}` is automatically replaced with the discussion topic
3. **Set response constraints**: Control length, style, and interaction patterns
4. **Define conversation rules**: Specify how models should engage with each other

#### Example Customizations

**Debate Mode:**
```
You are in a structured debate about: {topic}
Take a clear position and defend it with evidence.
Challenge your opponent's arguments directly.
Keep responses concise and focused.
```

**Collaborative Mode:**
```
You are collaborating on: {topic}
Build on your partner's ideas constructively.
Ask clarifying questions to deepen understanding.
Work together to explore new possibilities.
```

**Exploration Mode:**
```
You are exploring: {topic}
Ask "what if" questions to push boundaries.
Connect ideas in unexpected ways.
Challenge assumptions and conventional thinking.
```

## Supported Models

The application works with any OpenAI-compatible API. Common options include:

- **OpenAI Models**: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`
- **Custom Models**: Any model accessible via OpenAI-compatible endpoints
- **Local Models**: Models served through compatible inference servers

## Error Handling

The application includes comprehensive error handling for:

- **Configuration Errors**: Missing or invalid API keys, model names, or settings
- **API Errors**: Network failures, authentication issues, rate limits
- **Timeout Errors**: Requests that exceed the configured timeout period
- **Response Errors**: Invalid or incomplete responses from the API

When errors occur, the application:
1. Displays a clear error message to the user
2. Stops the conversation gracefully
3. Preserves any conversation history generated before the error

## Export Formats

### JSON Format
Complete conversation data including:
- Turn numbers and speakers
- Message content and timestamps
- Token usage statistics (if available)
- Response time metrics

### Markdown Format
Human-readable transcript with:
- Configuration summary
- Formatted conversation with headers
- Statistics section
- Timestamps for each message

## Best Practices

### Creating Engaging Conversations

1. **Define Distinct Personas**: Give each model a unique perspective or role
2. **Choose Focused Topics**: Specific topics lead to more coherent discussions
3. **Adjust Temperature**: Higher values (0.8-1.0) for creative discussions, lower (0.3-0.5) for analytical
4. **Set Appropriate Limits**: Start with 10-15 turns and adjust based on results
5. **Customize System Prompts**: Edit `system_prompt.txt` to control conversation flow and style

### Performance Optimization

1. **Use Efficient Models**: Smaller models respond faster and cost less
2. **Monitor Token Usage**: Check statistics to understand API consumption
3. **Set Reasonable Timeouts**: Balance between patience and responsiveness

### Security Considerations

1. **Protect API Keys**: Never commit `.env` files or expose keys in screenshots
2. **Use Environment Variables**: Store credentials in `.env` for local development
3. **Monitor Usage**: Keep track of API calls to avoid unexpected charges

## Troubleshooting

### Common Issues

**Issue**: "API key is required" error
- **Solution**: Ensure API keys are entered in the sidebar or set in `.env`

**Issue**: Conversation stops unexpectedly
- **Solution**: Check error messages; may be due to API limits or network issues

**Issue**: Slow response times
- **Solution**: Try using faster models or check network connectivity

**Issue**: Models repeat themselves
- **Solution**: Increase temperature or adjust personas for more variety

## Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment

For production deployment, consider:

1. **Streamlit Cloud**: Deploy directly from a Git repository
2. **Docker**: Containerize the application for consistent deployment
3. **Cloud Platforms**: Deploy to AWS, Google Cloud, or Azure

### Environment Variables for Production

Set the following environment variables:
- `OPENAI_API_KEY`: Default API key for models
- `STREAMLIT_SERVER_PORT`: Custom port (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Bind address (default: localhost)

## Optional Enhancements

The application can be extended with:

- **Multiple Conversation Rounds**: Save and load previous conversations
- **Advanced Metrics**: Sentiment analysis, topic tracking, agreement scoring
- **Different Conversation Styles**: Formal debate, Socratic dialogue, brainstorming
- **Model Comparison**: Run the same conversation with different model combinations
- **Conversation Branching**: Allow user intervention to guide the discussion

## Technical Details

### Dependencies
- `streamlit`: Web application framework
- `openai`: OpenAI API client library
- `python-dotenv`: Environment variable management

### Session State Management
The application uses Streamlit's session state to maintain:
- Conversation history with full message data
- Model client instances
- Configuration settings
- Conversation status (running/stopped)
- Current turn counter

### API Communication
- Uses OpenAI's chat completion API format
- Supports streaming and non-streaming responses
- Includes retry logic and timeout handling
- Tracks token usage and response times

## License

This application is provided as-is for educational and experimental purposes.

## Support

For issues, questions, or contributions, please refer to the project repository or contact the development team.

## Acknowledgments

Built with Streamlit and designed to work with OpenAI-compatible language models.
