
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import string
import random
from concurrent.futures import ThreadPoolExecutor

# 랜덤한 AD ID 생성 함수
def generate_random_ad_id(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def get_chrome_driver_with_custom_user_agent(ad_id):
    options = webdriver.ChromeOptions()
    
    # Custom user agent with Google ad-id
    user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3 (Google ad-id={ad_id})"
    
    # Adding custom user agent to Chrome options
    options.add_argument(f'user-agent={user_agent}')
    
    # Initialize the driver with the custom user agent
    driver = webdriver.Chrome(options=options)
    return driver

def crawl_webpage(driver, url):

    try:
        driver.get(url)

        # 페이지 로딩 대기 (최대 10초)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # 스크롤링 (30라인씩 아래로 이동)
        for _ in range(3):  # 3번 스크롤
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(1)  # 스크롤 간 간격 (1초)
            driver.execute_script("window.scrollBy(0, -400);")
            time.sleep(1)  # 스크롤 간 간격 (1초)
        
        # mobile 좋아요 버튼 클릭 (조건에 맞게 클릭)
        buttons = driver.find_elements(By.CLASS_NAME, "btn_like")
        for button in buttons:
            if "on" not in button.get_attribute("class"):
                button.click()
                print(f"<<<m클릭: 좋아용")
                break
        # Web 좋아요 버튼 클릭 (조건에 맞게 클릭)
        buttons = driver.find_elements(By.CLASS_NAME, "uoc-icon")
        for button in buttons:
            if "like_on" not in button.get_attribute("class"):
                button.click()
                print(f">>>w클릭: 좋아용")
                break 




        # 페이지 전체 내용 가져오기
        html = driver.page_source

        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(html, 'html.parser')

        # 제목 추출
        title = soup.title.string if soup.title else "제목 없음"

        # 내용 추출 (body 태그 내의 텍스트)
        content = soup.body.get_text(strip=True) if soup.body else "내용 없음"

        # 키워드 추출 (meta 태그에서 keywords 추출)
        keywords = soup.find('meta', attrs={'name': 'keywords'})['content'] if soup.find('meta', attrs={'name': 'keywords'}) else "키워드 없음"

        # 결과 출력
        print(f"URL: {url}")
        print(f"제목: {title}")
        print(f"내용: {content}")
        print(f"키워드: {keywords}")
        print("-" * 20)  # 페이지별 구분선 추가

    except Exception as e:
        print(f"오류: {e}")
    finally:
        print(f">>>crawl_webpage : Done :: {url}")
    #    driver.quit()

def sitemap_search(sitemap_url):
    global driver1, driver2, driver3  # 전역 변수 사용 선언
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml-xml')

        urls = [loc.text for loc in soup.find_all('loc')]

        # Shuffle the list
        # 순서를 Random하게 섞습니다.
        random.shuffle(urls)

        # ThreadPoolExecutor를 사용하여 병렬 처리
        with ThreadPoolExecutor(max_workers=3) as executor:
            ad_ids = [generate_random_ad_id() for _ in range(3)]
            for i, url in enumerate(urls):
                if i % 2 == 0:
                    #crawl_webpage(driver1, url)
                    executor.submit(crawl_webpage, driver1, url) # 1 번째 탭에서 크롤링
                elif i % 3 == 1 :
                    executor.submit(crawl_webpage, driver2, url) # 2 번째 탭에서 크롤링
                else:
                    executor.submit(crawl_webpage, driver3, url) # 3 번째 탭에서 크롤링

    except requests.exceptions.RequestException as e:
        print(f"오류: {e}")
    except AttributeError as e:
        print(f"오류: {e}")
    except TypeError as e:
        print(f"오류: {e}")

########################


        # 웹 드라이버 초기화 (Chrome 사용) - headless 옵션 제거
random_ad_id = generate_random_ad_id()
driver1 = get_chrome_driver_with_custom_user_agent(random_ad_id) # 첫 번째 탭용 드라이버

random_ad_id = generate_random_ad_id()
driver2 = get_chrome_driver_with_custom_user_agent(random_ad_id)  # 두 번째 탭용 드라이버

random_ad_id = generate_random_ad_id()
driver3 = get_chrome_driver_with_custom_user_agent(random_ad_id)  # 두 번째 탭용 드라이버



# Sitemap URL
sitemap_urls = ["https://sweeting.tistory.com/sitemap.xml","https://couplewith.tistory.com/sitemap.xml","https://smartbus.tistory.com/sitemap.xml"]
#sitemap_url = "https://sweeting.tistory.com/sitemap.xml"
#sitemap_url = "https://couplewith.tistory.com/sitemap.xml"
for sitemap_url in sitemap_urls:
    sitemap_search(sitemap_url)
