"""
Routes Blueprint 초기화 모듈
모든 Blueprint 인스턴스를 여기서 생성하고 import
"""
from flask import Blueprint

main_bp = Blueprint('main', __name__)
papers_bp = Blueprint('papers', __name__)
quotes_bp = Blueprint('quotes', __name__)


# 각 서브모듈에서 정의된 라우트들을 import
# 이 순서가 중요: Blueprint 정의 후 import
from .main import *
from .papers import *
from .quotes import *

# 등록 확인 로그 (선택사항)
def register_blueprints(app):
    """app.py에서 호출하여 Blueprint 등록"""
    app.register_blueprint(main_bp)
    app.register_blueprint(papers_bp)
    app.register_blueprint(quotes_bp)
    print("✅ 모든 Blueprint 등록 완료")
    print(f"  - main_bp: {main_bp.name}")
    print(f"  - papers_bp: {papers_bp.name}")
    print(f"  - quotes_bp: {quotes_bp.name}")
