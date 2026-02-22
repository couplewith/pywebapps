import sqlite3
import os
from datetime import datetime

BASE_PATH = r'C:\devData\work_2026\doc_annotation'
DATA_PATH = os.path.join(BASE_PATH, 'data')
DB_PATH = os.path.join(DATA_PATH, 'annotation.db')

def init_db():
    """DB 초기화"""
    os.makedirs(DATA_PATH, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
    CREATE TABLE IF NOT EXISTS doc_papers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        authors TEXT,
        year INTEGER,
        journal TEXT,
        apa_citation TEXT,
        abstract TEXT,
        abstract_ko TEXT,
        paper_tags TEXT,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS doc_quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paper_id INTEGER,
        quote_text TEXT NOT NULL,
        page_block TEXT,
        comment TEXT,
        annotation_tags TEXT,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (paper_id) REFERENCES doc_papers (id)
    )
    ''')
    conn.commit()
    conn.close()
    print("DB 초기화 완료:", DB_PATH)

def get_db():
    """DB 연결 반환"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Paper:
    @staticmethod
    def get_all(search='', tags=''):
        conn = get_db()
        query = 'SELECT * FROM doc_papers WHERE 1=1'
        params = []
        if search:
            query += ' AND (title LIKE ? OR authors LIKE ? OR abstract LIKE ? OR abstract_ko LIKE ?)'
            params.extend([f'%{search}%'] * 4)
        if tags:
            query += ' AND (paper_tags LIKE ?)'
            params.append(f'%{tags}%')
        query += ' ORDER BY created DESC'
        papers = conn.execute(query, params).fetchall()
        conn.close()
        return papers
    
    @staticmethod
    def get_by_id(paper_id):
        conn = get_db()
        paper = conn.execute('SELECT * FROM doc_papers WHERE id = ?', (paper_id,)).fetchone()
        conn.close()
        return paper
    
    @staticmethod
    def create(title, authors, year, journal, apa_citation, abstract, abstract_ko, paper_tags):
        conn = get_db()
        conn.execute('''INSERT INTO doc_papers 
                        (title, authors, year, journal, apa_citation, abstract, abstract_ko, paper_tags) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                     (title, authors, year, journal, apa_citation, abstract, abstract_ko, paper_tags))
        conn.commit()
        paper_id = conn.cursor().lastrowid
        conn.close()
        return paper_id
    
    
    @staticmethod
    def update(paper_id, title, authors, year, journal, apa_citation, abstract, abstract_ko, paper_tags):
        """논문 수정"""
        conn = get_db()
        conn.execute('''UPDATE doc_papers 
                        SET title=?, authors=?, year=?, journal=?, apa_citation=?, 
                            abstract=?, abstract_ko=?, paper_tags=?
                        WHERE id=?''',
                     (title, authors, year, journal, apa_citation, abstract, abstract_ko, paper_tags, paper_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete(paper_id):
        """논문 삭제 (연관 인용도 삭제)"""
        conn = get_db()
        # 먼저 연관 인용 삭제
        conn.execute('DELETE FROM doc_quotes WHERE paper_id = ?', (paper_id,))
        # 논문 삭제
        conn.execute('DELETE FROM doc_papers WHERE id = ?', (paper_id,))
        conn.commit()
        conn.close()

#####################################
class Quote:
    @staticmethod
    def get_by_paper(paper_id):
        conn = get_db()
        quotes = conn.execute('SELECT * FROM doc_quotes WHERE paper_id = ? ORDER BY created DESC', 
                             (paper_id,)).fetchall()
        conn.close()
        return quotes
    
    @staticmethod
    def create(paper_id, quote_text, page_block, comment, annotation_tags):
        conn = get_db()
        conn.execute('''INSERT INTO doc_quotes (paper_id, quote_text, page_block, comment, annotation_tags) 
                        VALUES (?, ?, ?, ?, ?)''',
                     (paper_id, quote_text, page_block, comment, annotation_tags))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete(quote_id):
        conn = get_db()
        paper_id = conn.execute('SELECT paper_id FROM doc_quotes WHERE id = ?', (quote_id,)).fetchone()['paper_id']
        conn.execute('DELETE FROM doc_quotes WHERE id = ?', (quote_id,))
        conn.commit()
        conn.close()
        return paper_id
    

