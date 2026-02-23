import os
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
import sys

# WSL Ollama 연결 (Windows 접근 시 IP 변경)
WSL_IP = "172.30.96.1"  # wsl hostname -I로 확인
BASE_URL = f"http://{WSL_IP}:11434"

# 1. 비식별화 데이터 (금융 거래)
financial_data = [
    "2026-01-15 고객 홍길동 계좌 1111-2222-3333에서 2,500,000원 주식 매수.",
    "2026-01-20 이순신 계좌 4444-5555-6666으로 1,200,000원 예금 이자 입금.",
    "2026-02-01 박지성 계좌 7777-8888-9999에서 800,000원 카드 결제.",
    "2026-02-05 김연아 계좌 0000-1111-2222로 3,000,000원 대출 상환.",
    "2026-02-09 최수봉 계좌 3333-4444-5555에서 450,000원 보험료 납부."
]

def anonymize_data(data):
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()
    anonymized = []
    for text in data:
        results = analyzer.analyze(text=text, language='ko')
        anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results)
        anonymized.append(anonymized_text.text)
    return anonymized

def build_rag_chain():
    # 비식별화
    anon_docs = anonymize_data(financial_data)
    print("Anonymized data:", anon_docs)
    
    # 청킹 & 임베딩
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.create_documents(anon_docs)
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
    
    # FAISS DB (영속: faiss_index 폴더)
    db_path = "faiss_index"
    if os.path.exists(db_path):
        vector_db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
        print("Loaded existing FAISS index.")
    else:
        vector_db = FAISS.from_documents(chunks, embeddings)
        vector_db.save_local(db_path)
        print("Created new FAISS index.")
    
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    
    # Ollama LLM (WSL 서버)
    llm = OllamaLLM(model="llama3", base_url=BASE_URL)
    
    # RAG 체인
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

if __name__ == "__main__":
    print(f"Connecting to Ollama at {BASE_URL}")
    chain = build_rag_chain()
    
    print("\n=== 금융 RAG 서비스 시작 (quit 입력 종료) ===")
    while True:
        query = input("\nQuery: ")
        if query.lower() == 'quit':
            break
        result = chain({"query": query})
        print("Answer:", result["result"])
        print("Sources:")
        for i, doc in enumerate(result["source_documents"], 1):
            print(f"  {i}. {doc.page_content}")
