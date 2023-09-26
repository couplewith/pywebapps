from urllib.parse import quote
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def url_encode(text):
    encoded_text = quote(text)
    return encoded_text

# 테스트
key_words = []
key_words.extend(["기술동향","디지털기술","인공지능","IT트렌드", "Trends", "디지털+트렌스포메이션", "Digital+Transformation"])
key_words.extend(["오늘의명언"])
key_words.extend(["빅데이터","database","블록체인","Data+mesh", "SQL", "SQLite"])
key_words.extend(["리눅스","셀스크립트","정규표현식","원도우+파일복구"])
key_words.extend(["블록체인","스마트컨트렉트","토큰증권","ERC-1400"])
key_words.extend(["selenium+기초","셀레니움", "Python","파이썬+프로그래밍기초","Rust+프로그래밍" ])

# WebDriver 초기화
driver = webdriver.Chrome()  # chromedriver 경로를 지정해야 합니다.

# 초기 윈도우를 2개 더 오픈 합니다.
driver.execute_script('window.open("about:blank", "_blank");')

driver.execute_script('window.open("about:blank", "_blank");')
tabs = driver.window_handles

print("start Search google", '->  open-browser tabs', len(tabs), tabs)

time.sleep(2)
url_lists = []
idx = 0
mode="search"  # "mode = [url, search]"

for keyword in key_words:

    encoded_keyword = url_encode(keyword)

    idx = idx + 1
    tabid = (idx % 3)
    driver.switch_to.window(driver.window_handles[tabid])

    if mode == 'url':

        search_url = f"https://www.google.com/search?q={encoded_keyword}+site%3Acouplewith.tistory.com&oq={encoded_keyword}+site%3Acouplewith.tistory.com&sourceid=chrome{idx}&ie=UTF-8"
        search_url = f"https://www.google.com/search?q={encoded_keyword}+site%3Acouplewith.tistory.com&sourceid=chrome{idx}&ie=UTF-8"

        driver.get(search_url)
        time.sleep(1)

    else:

        # Google .
        driver.get("https://www.google.com")

        # Google 검색어 입력란을 찾습니다.
        search_box = driver.find_element(By.NAME, "q")

        # 검색어를 입력합니다.
        search_query = f"{keyword} site:couplewith.tistory.com"
        search_box.send_keys(search_query)

        # 검색을 실행합니다.
        search_box.send_keys(Keys.RETURN)
        time.sleep(1)

    try:

        # 검색 결과 링크 가져오기
        # #rso > div:nth-child(1) > div > div > div > div > div > span > a
        # CSS PATH : #rso > div:nth-child(1) > div > div > div > div > a
        # Xpath : //*[@id="rso"]/div[2]/div/div/div[1]/div/div/span/a
        # // XPath 표현식은 ID가 "rso"인 모든 /div 요소를 선택한다.

        links = driver.find_elements(By.XPATH, '//*[@id="rso"]//div//a')
        print( " >> search result find links", len(links))

        for link in links:
            url = link.get_attribute('href')
            attr = link.get_attribute('text')
            url_lists.append({"url": url, "attr": attr, "keyword" : keyword})

        print(" -> ", keyword, len(url_lists))

    except NoSuchElementException:
        print(">  NoSuchElementException ", search_url)


#
print(" -> url_lists ", len(url_lists), url_lists)
# URL 리스트 출력
#  url_lists[ [url, attr, keyword],... ]
idx = 0

for url in url_lists:
    
    idx = idx + 1

    tabid = (idx % 3)
    driver.switch_to.window(driver.window_handles[tabid])
    print(idx, tabid, url)

    driver.get(url['url'])
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

# WebDriver 종료
driver.quit()
