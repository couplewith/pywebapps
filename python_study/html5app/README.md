먼저, Flask와 requests 모듈을 설치합니다.
bash
Copy code
pip install Flask requests
다음과 같이 서버를 구성합니다.
python
Copy code
from flask import Flask, request, Response
import requests

app = Flask(__name__)

# CORS 설정
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response

# 이미지 생성 엔드포인트
@app.route('/image/<path:link>')
def generate_image(link):
    api_url = f'https://api.microlink.io/?url={link}&screenshot=true'
    response = requests.get(api_url)
    image = response.content
    return Response(image, mimetype='image/png')

# 서버 시작
if __name__ == '__main__':
    app.run(debug=True)


클라이언트 측의 HTML 파일을 다음과 같이 수정합니다.

서버 측 코드가 Flask로 작성된 것을 고려하여, 클라이언트 측 코드도 이와 연동되도록 작성해 보겠습니다. index.html 파일을 다음과 같이 작성합니다.

html
Copy code
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>웹 페이지 링크 이미지 생성기</title>
    <style>
      /* 스타일 설정 */
      body {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
      }
      form {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
      }
      label {
        margin-bottom: 10px;
        font-size: 1.2rem;
        font-weight: bold;
      }
      input[type="text"] {
        margin-bottom: 20px;
        padding: 5px;
        font-size: 1.2rem;
        border: 2px solid #ccc;
        border-radius: 5px;
        width: 400px;
        max-width: 100%;
      }
      button {
        padding: 10px 20px;
        font-size: 1.2rem;
        font-weight: bold;
        color: #fff;
        background-color: #007bff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.2s ease-in-out;
      }
      button:hover {
        background-color: #0062cc;
      }
      img {
        margin-top: 20px;
        max-width: 100%;
      }
    </style>
  </head>
  <body>
    <!-- 입력 폼 -->
    <form id="link-form">
      <label for="link-input">링크 주소:</label>
      <input type="text" id="link-input" name="link" placeholder="https://example.com">
      <button type="submit">이미지 생성</button>
    </form>

    <!-- 이미지 -->
    <div id="image-container"></div>

    <!-- 자바스크립트 -->
    <script>
      const form = document.querySelector('#link-form');
      const imageContainer = document.querySelector('#image-container');

      form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const linkInput = document.querySelector('#link-input');
        const link = encodeURIComponent(linkInput.value);

        try {
          const response = await fetch(`http://localhost:5000/image/${link}`);

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          const imageBlob = await response.blob();

          const img = document.createElement('img');
          img.src = URL.createObjectURL(imageBlob);

          imageContainer.innerHTML = '';
          imageContainer.appendChild(img);
        } catch (error) {
          console.error(error);
          alert('이미지를 가져올 수 없습니다.');
        }
      });
    </script>
  </body>
</html>
위 코드에서 <script> 태그 내부에 작성된 자바스크립트 코드는, link-form 폼에서 제출 이벤트가 발생했을 때 fetch() 메서드를 사용하여 서버로 이미지를 요청하고, 서버에서