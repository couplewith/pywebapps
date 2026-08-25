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
key_words.extend(["인공지능","AI비즈니스","AI&Tech","AI 에이전트","AI챗봇","RAG","자가진화"])
key_words.extend(["퀀텀 양자","쳇봇 RAG","IT트렌드", "Trends", "디지털+트렌스포메이션", "Digital+Transformation"])
key_words.extend(["오늘의명언","명언","전략기획","경영전략","성공 전략"])
key_words.extend(["빅데이터","database","블록체인","Data+mesh", "SQL", "SQLite"])
key_words.extend(["리눅스", "Linux 튜닝", "Linux","셀스크립트","정규표현식","원도우+파일복구"])
key_words.extend(["블록체인","스마트컨트렉트","금융","STO","ERC-1400"])
key_words.extend(["selenium+기초","셀레니움", "테스트 자동화","Python","파이썬+프로그래밍기초","Rust+프로그래밍" ])

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
        

    try:
        
        if idx <3:
            time.sleep(30)
        else:
            time.sleep(1)

        # 검색 결과 링크 가져오기
        # #rso > div:nth-child(1) > div > div > div > div > div > span > a
        # CSS PATH : #rso > div:nth-child(1) > div > div > div > div > a
        # Xpath : //*[@id="rso"]/div[2]/div/div/div[1]/div/div/span/a
        # // XPath 표현식은 ID가 "rso"인 모든 /div 요소를 선택한다.

        links = driver.find_elements(By.XPATH, '//*[@id="rso"]//div//a')
        links_len=len(links)
        print( f'[{idx}]>> search result find links [{links_len}]' )

        for link in links:
            url = link.get_attribute('href')
            attr = link.get_attribute('text')
            url_lists.append({"url": url, "attr": attr, "keyword" : keyword})
        
        url_cnt=len(url_lists)

        print(f' >>keyword [{keyword}]--> url_lists_cnt:{url_cnt}')

    except NoSuchElementException:
        print(">  NoSuchElementException ", search_url)

#################
print("[Url Scan Done] -> url_lists ", len(url_lists), url_lists)

#################
# URL 리스트 출력 :  url_lists[ [url, attr, keyword],... ]
#################

idx = 0
tabid = 0
tabid_bef = 0

for url in url_lists:
    
    idx = idx + 1
    tabid = (idx % 3)

    driver.switch_to.window(driver.window_handles[tabid])
    print(idx, tabid, tabid_bef, url)

    driver.get(url['url'])

    driver.switch_to.window(driver.window_handles[tabid_bef])

    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 페이지를 키워드로 스크롤 합니다.
    for c in range(0, 2):
        # 페이지를 아래 위로 스크롤 합니다.
        driver.find_element(By.TAG_NAME, value='body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        driver.find_element(By.TAG_NAME, value='body').send_keys(Keys.PAGE_UP)
        time.sleep(1)
        driver.find_element(By.TAG_NAME, value='body').send_keys(Keys.PAGE_DOWN)
    


    time.sleep(1)
    driver.switch_to.window(driver.window_handles[tabid])
    tabid_bef = tabid

    print(f'Done>> idx=[{idx}]  tabid[{tabid}], tabid_bef[{tabid_bef}], url={url}')

# WebDriver 종료
#driver.quit()
