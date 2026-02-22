from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer

# Sentiment analysis pipeline (기본 모델: distilbert-base-uncased-finetuned-sst-2-english)
analyzer = pipeline("sentiment-analysis")

# Question answering pipeline (DistilBERT SQuAD 모델)
oracle = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad",
    tokenizer="distilbert-base-cased-distilled-squad"
)

# Named entity recognition pipeline (CoNLL03 NER 모델)
model = AutoModelForTokenClassification.from_pretrained(
    "dbmdz/bert-large-cased-finetuned-conll03-english"
)
tokenizer = AutoTokenizer.from_pretrained(
    "dbmdz/bert-large-cased-finetuned-conll03-english"
)
recognizer = pipeline("ner", model=model, tokenizer=tokenizer)

# 결과 출력
print("Sentiment analysis result:",
      analyzer("I love HuggingFace!"))

print("Question answering result:",
      oracle(
          question="What is HuggingFace?",
          context="HuggingFace is a company that provides open-source tools for natural language processing."
      ))

print("Named entity recognition result:",
      recognizer("HuggingFace is based in New York and was founded by Clément Delangue."))

#
# BertForTokenClassification LOAD REPORT from: dbmdz/bert-large-cased-finetuned-conll03-english
# Key                      | Status     |  | 
# -------------------------+------------+--+-
# bert.pooler.dense.bias   | UNEXPECTED |  | 
# bert.pooler.dense.weight | UNEXPECTED |  | 
# 위 모델은 토큰 분류용으로 pooler 레이어가 없어서 UNEXPECTED로 뜨지만, NER 파이프라인에서는 문제없이 작동합니다.


# vocab.txt: 
#  213k/? [00:00<00:00, 3.02MB/s]

# Sentiment analysis result: [{'label': 'POSITIVE', 'score': 0.9998130202293396}]
# Question answering result: {'score': 0.40548229217529297, 'start': 15, 'end': 88, 'answer': 'a company that provides open-source tools for natural language processing'}
# Named entity recognition result: [{'entity': 'I-ORG', 'score': np.float32(0.99629116), 'index': 1, 'word': 'Hu', 'start': 
# > entiment-analysis : 감정 분석 결과 양성
# > Question answering : 질문에 대한 답변과 신뢰도 점수 
# > Named entity recognition : 문장에서 인식된 개체명과 그 유형 (I-ORG: 조직명, I-PER: 인명, I-LOC: 지명 등)
