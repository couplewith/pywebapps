from transformers import pipeline

# NER 파이프라인
recognizer = pipeline(
    "ner",
    model="dbmdz/bert-large-cased-finetuned-conll03-english",
    tokenizer="dbmdz/bert-large-cased-finetuned-conll03-english"
)

text = "HuggingFace is based in New York and was founded by Clément Delangue."
results = recognizer(text)

# 엔티티 치환
def replace_entities(text, results):
    # 결과를 start 위치 기준으로 정렬
    results = sorted(results, key=lambda x: x["start"])
    new_text = ""
    last_idx = 0
    for ent in results:
        # 원문에서 엔티티 앞부분 추가
        new_text += text[last_idx:ent["start"]]
        # 엔티티 치환
        if ent["entity"].endswith("ORG"):
            new_text += "[ORG]"
        elif ent["entity"].endswith("LOC"):
            new_text += "[LOC]"
        elif ent["entity"].endswith("PER"):
            new_text += "[PER]"
        else:
            new_text += text[ent["start"]:ent["end"]]
        last_idx = ent["end"]
    # 마지막 부분 추가
    new_text += text[last_idx:]
    return new_text
# JSON 포맷으로 변환
def ner_to_json(results):
    entities = {"ORG": [], "LOC": [], "PER": []}
    for ent in results:
        if ent["entity"].endswith("ORG"):
            entities["ORG"].append(ent["word"])
        elif ent["entity"].endswith("LOC"):
            entities["LOC"].append(ent["word"])
        elif ent["entity"].endswith("PER"):
            entities["PER"].append(ent["word"])
    return entities


print("Original:", text)
print("NER raw result:", results)
print("NER replaced:", replace_entities(text, results))
print("NER JSON:", ner_to_json(results))


# 
# Original: HuggingFace is based in New York and was founded by Clément Delangue.
# NER raw result: [{'entity': 'I-ORG', 'score': 0.9995, 'index': 1, 'word': 'HuggingFace', ...}, ...]

# Ner-replaced: 원문에서 인식된 조직명은 [ORG], 위치는 [LOC], 인물은 [PER]로 치환하여 출력
# NER replaced: [ORG] is based in [LOC] and was founded by [PER].   
# NER JSON: {'ORG': ['Hu', '##gging', '##F', '##ace'], 'LOC': ['New', 'York'], 'PER': ['C', '##lé', '##ment', 'Del', '##ang', '##ue']}
