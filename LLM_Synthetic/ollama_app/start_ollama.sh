#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/logs/ollama.log"
source "${SCRIPT_DIR}/ollama_env.sh"

if pgrep -f "ollama serve" > /dev/null; then
    echo "Ollama가 이미 실행 중입니다."
    exit 1
fi

echo "Ollama 시작 중..."
nohup "${SCRIPT_DIR}/ollama" serve >> "$LOG_FILE" 2>&1 &
sleep 3

if pgrep -f "ollama serve" > /dev/null; then
    echo "✓ Ollama 시작 완료 (포트: 11434)"
else
    echo "✗ 시작 실패. 로그: $LOG_FILE"
    exit 1
fi
