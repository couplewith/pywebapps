from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
import time

def url_encode(text):
    encoded_text = quote(text)
    return encoded_text

# 테스트
key_words = ['블록체인','셀스크립트', '인공지능', '데이터','리눅스','프로그래밍','정규표현식','원도우복구','파이썬','Rust', 'selenium', 'data','디지털']
key_words = ['기술동향','디지털기술','인공지능','오늘의명언','빅데이터','database','블록체인', '리눅스','셀스크립트','프로그래밍','정규표현식','원도우복구','파이썬','Rust', 'selenium']

# WebDriver 초기화
driver = webdriver.Chrome()  # chromedriver 경로를 지정해야 합니다.

# 초기 윈도우를 2개 더 오픈 합니다.
driver.execute_script('window.open("about:blank", "_blank");')
driver.execute_script('window.open("about:blank", "_blank");')
tabs = driver.window_handles

print('tabs', len(tabs), tabs)

time.sleep(2)
url_lists = []
for keyword in key_words:
    encoded_keyword = url_encode(keyword)
    search_url = f"https://www.google.com/search?q={encoded_keyword}+site%3Acouplewith.tistory.com&oq={encoded_keyword}+site%3Acouplewith.tistory.com&sourceid=chrome&ie=UTF-8"
    driver.switch_to.window(driver.window_handles[0])
    driver.get(search_url)
    print(search_url)

    try:
        # 검색 결과 링크 가져오기
        # #rso > div:nth-child(1) > div > div > div > div > a
        links = driver.find_elements(By.XPATH, '//*[@id="rso"]/div//div[1]/div/a')
        print (len(links))

        for link in links:
            url = link.get_attribute('href')
            attr = link.get_attribute('text')
            url_lists.append({"url": url, "attr": attr})


    except NoSuchElementException:
        print(">  NoSuchElementException ", search_url)


# URL 리스트 출력
idx = 0

for url in url_lists:
    print(url)
    idx = idx + 1

    if ( (idx % 2 ) == 1):
        driver.switch_to.window(driver.window_handles[1])
        print(idx, 1)
    else:
        driver.switch_to.window(driver.window_handles[2])
        print(idx, 2)
    driver.get(url['url'])

    # 페이지를 키워드로 스크롤 합니다.
    for c in range(0, 5):
        driver.find_element( By.TAG_NAME, value='body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    # 페이지를 하단으로 스크롤 합니다.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# WebDriver 종료
driver.quit()
