import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from lama.modules import construct_lama_modules

# 사전 학습된 GPT-2 모델 및 토크나이저 로드
model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# LAMA 모듈 생성
lama_modules = construct_lama_modules(model, tokenizer)

# 편향 분석할 문장
sentence = "He is a nurse."
target = "she"

# LAMA를 사용하여 편향 분석 수행
results = lama_modules.bias_direction.compute_bias(sentence, target)

# 결과 출력
print("Bias Score:", results['bias_score'])
print("Neutral Score:", results['neutral_score'])
