from flask import Blueprint, request, redirect, url_for, flash
from models import Quote

quotes_bp = Blueprint('quotes', __name__, url_prefix='/quotes')

@quotes_bp.route('/add/<int:paper_id>', methods=['POST'])
def add_quote(paper_id):
    quote_text = request.form.get('quote_text', '').strip()
    if not quote_text:
        flash('인용문은 필수입니다.')
    else:
        Quote.create(
            paper_id,
            quote_text,
            request.form.get('page_block', ''),
            request.form.get('comment', ''),
            request.form.get('annotation_tags', '')
        )
        flash('인용이 추가되었습니다.')
    return redirect(url_for('papers.paper_info', paper_id=paper_id))

@quotes_bp.route('/delete/<int:quote_id>')
def delete_quote(quote_id):
    paper_id = Quote.delete(quote_id)
    flash('인용이 삭제되었습니다.')
    return redirect(url_for('papers.paper_info', paper_id=paper_id))
