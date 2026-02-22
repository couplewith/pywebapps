# 1. Hugging Face aggregation_strategy 활용
# pipeline("ner")는 기본적으로 토큰 단위 결과를 반환하지만, aggregation_strategy="simple" 옵션을 주면 자동으로 연속된 토큰을 하나의 엔티티로 합쳐줍니다.

from transformers import pipeline

recognizer = pipeline(
    "ner",
    model="dbmdz/bert-large-cased-finetuned-conll03-english",
    tokenizer="dbmdz/bert-large-cased-finetuned-conll03-english",
    aggregation_strategy="simple"   # 엔티티 자동 합치기
)

text = "HuggingFace is based in New York and was founded by Clément Delangue."
results = recognizer(text)

print("NER aggregated result:", results)


# 결과 예시
# NER aggregated result: [
#  {'entity_group': 'ORG', 'score': 0.9995, 'word': 'HuggingFace', 'start': 0, 'end': 11},
#  {'entity_group': 'LOC', 'score': 0.9993, 'word': 'New York', 'start': 23, 'end': 31},
#  {'entity_group': 'PER', 'score': 0.9986, 'word': 'Clément Delangue', 'start': 52, 'end': 68}
# ]