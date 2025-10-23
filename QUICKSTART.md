# LLM Duel - Quick Start Guide

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and edit it with your settings:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys and preferred settings.

## Running the App

### Option 1: Using the Startup Script (Recommended)

The startup scripts automatically clear cache to ensure you see the latest version.

**On Linux/Mac:**
```bash
./run.sh
```

### Option 2: Manual Start

```bash
# Clear cache first (important!)
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
rm -rf ~/.streamlit/cache

# Start the app
streamlit run app.py
```

## Accessing the App

Once started, open your browser to:
```
http://localhost:8501
```

**Important:** If you see old content or changes don't appear:
- Do a **hard refresh** in your browser:
  - **Windows/Linux**: `Ctrl + Shift + R` or `Ctrl + F5`
  - **Mac**: `Cmd + Shift + R`
- Or open in an **incognito/private window**

## Quick Configuration

### Minimal Setup (.env)

```env
# Use same API key for both models
OPENAI_API_KEY=your_api_key_here

# Set nicknames
MODEL_A_NICKNAME=Alice
MODEL_B_NICKNAME=Bob

# Set personas
MODEL_A_PERSONA=You are a thoughtful analyst
MODEL_B_PERSONA=You are a creative thinker
```

### Using Same Model for Both Personas

1. Configure Model A in the sidebar
2. Check "Use same model for both personas"
3. Set different nicknames and personas for variety

## Troubleshooting

### Changes Don't Appear

1. **Clear browser cache**: Hard refresh (`Ctrl+Shift+R`)
2. **Clear Python cache**: Delete `__pycache__` folders
3. **Clear Streamlit cache**: Delete `~/.streamlit/cache`
4. **Restart the app**: Use the startup scripts

### Stop Button Not Showing

- Make sure you're using the latest version
- Do a hard refresh in your browser
- The stop button appears in the second column when conversation is running

### Nicknames Not Showing

- Check that nicknames are set in `.env` or sidebar
- Hard refresh your browser
- Restart the app using `run.sh` 

## Features

- **Real-time conversation** between two AI models
- **Configurable personas** for each model
- **Custom system prompts** via `system_prompt.txt`
- **Turn delay** to prevent rate limiting
- **Export transcripts** in JSON and Markdown
- **Same model mode** to test different personas with one model

## Tips

- Start with 5-10 turns for testing
- Use temperature 0.7-1.0 for balanced creativity
- Edit `system_prompt.txt` to change conversation dynamics
- Use turn delay of 1-2 seconds to avoid rate limits

