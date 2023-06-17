from urllib.parse import quote
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

def url_encode(text):
    encoded_text = quote(text)
    return encoded_text

# 테스트
key_words = ['경기도근처카페', '경기도가볼만한곳', '베이커리카페', '당일여행']

# WebDriver 초기화
driver = webdriver.Chrome()  # chromedriver 경로를 지정해야 합니다.

url_lists = []
for keyword in key_words:
    encoded_keyword = url_encode(keyword)
    search_url = f"https://www.google.com/search?q={encoded_keyword}+site%3Asweeting.tistory.com&oq={encoded_keyword}+site%3Asweeting.tistory.com&sourceid=chrome&ie=UTF-8"

    driver.get(search_url)
    print(search_url)

    try:
        # 검색 결과 링크 가져오기
        # #rso > div:nth-child(1) > div > div > div > div > a
        links = driver.find_elements(By.CSS_SELECTOR, f'#search > div > #rso > div:nth-child(1) > div > div > div > div > a')


        for link in links:
            url = link.get_attribute('href')
            url_lists.append(url)

    except NoSuchElementException:
        print(">  NoSuchElementException ", search_url)


# URL 리스트 출력
for url in url_lists:
    print(url)

# WebDriver 종료
driver.quit()
