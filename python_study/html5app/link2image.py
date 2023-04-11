import requests
from flask import Flask, request, send_file

app = Flask(__name__)

# CORS 설정
@app.after_request
def set_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# 이미지 생성 엔드포인트
@app.route('/image/<path:link>')
def generate_image(link):
    api_url = f'https://api.microlink.io/?url={link}&screenshot=true'
    response = requests.get(api_url)
    return send_file(
        io.BytesIO(response.content),
        mimetype='image/png',
        as_attachment=False,
        attachment_filename='screenshot.png'
    )

# 서버 시작
if __name__ == '__main__':
    app.run(debug=True, port=3000)
