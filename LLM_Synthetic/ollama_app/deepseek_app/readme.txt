DeepSeek 모델 다운로드

Ollama는 자체적으로 모델을 관리하므로 아래 명령어로 설치:

bash
ollama pull deepseek
원하는 버전이 있다면 deepseek-r1, deepseek-coder 등 구체적으로 지정 가능.

모델 실행

bash
ollama run deepseek
터미널에서 바로 대화형으로 모델을 실행할 수 있음.

모델 저장 위치

기본적으로 모델은 $HOME/.ollama/models 디렉토리에 저장됨.

필요 시 환경 변수 OLLAMA_MODELS를 지정해 별도 디렉토리 사용 가능:

bash
export OLLAMA_MODELS="${INSTALL_DIR}/models"
API 서버 활용

Ollama는 REST API를 제공하므로 외부 애플리케이션에서 DeepSeek 모델을 호출 가능:

bash
curl http://localhost:11434/api/generate -d '{
  "model": "deepseek",
  "prompt": "Hello, world!"
}'
