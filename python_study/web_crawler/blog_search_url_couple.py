from urllib.parse import quote
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
import time

def url_encode(text):
    encoded_text = quote(text)
    return encoded_text

# 테스트
key_words=["파일복구","Rust 프로그래밍", "셀스크립트 작성", "빅데이터", "인공지능", "IT 트렌드", "Trends", "디지털 트렌스포메이션", "Digital Transformation", "Data mesh", "셀레니움", "파이썬", "SQL", "SQLite"]

# WebDriver 초기화
driver = webdriver.Chrome()  # chromedriver 경로를 지정해야 합니다.

# 초기 윈도우를 2개 더 오픈 합니다.
driver.execute_script('window.open("about:blank", "_blank");')git

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

# WebDriver 종료
driver.quit()
