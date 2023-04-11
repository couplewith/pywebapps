import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# SSL 인증서 무시
#response = requests.get('https://example.com', verify=False)

# 크롤링할 사이트 URL
url = 'http://news.naver.com/main/hotissue/sectionList.nhn?mid=hot&sid1=102&cid=1070665'

# requests 모듈을 이용해 웹 페이지 요청
response = requests.get(url,verify=False)

# 요청에 실패한 경우 예외 처리
if response.status_code != 200:
    print('요청 실패')
    exit()

# BeautifulSoup4 모듈을 이용해 HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 각 뉴스 기사에 대한 링크를 가져오기 위해 CSS 선택자 사용
links = soup.select('.issue .issue_list li a')

# 링크와 함께 해당 기사 제목 출력
for link in links:
    print(link['href'], link.text)
