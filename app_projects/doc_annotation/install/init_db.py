# init_db.py (한 번 실행)
import sqlite3

base_path='C:\devData\work_2026\doc_annotation\data\annotation.db'
annotation_db=base_path + 'annotation.db'

conn = sqlite3.connect(annotation_db)
conn.execute('''
CREATE TABLE IF NOT EXISTS doc_papers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    authors TEXT,
    year INTEGER,
    journal TEXT,
    apa_citation TEXT,  -- APA 형식 인용문
    abstract TEXT,  -- 사용자가 입력한 논문 요약
    abstract_ko TEXT,  -- 사용자가 입력한 논문 요약 (한국어)
    paper_tags TEXT,  -- "tag1,tag2" 형식
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.execute(''')
CREATE TABLE IF NOT EXISTS doc_quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id INTEGER,   -- doc_papers.id 참조
    quote_text TEXT NOT NULL,   -- 인용문 텍스트
    page_block TEXT,  -- "p.10-12" 형식
    comment TEXT, -- 사용자가 입력한 코멘트
    annotation_tags TEXT, -- "tag1,tag2" 형식
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paper_id) REFERENCES papers (id)
)
''')
conn.commit()
conn.close()
print("DB 초기화 완료")
