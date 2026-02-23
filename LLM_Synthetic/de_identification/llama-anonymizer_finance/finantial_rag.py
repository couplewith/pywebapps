# 1. 라이브러리 및 Presidio
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")  # 한국어 최적
llm = OllamaLLM(model="llama3")
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)

# 2. 비식별화
anonymized_docs = []
for text in financial_data:
    results = analyzer.analyze(text=text, language='ko')
    anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
    anonymized_docs.append(anonymized.text)

# 3. 벡터 DB
chunks = splitter.create_documents(anonymized_docs)
vector_db = FAISS.from_documents(chunks, embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 2})

# 4. QA 체인
qa_chain = RetrievalQA.from_chain_type(
    llm=llm, retriever=retriever, return_source_documents=True
)

# 5. 테스트 쿼리
queries = [
    "2월 거래 중 가장 큰 금액은?",
    "주식 매수 거래는 언제?",
    "대출 상환 내역 알려줘"
]

for q in queries:
    result = qa_chain({"query": q})
    print(f"Query: {q}")
    print(f"Answer: {result['result']}")
    print(f"Source: {[doc.page_content for doc in result['source_documents']]}")
    print("-" * 50)
