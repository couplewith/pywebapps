pip install llama-cpp-python

python3 -m llama_cpp.server \
  --model ./models/llama-4-7b.gguf \
  --host 0.0.0.0 \
  --port 8000

