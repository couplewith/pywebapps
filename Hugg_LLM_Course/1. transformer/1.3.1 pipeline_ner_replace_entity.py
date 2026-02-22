# 토큰 단위가 아닌 완전한 엔티티 문자열을 JSON으로 정리
# NER 결과를 엔티티별로 합쳐서 JSON 포맷으로 정리
from transformers import pipeline

# NER 파이프라인
recognizer = pipeline(
    "ner",
    model="dbmdz/bert-large-cased-finetuned-conll03-english",
    tokenizer="dbmdz/bert-large-cased-finetuned-conll03-english"
)

text = "HuggingFace is based in New York and was founded by Clément Delangue."
results = recognizer(text)

# JSON 포맷 변환 (엔티티 합치기)
def ner_to_json(results, text):
    entities = {"ORG": [], "LOC": [], "PER": []}
    merged = []
    current = None

    for ent in sorted(results, key=lambda x: x["start"]):
        label = ent["entity"].split("-")[-1]  # ORG, LOC, PER
        word = text[ent["start"]:ent["end"]]

        if current and current["label"] == label and ent["start"] == current["end"]:
            # 바로 이어지는 토큰이면 합치기
            current["text"] += " " + word
            current["end"] = ent["end"]
        else:
            if current:
                merged.append(current)
            current = {"label": label, "text": word, "end": ent["end"]}

    if current:
        merged.append(current)

    # JSON 구조로 변환
    for m in merged:
        entities[m["label"]].append(m["text"])

    return entities

print("Original:", text)
print("NER JSON:", ner_to_json(results, text))


# 앞의 예제와 달리 new york과 clément delangue가 각각 하나의 엔티티로 합쳐져서 출력됩니다.
# Original: HuggingFace is based in New York and was founded by Clément Delangue.
# NER JSON: {'ORG': ['HuggingFace'], 'LOC': ['New York'], 'PER': ['Clément Delangue']}