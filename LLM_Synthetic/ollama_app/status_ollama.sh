#!/bin/bash
if pgrep -f "ollama serve" > /dev/null; then
    echo "✓ Ollama 실행 중"
    ps aux | grep "ollama serve" | grep -v grep
else
    echo "✗ Ollama 정지됨"
fi
