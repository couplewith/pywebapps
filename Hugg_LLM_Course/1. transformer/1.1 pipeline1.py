from transformers import pipeline

# (강의) https://huggingface.co/docs/transformers/main_classes/pipelines
# (참조) https://huggingface.co/docs/transformers/main_classes/pipelines#natural-language-processing
# https://colab.research.google.com/drive/1cLMR7NNvQ_D29C_511yxGrICK185BaQZ#scrollTo=V0mDla5MtV5z

# sentiment-analysis : 감정 분석
classifier = pipeline("sentiment-analysis")
result = classifier("I've been waiting for a HuggingFace course my whole life.")
# 결과 출력
print("Sentiment result:", result)

# result -> Sentiment result: [{'label': 'POSITIVE', 'score': 0.9998}]
# 감정이 긍정적(POSITIVE) 이고 신뢰도 점수가 매우 높다는 결과



generator = pipeline("text-generation", model="LLAMA3")
result = generator("Hello, I'm a HuggingFace course!", max_length=30)
# 결과 출력
print("text-generation result:", result)


pipe = pipeline(model="FacebookAI/roberta-large-mnli")
result = pipe(["This restaurant is awesome", "This restaurant is awful"])
print("FacebookAI classification result:", result)
# [{'label': 'NEUTRAL', 'score': 0.7313136458396912}]


pipe = pipeline("text-classification")
result = pipe(["This restaurant is awesome", "This restaurant is awful"])
print("text-classification result:", result)
 
# [{'label': 'POSITIVE', 'score': 0.9998743534088135},
#  {'label': 'NEGATIVE', 'score': 0.9996669292449951}]

# pipeline : 모델과 토크나이저를 자동으로 로드하여 특정 작업을 수행하는 간단한 인터페이스 제공
# pipeline 종류      
# - audio-classification : 오디오 분류
# - feature-extraction : 특징 추출 (텍스트에 대한 벡터 표현 추출) 
# - fill-mask : 마스크 채우기
# - ner : 개체명 인식 (named entity recognition)
# - question-answering : 질의 응답
# - sentiment-analysis : 감정 분석
# - summarization : 요약
# - text-generation : 텍스트 생성
# - translation : 번역
# - zero-shot-classification : 제로샷 분류