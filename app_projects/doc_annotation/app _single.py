from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
import os
from io import StringIO
import xml.etree.ElementTree as ET
from datetime import datetime

BASE_PATH = r'C:\devData\work_2026\doc_annotation'
DATA_PATH = os.path.join(BASE_PATH, 'data')
HTML_PATH = os.path.join(BASE_PATH, 'html')
DB_PATH = os.path.join(DATA_PATH, 'annotation.db')

os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(HTML_PATH, exist_ok=True)

app = Flask(__name__, template_folder=HTML_PATH)
app.secret_key = 'dev_annotation_secret_2026'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.before_first_request
def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS doc_papers (
        id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, authors TEXT, year INTEGER,
        journal TEXT, apa_citation TEXT, abstract TEXT, abstract_ko TEXT, paper_tags TEXT,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS doc_quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, paper_id INTEGER, quote_text TEXT NOT NULL,
        page_block TEXT, comment TEXT, annotation_tags TEXT, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(paper_id) REFERENCES doc_papers(id))''')
    conn.commit()
    conn.close()
    print("✅ DB 초기화 완료")

@app.route('/')
def index():
    search = request.args.get('search', '')
    tags = request.args.get('tags', '').strip()
    conn = get_db()
    query = 'SELECT * FROM doc_papers WHERE 1=1'
    params = []
    if search:
        query += ' AND (title LIKE ? OR authors LIKE ? OR abstract LIKE ? OR abstract_ko LIKE ?)'
        params.extend([f'%{search}%']*4)
    if tags:
        query += ' AND paper_tags LIKE ?'
        params.append(f'%{tags}%')
    query += ' ORDER BY created DESC'
    papers = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('index.html', papers=papers, search=search, tags=tags)

# 나머지 라우트들 (add_paper, paper_info, add_quote, delete_quote, export_xml)
# ... (모든 기능 포함, 이전 단일 app.py 버전과 동일)

if __name__ == '__main__':
    print("🚀 앱 시작: http://127.0.0.1:5000")
    app.run(debug=True)
