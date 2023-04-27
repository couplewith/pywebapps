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

# url = 'https://exampleblog.com'  # 크롤링할 블로그 주소
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
#
# posts = []
# for post in soup.find_all('div', {'class': 'post'}):  # 블로그 게시글 영역에 해당하는 div 태그의 class명
#     title = post.find('h2', {'class': 'post-title'}).text.strip()  # 게시글 제목
#     content = post.find('div', {'class': 'post-content'}).text.strip()  # 게시글 내용
#     posts.append((title, content))
#
# print(posts)

posts = [
    {'title': '제<html> <a href="adfadf.cadfl.com" alt="안ㄹ드리" >목1</a>', 'content': '내용1'},
    {'title': '제목2', 'content': '내용2'},
    {'title': '제목3', 'content': '내용3'}
]
json_save(posts)

