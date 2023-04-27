import re
import json

# 2 전처리
# 수집한 데이터를 전처리하여 분석에 적합한 형태로 가공
# 예를 들어, HTML 태그 제거, 특수문자 제거, 대소문자 통일 등의 과정

def clean_text(text):
    # HTML 태그 제거
    clean = re.compile('<.*?>', re.UNICODE)  # 패턴을 Unicode로 지정
    text = re.sub(clean, '',text)
    print('clean_text', text)
    # 특수문자 제거
    #text = re.sub('[^A-Za-z0-9]+', ' ', text)
    text = re.sub('[^A-Za-z0-9가-힣]+', ' ', text)  # 특수문자 중에서도 한글은 유니코드로 지정
    # 대소문자 통일
    text = text.lower()
    return text

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



cleaned_posts = []

posts = json_read('posts_list.json')

print(posts)
for post in posts:
    print( '>start', post['title'], post['content'])
    title = clean_text(post['title'])
    content = clean_text(post['content'])
    cleaned_posts.append({"title": title, "content": content})

print(cleaned_posts)

json_save(cleaned_posts, 'posts_list_clean.json')
