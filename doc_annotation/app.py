from flask import Flask
import os

BASE_PATH = r'C:\devData\work_2026\doc_annotation'
HTML_PATH = os.path.join(BASE_PATH, 'html')
STATIC_PATH = os.path.join(BASE_PATH, 'static')

app = Flask(__name__, 
            template_folder=HTML_PATH,
            static_folder=STATIC_PATH)
app.secret_key = 'dev_annotation_secret_2026'

# DB 초기화
from models import init_db
with app.app_context():
    init_db()

# Blueprint 등록 (url_prefix 제거)
try:
    from routes.main import main_bp
    from routes.papers import papers_bp
    from routes.quotes import quotes_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(papers_bp)  # ✅ url_prefix 없음
    app.register_blueprint(quotes_bp)
    print("✅ Blueprint 등록 완료")
except ImportError as e:
    print(f"⚠️ Blueprint import 오류: {e}")

if __name__ == '__main__':
    print("=== 논문 인용 관리 앱 ===")
    print(f"DB: {os.path.join(BASE_PATH, 'data', 'annotation.db')}")
    print(f"Templates: {HTML_PATH}")
    print("접속: http://127.0.0.1:5000")
    print("========================")
    app.run(debug=True, host='127.0.0.1', port=5000)
