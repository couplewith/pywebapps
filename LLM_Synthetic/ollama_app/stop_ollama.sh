#!/bin/bash
if pgrep -f "ollama serve" > /dev/null; then
    pkill -f "ollama serve"
    sleep 2
    if pgrep -f "ollama serve" > /dev/null; then
        pkill -9 -f "ollama serve"
    fi
    echo "✓ Ollama 정지 완료"
else
    echo "실행 중인 Ollama 없음"
fi
