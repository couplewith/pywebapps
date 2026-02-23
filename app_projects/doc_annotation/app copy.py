from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
import os
from io import StringIO
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

BASE_PATH = r'C:\devData\work_2026\doc_annotation\data'
DB_PATH = os.path.join(BASE_PATH, 'annotation.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    search = request.args.get('search', '')
    tags = request.args.get('tags', '').strip()
    
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
    return render_template('index.html', papers=papers, search=search, tags=tags)

@app.route('/paper/<int:paper_id>')
def paper(paper_id):
    conn = get_db()
    paper = conn.execute('SELECT * FROM doc_papers WHERE id = ?', (paper_id,)).fetchone()
    quotes = conn.execute('SELECT * FROM doc_quotes WHERE paper_id = ? ORDER BY created DESC', (paper_id,)).fetchall()
    conn.close()
    if paper is None:
        flash('논문을 찾을 수 없습니다.')
        return redirect(url_for('index'))
    return render_template('paper.html', paper=paper, quotes=quotes)

@app.route('/add_paper', methods=['GET', 'POST'])
def add_paper():
    if request.method == 'POST':
        title = request.form['title']
        authors = request.form['authors']
        year = request.form['year']
        journal = request.form['journal']
        apa_citation = request.form['apa_citation']
        abstract = request.form['abstract']
        abstract_ko = request.form['abstract_ko']
        paper_tags = request.form['paper_tags']
        if not title:
            flash('제목은 필수입니다.')
            return render_template('add_paper.html')
        conn = get_db()
        conn.execute('''INSERT INTO doc_papers (title, authors, year, journal, apa_citation, abstract, 
                        abstract_ko, paper_tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                     (title, authors, year, journal, apa_citation, abstract, abstract_ko, paper_tags))
        conn.commit()
        paper_id = conn.cursor().lastrowid
        conn.close()
        flash('논문이 추가되었습니다.')
        return redirect(url_for('paper', paper_id=paper_id))
    return render_template('add_paper.html')

@app.route('/add_quote/<int:paper_id>', methods=['POST'])
def add_quote(paper_id):
    quote_text = request.form['quote_text']
    page_block = request.form['page_block']
    comment = request.form['comment']
    annotation_tags = request.form['annotation_tags']
    if not quote_text:
        flash('인용문은 필수입니다.')
    else:
        conn = get_db()
        conn.execute('''INSERT INTO doc_quotes (paper_id, quote_text, page_block, comment, annotation_tags) 
                        VALUES (?, ?, ?, ?, ?)''',
                     (paper_id, quote_text, page_block, comment, annotation_tags))
        conn.commit()
        conn.close()
        flash('인용이 추가되었습니다.')
    return redirect(url_for('paper', paper_id=paper_id))

@app.route('/delete_quote/<int:quote_id>')
def delete_quote(quote_id):
    conn = get_db()
    paper_id = conn.execute('SELECT paper_id FROM doc_quotes WHERE id = ?', (quote_id,)).fetchone()['paper_id']
    conn.execute('DELETE FROM doc_quotes WHERE id = ?', (quote_id,))
    conn.commit()
    conn.close()
    flash('인용이 삭제되었습니다.')
    return redirect(url_for('paper', paper_id=paper_id))

@app.route('/export_xml')
def export_xml():
    conn = get_db()
    papers = conn.execute('''
        SELECT p.*, q.quote_text, q.page_block, q.comment, q.annotation_tags as quote_tags
        FROM doc_papers p LEFT JOIN doc_quotes q ON p.id = q.paper_id
        ORDER BY p.id
    ''').fetchall()
    conn.close()

    root = ET.Element('papers')
    current_paper = None
    paper_elem = None
    for row in papers:
        if current_paper != row['id']:
            current_paper = row['id']
            paper_elem = ET.SubElement(root, 'paper')
            paper_elem.set('id', str(row['id']))
            ET.SubElement(paper_elem, 'title').text = row['title']
            ET.SubElement(paper_elem, 'authors').text = row['authors']
            ET.SubElement(paper_elem, 'year').text = str(row['year'])
            ET.SubElement(paper_elem, 'journal').text = row['journal']
            ET.SubElement(paper_elem, 'apa_citation').text = row['apa_citation']
            ET.SubElement(paper_elem, 'abstract').text = row['abstract']
            ET.SubElement(paper_elem, 'abstract_ko').text = row['abstract_ko']
            ET.SubElement(paper_elem, 'paper_tags').text = row['paper_tags']
            quotes_elem = ET.SubElement(paper_elem, 'quotes')
        if row['quote_text']:
            quote_elem = ET.SubElement(quotes_elem, 'quote')
            ET.SubElement(quote_elem, 'text').text = row['quote_text']
            ET.SubElement(quote_elem, 'page').text = row['page_block']
            ET.SubElement(quote_elem, 'comment').text = row['comment']
            ET.SubElement(quote_elem, 'tags').text = row['quote_tags']

    xml_str = ET.tostring(root, encoding='unicode', method='xml')
    return send_file(StringIO(xml_str).getvalue().encode('utf-8'), mimetype='application/xml', 
                     as_attachment=True, download_name=f'papers_{datetime.now().strftime("%Y%m%d")}.xml')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
