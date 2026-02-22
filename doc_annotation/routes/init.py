from flask import Blueprint
main_bp = Blueprint('main', __name__)
papers_bp = Blueprint('papers', __name__)
quotes_bp = Blueprint('quotes', __name__)
from .main import *
from .papers import *
from .quotes import *
def register_blueprints(app):
    """app.py에서 호출하여 Blueprint 등록"""
    app.register_blueprint(main_bp)
    app.register_blueprint(papers_bp)
    app.register_blueprint(quotes_bp)
    print("✅ 모든 Blueprint 등록 완료")
    print(f"  - main_bp: {main_bp.name}")
    print(f"  - papers_bp: {papers_bp.name}")
    print(f"  - quotes_bp: {quotes_bp.name}")  