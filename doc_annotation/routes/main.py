from flask import Blueprint, render_template, request, send_file
from models import Paper, get_db
import xml.etree.ElementTree as ET
from io import BytesIO
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    search = request.args.get('search', '')
    tags = request.args.get('tags', '').strip()
    papers = Paper.get_all(search, tags)
    return render_template('index.html', papers=papers, search=search, tags=tags)

@main_bp.route('/export_xml')
def export_xml():
    conn = get_db()
    rows = conn.execute('''
        SELECT p.*, q.quote_text, q.page_block, q.comment, q.annotation_tags as quote_tags
        FROM doc_papers p LEFT JOIN doc_quotes q ON p.id = q.paper_id ORDER BY p.id
    ''').fetchall()
    conn.close()

    root = ET.Element('papers')
    current_paper = None
    paper_elem = None
    quotes_elem = None
    
    for row in rows:
        if current_paper != row['id']:
            current_paper = row['id']
            paper_elem = ET.SubElement(root, 'paper', id=str(row['id']))
            ET.SubElement(paper_elem, 'title').text = row['title'] or ''
            ET.SubElement(paper_elem, 'authors').text = row['authors'] or ''
            ET.SubElement(paper_elem, 'year').text = str(row['year']) if row['year'] else ''
            ET.SubElement(paper_elem, 'journal').text = row['journal'] or ''
            ET.SubElement(paper_elem, 'apa_citation').text = row['apa_citation'] or ''
            ET.SubElement(paper_elem, 'abstract').text = row['abstract'] or ''
            ET.SubElement(paper_elem, 'abstract_ko').text = row['abstract_ko'] or ''
            ET.SubElement(paper_elem, 'paper_tags').text = row['paper_tags'] or ''
            quotes_elem = ET.SubElement(paper_elem, 'quotes')
        
        if row['quote_text']:
            quote_elem = ET.SubElement(quotes_elem, 'quote')
            ET.SubElement(quote_elem, 'text').text = row['quote_text']
            ET.SubElement(quote_elem, 'page').text = row['page_block'] or ''
            ET.SubElement(quote_elem, 'comment').text = row['comment'] or ''
            ET.SubElement(quote_elem, 'tags').text = row['quote_tags'] or ''

    xml_bytes = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    return send_file(
        BytesIO(xml_bytes),
        mimetype='application/xml',
        as_attachment=True,
        download_name=f'papers_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xml'
    )
