#!/bin/bash
# Initialize Ollama with required model for Medical RAG Chatbot
# This script pulls the Llama 3.2 model if not already present

set -e  # Exit on error

OLLAMA_HOST="${OLLAMA_BASE_URL:-http://localhost:11434}"
MODEL="${OLLAMA_MODEL:-llama3.2:latest}"

echo "🚀 Initializing Ollama..."
echo "Host: $OLLAMA_HOST"
echo "Model: $MODEL"

# Wait for Ollama service to be ready
echo "⏳ Waiting for Ollama service..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -s "$OLLAMA_HOST/api/tags" > /dev/null 2>&1; then
        echo "✅ Ollama service is ready!"
        break
    fi
    attempt=$((attempt + 1))
    echo "Attempt $attempt/$max_attempts - Waiting for Ollama..."
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "❌ Failed to connect to Ollama service after $max_attempts attempts"
    exit 1
fi

# Check if model is already pulled
echo "🔍 Checking if model '$MODEL' is available..."
if docker exec medical-rag-ollama ollama list | grep -q "$MODEL"; then
    echo "✅ Model '$MODEL' is already available!"
else
    echo "📥 Pulling model '$MODEL' (this may take a few minutes, ~2GB download)..."
    docker exec medical-rag-ollama ollama pull "$MODEL"
    echo "✅ Model '$MODEL' pulled successfully!"
fi

echo "🎉 Ollama initialization complete!"
echo ""
echo "You can now use the Medical RAG Chatbot at http://localhost:5000"
echo ""
echo "To test the model directly:"
echo "  docker exec -it medical-rag-ollama ollama run $MODEL"
