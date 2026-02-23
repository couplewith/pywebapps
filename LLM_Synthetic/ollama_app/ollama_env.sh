#!/bin/bash
export OLLAMA_HOME=/data/ollama_app
export OLLAMA_MODELS=/data/ollama_app/models
export OLLAMA_HOST=0.0.0.0:11434
export PATH=/data/ollama_app/bin:$PATH
echo "Ollama 환경 변수 로드 완료"
