import random
import re
import time
from urllib.parse import quote

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def url_encode(text):
    return quote(text)


# 1. 사용자 정보 가상화를 위한 랜덤 User-Agent 리스트 정의
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
]

# 2. Chrome Options 설정 (보안/개인정보 및 자동화 탐지 방지)
chrome_options = Options()

# 자동화 감지 플래그 제거 및 시크릿 모드 설정
chrome_options.add_argument("--incognito")  # 시크릿 모드로 쿠키/방문기록 남기지 않음
chrome_options.add_argument(
    f"user-agent={random.choice(USER_AGENTS)}"
)  # 랜덤 User-Agent 설정
chrome_options.add_argument(
    "--disable-blink-features=AutomationControlled"
)  # 셀레니움 감지 방지
chrome_options.add_experimental_option(
    "excludeSwitches", ["enable-automation"]
)  # 자동화 제어 알림창 제거
chrome_options.add_experimental_option("useAutomationExtension", False)

# 무작위 창 크기 설정 (화면 해상도 핑거프린팅 방지)
window_sizes = [(1366, 768), (1440, 900), (1920, 1080), (1536, 864)]
selected_size = random.choice(window_sizes)

# WebDriver 초기화
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(selected_size[0], selected_size[1])

# CDP(Chrome DevTools Protocol)를 통해 navigator.webdriver = false 강제 적용
driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
    """
    },
)

driver.implicitly_wait(5)

# 검색 키워드 설정 (중복 제거 및 정리)
key_words = list(
    set([
        "AI",
        "LLM",
        "Agent",
        "인공지능",
        "AI비즈니스",
        "AI&Tech",
        "에이전트",
        "AI챗봇",
        "RAG",
        "자가진화",
        "디지털",
        "퀀텀",
        "양자",
        "IT트렌드",
        "디지털혁신",
        "트렌스포메이션",
        "오늘의명언",
        "좋은글",
        "명언",
        "전략기획",
        "경영전략",
        "성공",
        "빅데이터",
        "database",
        "블록체인",
        "데이터베이스",
        "SQL",
        "DBMS",
        "리눅스",
        "Linux",
        "Docker",
        "WSL",
        "시스템",
        "오픈소스",
        "셀스크립트",
        "정규표현식",
        "정규식",
        "파일복구",
        "파이썬",
        "개발방법론",
        "언어",
        "GO",
        "Rust",
        "프로그래밍",
        "가이드",
        "selenium+기초",
        "셀레니움",
        "테스트 자동화",
        "Python",
        "파이썬+프로그래밍기초",
        "Rust+프로그래밍",
        "스마트컨트렉트",
        "토큰증권",
        "스테이블코인",
        "암호화",
        "보안",
        "금융",
        "증권",
        "투자",
        "주식",
    ])
)

try:
    for keyword in key_words:
        blog_name = "couplewith.tistory.com"
        encoded_keyword = url_encode(keyword)
        #search_url = f"https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=site%3A+{blog_name}++{encoded_keyword}"
        search_url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={encoded_keyword}++site%3A{blog_name}&ackey=64g1dxrk"
        # 1. 블로그 검색 페이지 이동
        driver.get(search_url)
        time.sleep(random.uniform(2.0, 3.5))  # 고정 대기 대신 랜덤 대기 적용
        print(f"\n[+] 키워드 검색 진행 중: '{keyword}'")

        # 2. 검색 결과 수집
        post_links = []
        blog_elements = driver.find_elements(
            By.XPATH, f'//a[contains(@href, "{blog_name}")]'
        )

        for elem in blog_elements:
            url = elem.get_attribute("href")
            if url and url not in post_links:
                post_links.append(url)

        print(f" -> 수집된 게시글 수: {len(post_links)}개")

        # 3. 게시글 순회
        for idx, post_url in enumerate(post_links):
            print(
                f"  [{idx + 1}/{len(post_links)}] 게시글 이동: {post_url}"
            )

            driver.get(post_url)
            time.sleep(random.uniform(1.8, 3.0))

            # iframe 처리 (NoSuchFrameException 예외 처리 추가)
            try:
                current_url = driver.current_url
                if "blog.naver.com" in current_url:
                    driver.switch_to.frame("mainFrame")
                else:
                    driver.switch_to.default_content()
            except (NoSuchElementException, NoSuchFrameException):
                pass

            # 사람처럼 부드럽게 랜덤 스크롤
            scroll_location = random.uniform(0.2, 0.5)
            driver.execute_script(
                f"window.scrollTo(0, document.body.scrollHeight * {scroll_location});"
            )
            time.sleep(random.uniform(1.0, 2.5))

            # 검색 페이지로 돌아가기
            driver.get(search_url)
            time.sleep(random.uniform(1.0, 2.0))

finally:
    print("\n[+] 모든 키워드 조회가 완료되어 브라우저를 종료합니다.")
    driver.quit()

# '''
# 시크릿 모드(--incognito) 설정:

# 기존 방문 기록, 탭 쿠키, 개인 핑거프린트 데이터를 완전히 차단하여 새로운 세션처럼 접속합니다.

# 크롤링 감지 변수(navigator.webdriver) 제거:

# 네이버 등의 사이트는 navigator.webdriver == true인 경우 매크로로 간주하고 캡차(CAPTCHA)를 띄웁니다. CDP 스크립트를 통해 이를 undefined로 우회했습니다.

# User-Agent 및 해상도 무작위화:

# 매 실행 시 OS 및 브라우저 버전(User-Agent)과 브라우저 창 크기를 무작위로 변경하여 고정된 디바이스로 추적되는 것을 방지했습니다.

# 패턴 감지 방지를 위한 random.uniform() 도입:

# time.sleep(2)처럼 정확하게 일정한 시간 간격으로 요청을 보내면 알고리즘에 의해 자동화 도구로 차단될 위험이 높습니다. 요청 및 스크롤 동작 간격을 무작위 실수 형태로 지정했습니다.
# '''