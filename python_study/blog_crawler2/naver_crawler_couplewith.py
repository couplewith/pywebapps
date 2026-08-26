from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re


def url_encode(text):
    return quote(text)


# 1. 검색 키워드 설정
key_words = []
key_words.extend(["인공지능","AI비즈니스","AI&Tech","AI 에이전트","AI챗봇","RAG","자가진화"])
key_words.extend(["디지털","퀀텀 양자","IT트렌드", "디지털혁신", "디지털+트렌스포메이션", "Digital+Transformation"])
key_words.extend(["오늘의명언","명언","전략기획","경영전략","성공 전략"])
key_words.extend(["빅데이터","database","블록체인","Data+mesh", "SQL", "SQLite"])
key_words.extend(["리눅스", "Linux 튜닝", "WSL", "Docker","셀스크립트","정규표현식","원도우+파일복구"])
key_words.extend(["파이썬", "개발방법론","언어","GO", "Rust","프로그래밍"])
key_words.extend(["블록체인","스마트컨트렉트","토큰 증권 STO","ERC-1400","Truffle"])
key_words.extend(["암호화","보안"])
key_words.extend(["selenium+기초","셀레니움","테스트", "테스트 자동화" ])
key_words.extend(["금융","증권","투자","주식"])

# WebDriver 초기화
driver = webdriver.Chrome()
driver.implicitly_wait(5)

try:
    # 7-8. 키워드 전체 순회
    for keyword in key_words:
        blog_name ="couplewith.tistory.com"
        encoded_keyword = url_encode(keyword)
        ackey="24zxtz2s"
        # 네이버 블로그 검색 URL
        #search_url = f"https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=site%3Ablog.naver.com%2Fwinrae++{encoded_keyword}"
        # https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=site%3A+couplewith.tistory.com++AI
        search_url = f"https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=site%3A+{blog_name}++{encoded_keyword}"

        # 1. 블로그 검색 페이지 이동
        driver.get(search_url)
        time.sleep(2)
        print(f"\n[+] 키워드 검색 진행 중: '{keyword}'")

        # 2. 검색 결과에서 blog_name 게시글 목록 수집
        post_links = []
        blog_elements = driver.find_elements(By.XPATH, f'//a[contains(@href, "{blog_name}/")]')

        # couplewith.tistory.com/숫자 형태만 추출하는 정규표현식 Pattern
        pattern = re.compile(rf'https?://{blog_name}\.tistory\.com/\d+/?$')

        for elem in blog_elements:
            url = elem.get_attribute('href')
            # 중복 및 단순 프로필/블로그 홈 링크 제외
            if url and url not in post_links and ("Redirect=Log" in url or blog_name in url):
                post_links.append(url)

        print(f" -> 수집된 게시글 수: {len(post_links)}개")

        # 3-5. 게시글 목록 하나씩 순회
        for idx, post_url in enumerate(post_links):
            print(f"  [{idx + 1}/{len(post_links)}] 게시글 이동: {post_url}")

            # 3. 각 게시글로 이동
            driver.get(post_url)
            time.sleep(2)

            # 네이버 블로그 iframe 구조 처리   #mainFrame : 네이버 전용창
            try:
                # 수정 코드: URL 조건에 따라 프레임 전환
                current_url = driver.current_url

                if "blog.naver.com" in current_url:
                    try:
                        driver.switch_to.frame("mainFrame")
                    except NoSuchFrameException:
                        pass
                else:
                    # 티스토리 등 외부 블로그는 iframe 전환 없이 메인 컨텍스트 유지
                    driver.switch_to.default_content()
            except NoSuchElementException:
                pass

            # 3. 화면을 아래로 30% 스크롤
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
            time.sleep(1.5)

            # 4. 이전의 검색 화면으로 이동 (검색 URL로 다시 로드)
            driver.get(search_url)
            time.sleep(1.5)

# 8. 모든 키워드 검색 완료 시 종료
finally:
    print("\n[+] 모든 키워드 조회가 완료되어 브라우저를 종료합니다.")
    driver.quit()