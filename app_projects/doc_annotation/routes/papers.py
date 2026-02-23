from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Paper, Quote

# Blueprint 생성 (url_prefix 없이)
papers_bp = Blueprint('papers', __name__)


@papers_bp.route('/papers/add', methods=['GET', 'POST'])
def add_paper():
    """새 논문 추가"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        
        # 필수 필드 검증
        if not title:
            flash('제목은 필수입니다.')
            return render_template('add_paper.html')
        
        # 논문 생성
        try:
            paper_id = Paper.create(
                title=title,
                authors=request.form.get('authors', ''),
                year=request.form.get('year', None, type=int),
                journal=request.form.get('journal', ''),
                apa_citation=request.form.get('apa_citation', ''),
                abstract=request.form.get('abstract', ''),
                abstract_ko=request.form.get('abstract_ko', ''),
                paper_tags=request.form.get('paper_tags', '')
            )
            flash('✅ 논문이 추가되었습니다.')
            return redirect(url_for('papers.paper_info', paper_id=paper_id))
        except Exception as e:
            flash(f'❌ 논문 추가 실패: {str(e)}')
            return render_template('add_paper.html')
    
    return render_template('add_paper.html')


@papers_bp.route('/papers/<int:paper_id>')
def paper_info(paper_id):
    """논문 상세 정보 및 인용 목록"""
    paper = Paper.get_by_id(paper_id)
    
    if not paper:
        flash('❌ 논문을 찾을 수 없습니다.')
        return redirect(url_for('main.index'))
    
    quotes = Quote.get_by_paper(paper_id)
    return render_template('paper_info.html', paper=paper, quotes=quotes)


@papers_bp.route('/papers/edit/<int:paper_id>', methods=['GET', 'POST'])
def edit_paper(paper_id):
    """논문 수정 (선택적 기능)"""
    paper = Paper.get_by_id(paper_id)
    
    if not paper:
        flash('❌ 논문을 찾을 수 없습니다.')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('제목은 필수입니다.')
            return render_template('edit_paper.html', paper=paper)
        
        # 논문 업데이트 (models.py에 Paper.update 추가 필요)
        try:
            Paper.update(
                paper_id,
                title=title,
                authors=request.form.get('authors', ''),
                year=request.form.get('year', None, type=int),
                journal=request.form.get('journal', ''),
                apa_citation=request.form.get('apa_citation', ''),
                abstract=request.form.get('abstract', ''),
                abstract_ko=request.form.get('abstract_ko', ''),
                paper_tags=request.form.get('paper_tags', '')
            )
            flash('✅ 논문이 수정되었습니다.')
            return redirect(url_for('papers.paper_info', paper_id=paper_id))
        except Exception as e:
            flash(f'❌ 수정 실패: {str(e)}')
    
    return render_template('edit_paper.html', paper=paper)


@papers_bp.route('/papers/delete/<int:paper_id>')
def delete_paper(paper_id):
    """논문 삭제 (선택적 기능)"""
    try:
        Paper.delete(paper_id)  # models.py에 Paper.delete 추가 필요
        flash('✅ 논문이 삭제되었습니다.')
    except Exception as e:
        flash(f'❌ 삭제 실패: {str(e)}')
    
    return redirect(url_for('main.index'))
