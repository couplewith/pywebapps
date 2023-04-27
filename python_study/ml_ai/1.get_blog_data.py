import requests
from bs4 import BeautifulSoup
import json

def json_save(list_data, file_name = 'posts_list.json'):

    # JSON 파일로 저장하기
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(list_data, f, ensure_ascii=False)
    print('저장 완료', file_name)

def json_read( file_name = 'posts_list.json'):
    # JSON 파일에서 데이터 읽어오기
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


url = 'https://exampleblog.com'  # 크롤링할 블로그 주소
url = 'https://couplwith.tistory.com'  # 크롤링할 블로그 주소
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')

posts = []
# for post in soup.find_all('div', {'class': 'post'}):  # 블로그 게시글 영역에 해당하는 div 태그의 class명
#     title = post.find('h2', {'class': 'post-title'}).text.strip()  # 게시글 제목
#     content = post.find('div', {'class': 'post-content'}).text.strip()  # 게시글 내용
#     posts.append((title, content))

# tistory.com
for post in soup.find_all('div', {'class': 'article'}):  # 블로그 게시글 영역에 해당하는 div 태그의 class명
    title = post.find('h2', {'class': 'tit_post'}).text.strip()  # 게시글 제목
    content = post.find('div', {'class': 'area_view'}).text.strip()  # 게시글 내용
    posts.append((title, content))


print(posts)
json_save(posts)

