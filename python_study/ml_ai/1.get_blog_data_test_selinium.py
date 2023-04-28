from selenium import webdriver
from lxml import html
import requests
from py2neo import Graph, Node, Relationship



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

# 웹드라이버 설정
driver = webdriver.Chrome("chromedriver.exe")

# 블로그 URL 설정
url = "https://couplewith.tistory.com/400"

# 블로그 페이지 로드
driver.get(url)

# 페이지 소스 가져오기
page = driver.page_source

# lxml parser로 HTML 파싱
tree = html.fromstring(page)

# 제목 가져오기
title = tree.xpath('//title/text()')[0]

# URL 저장
url_node = Node("URL", name=url)

# 내용 가져오기
content = tree.xpath('//div[@class="content"]')[0]
content_text = content.text_content()

# HTML 태그 제거
clean_content = html.fromstring(content_text).text_content()

# 키워드 추출
r = requests.get('https://api.datamuse.com/words?ml=' + clean_content)
json_data = r.json()
keywords = [i['word'] for i in json_data]

print(keywords)

# # GraphDB 연결 설정
# graph = Graph("http://localhost:7474/db/data/", auth=("username", "password"))
#
# # 노드 생성
# post_node = Node("Post", title=title, content=clean_content)
# graph.create(post_node)
#
# # URL 노드 연결
# rel_url = Relationship(post_node, "HAS_URL", url_node)
# graph.create(rel_url)
#
# # 키워드 노드 생성 및 연결
# keyword_nodes = []
# for keyword in keywords:
#     keyword_node = Node("Keyword", name=keyword)
#     graph.create(keyword_node)
#     keyword_nodes.append(keyword_node)
#     rel_keyword = Relationship(post_node, "HAS_KEYWORD", keyword_node)
#     graph.create(rel_keyword)
#
#
#
# posts = [
#     {'title': '제<html> <a href="adfadf.cadfl.com" alt="안ㄹ드리" >목1</a>', 'content': '내용1'},
#     {'title': '제목2', 'content': '내용2'},
#     {'title': '제목3', 'content': '내용3'}
# ]
# json_save(posts)

