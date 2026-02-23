
C:\devData\work_2026\doc_annotation\
├── app.py (메인)
├── models.py (DB 모델)
├── routes/
│   ├── __init__.py
│   ├── main.py (메인 페이지)
│   ├── papers.py (논문 관리)
│   └── quotes.py (인용 관리)
├── html/ (기존 템플릿)
└── data/
    └── annotation.db

## 프로젝트 구조 개선
doc_annotation/
├── app.py
├── models.py
├── routes/
│   ├── __init__.py  ← **이 파일 핵심**
│   ├── main.py
│   ├── papers.py
│   └── quotes.py
├── html/
│   ├── base.html
│   ├── index.html
│   ├── add_paper.html
│   └── paper_info.html
└── data/
    └── annotation.db

## Blueprint 설정으로 라우팅 개선
#### Blueprint 사용 장단점
  -- 1. 코드 모듈화 & 구조화
  -- 2. URL Prefix 자동 관리
  -- 3. 독립적 개발/테스트

❌ 단일 app.py (1000줄+)
├── 모든 라우트 섞임
├── 수정 어려움

✅ Blueprint 분리
├── routes/main.py (홈, 내보내기)
├── routes/papers.py (논문 CRUD)
├── routes/quotes.py (인용 관리)
└── routes/auth.py (미래 인증)

### 2. URL Prefix 자동 관리
 -- *장점: /papers/add_paper, /quotes/delete/123 자동 생성

'''
## Blueprint 설정
papers_bp = Blueprint('papers', __name__, url_prefix='/papers')

#### 라우트 정의
@papers_bp.route('/add')  # 실제 URL: /papers/add
@papers_bp.route('/<id>') # 실제 URL: /papers/123
'''


### 3. 독립적 개발/테스트

'''
# 각 Blueprint 독립 테스트 가능
app.register_blueprint(papers_bp, url_prefix='/papers')

# papers_bp만 테스트
test_client = papers_bp.test_client()
'''

## 작성된 라우트
main.index
papers.paper_info
papers.add_paper
quotes.add_quote
quotes.delete_quote
main.export_xml


#####################################
# 1. 설치

cd C:\devData\work_2026\doc_annotation

# 1. 가상환경 생성/활성화
python -m venv venv
-- venv\Scripts\activate
.venv\Scripts\activate.bat


# 2. 패키지 설치
pip install flask

# 3. DB 초기화 (init_db.py 실행 또는 앱 첫 실행)
python -c "from models import init_db; init_db()"

# 4. 앱 실행
python app.py


########################################
## 특정 Python 버전 확인
python --version
where python

## pip 업그레이드
python -m pip install --upgrade pip

## 캐시 문제 해결
pip install flask --no-cache-dir


# 2. 파이썬 패키지 설치
(venv) PS C:\devData\work_2026\doc_annotation> python app.py
DB 경로: C:\devData\work_2026\doc_annotation\data\annotation.db
HTML 경로: C:\devData\work_2026\doc_annotation\html
 * Running on http://127.0.0.1:5000