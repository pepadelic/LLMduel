#!/bin/bash

# LLM Duel - Startup Script
# This script clears cache and starts the Streamlit app

echo "🚀 Starting LLM Duel..."

# Clear Python cache
echo "🧹 Clearing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null

# Clear Streamlit cache
echo "🧹 Clearing Streamlit cache..."
rm -rf ~/.streamlit/cache 2>/dev/null

# Start Streamlit
echo "▶️  Launching app..."
streamlit run app.py --server.port 8501

echo "✅ App started! Open http://localhost:8501 in your browser"
echo "💡 If you see old content, do a hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)"

