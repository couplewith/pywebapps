from transformers import pipeline

# Named Entity Recognition (NER) 파이프라인
recognizer = pipeline(
    "ner",
    model="dbmdz/bert-large-cased-finetuned-conll03-english",
    tokenizer="dbmdz/bert-large-cased-finetuned-conll03-english"
)

# 테스트 문장
text = "HuggingFace is based in New York and was founded by Clément Delangue."

# 결과 출력
result = recognizer(text)
print("Named entity recognition result:", result)


#- ORG → HuggingFace (조직)
# - LOC → New York (위치)
# - PER → Clément Delangue (인물)
# 
#Key                      | Status     |  | 
#-------------------------+------------+--+-
#bert.pooler.dense.bias   | UNEXPECTED |  | 
#bert.pooler.dense.weight | UNEXPECTED |  | 
#
#Notes:
#- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
# Named entity recognition result: [
#  {'entity': 'I-ORG', 'score': 0.9995, 'index': 1, 'word': 'HuggingFace', 'start': 0, 'end': 11},
#  {'entity': 'I-LOC', 'score': 0.9994, 'index': 5, 'word': 'New', 'start': 23, 'end': 26},
#  {'entity': 'I-LOC', 'score': 0.9993, 'index': 6, 'word': 'York', 'start': 27, 'end': 31},
#  {'entity': 'I-PER', 'score': 0.9987, 'index': 12, 'word': 'Clément', 'start': 52, 'end': 59},
#  {'entity': 'I-PER', 'score': 0.9986, 'index': 13, 'word': 'Delangue', 'start': 60, 'end': 68}
#]