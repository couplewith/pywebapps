from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, \
    UnexpectedAlertPresentException
from selenium.webdriver import ActionChains

import module_webdriver as WD
import time


# driver_path = '/path/to/chromedriver'
# driver = webdriver.Chrome(executable_path=driver_path)

# selenium page Webdriver
ui_mode = 1   # 1 : with browser UI,  other: without browser UI
#driver = WD.set_driver("edge", ui_mode)
driver = WD.set_driver("chrome", ui_mode)


def SearchByhome(key, site=''):
    # 검색 엔진 사이트 접속
    driver.get('https://www.google.com')
    # 검색어 입력
    #search_input = driver.find_element_by_name('input')  # 검색어 입력 필드의 name 속성을 확인하여 변경 가능
    #search_input = driver.find_element_by_css_selector('input[name="q"]')
    search_input = driver.find_element(By.CSS_SELECTOR, 'input[name="q"]')
    # 검색 수행
    search_input.send_keys(Keys.RETURN)

def SearchByUrl(url):
    driver.get(url)



# --검색 결과 읽기-------------------------#
def ShowSearchResults(driver, result_css):
    # #rso > div:nth-child(1)

    elements = []

    # 검색 결과 링크 선택
    result_css="#search > div > #rso > div:nth-child(1)"
    for i in range(5):
        element = driver.find_element(By.CSS_SELECTOR, f'#search > div > #rso > div:nth-child({i + 1}) a')
        elements.append(element)

        # 검색 결과 링크 선택
        #elements[0] = driver.find_element(By.CSS_SELECTOR, '#search .g:nth-child(1) a') # 첫 번째 검색 결과를 선택합니다.


        action = ActionChains(driver)

        for item in elements :
            # New Windows Open : 새창으로 열립니다.
            action.key_down(Keys.SHIFT).click(item).key_up(Keys.SHIFT).perform()
            print(" webdriver SHIFT windows open ",len(driver.window_handles) )
            time.sleep(5)

            # New Tab Open : 새탭으로 열립니다.
            #action.key_down(Keys.CONTROL).click(item).key_up(Keys.CONTROL).perform()
            #print( " webdriver CONTROL windows open ",len(driver.window_handles) )

            #action.key_down(Keys.COMMAND).click(item).key_up(Keys.COMMAND).perform()
            #action.key_down(Keys.SHIFT).key_down(Keys.CONTROL).click(item).key_up(Keys.CONTROL).key_up(Keys.SHIFT).perform()
            #time.sleep(5)
            print(" size of windows {}", len(driver.window_handles))
            # 새 창으로 전환
            driver.switch_to.window(driver.window_handles[1])

            # 새 창 닫기
            driver.close()

            # 원래 창으로 전환
            driver.switch_to.window(driver.window_handles[0])

    time.sleep(10)
# google
KeyWords=["카페찾기", "당일여행", "대형베이커리", "베이커리카페", "주말여행"]
url ="https://www.google.com/search?q=%EC%B9%B4%ED%8E%98%EC%B0%BE%EA%B8%B0+site:sweeting.tistory.com"
result_css="#search > div > #rso > div:nth-child(1)"

SearchByUrl(url)
ShowSearchResults(driver, result_css)


# 웹 드라이버 종료
driver.quit()



#
# New Tab Open : 새탭으로 열립니다.
# action.key_down(Keys.CONTROL).click(item).key_up(Keys.CONTROL).perform()
# print( " webdriver CONTROL windows open ",len(driver.window_handles) )


# New Windows Open : 새창으로 열립니다.
action.key_down(Keys.SHIFT).click(item).key_up(Keys.SHIFT).perform()
print(" webdriver SHIFT windows open ", len(driver.window_handles))
time.sleep(5)