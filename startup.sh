#!/bin/bash
set -e

echo "🚀 Starting AI Tutor Application..."

# Start Ollama server in background
echo "📦 Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to be ready..."
sleep 10

# Check if Ollama is responding
max_retries=30
retry_count=0
until curl -s http://localhost:11434/api/tags > /dev/null 2>&1 || [ $retry_count -eq $max_retries ]; do
    echo "Waiting for Ollama... ($retry_count/$max_retries)"
    sleep 2
    retry_count=$((retry_count + 1))
done

if [ $retry_count -eq $max_retries ]; then
    echo "❌ Failed to start Ollama"
    exit 1
fi

echo "✅ Ollama is ready"

# Pull required models
echo "📥 Pulling phi3:mini model..."
ollama pull phi3:mini || echo "⚠️ Warning: Failed to pull phi3:mini"

echo "📥 Pulling mistral:7b model..."
ollama pull mistral:7b || echo "⚠️ Warning: Failed to pull mistral:7b"

echo "✅ Models ready"

# Start the Gradio application
echo "🎓 Starting AI Tutor application..."
python app.py

# If python exits, kill Ollama
kill $OLLAMA_PID 2>/dev/null || true
