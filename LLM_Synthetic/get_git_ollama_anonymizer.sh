# git clone https://github.com/mithp/ollama-anonymizer.git


git clone https://github.com/mithp/ollama-anonymizer.git --config core.filemode=false


# WSL이나 VM에서 마운트된 디렉토리(/mnt/d/...)는 권한 변경을 지원하지 않을 수 있음
# 리눅스 홈 디렉토리(~/) 안에서 클론

# git 전역 변수를 수정:
git config --global core.filemode false
