from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import module_webdriver as WD


# driver_path = '/path/to/chromedriver'
# driver = webdriver.Chrome(executable_path=driver_path)

# selenium page Webdriver
ui_mode = 1   # 1 : with browser UI,  other: without browser UI
#driver = WD.set_driver("edge", ui_mode)
driver = WD.set_driver("chrome", ui_mode)


# 검색 엔진 사이트 접속
driver.get('https://www.google.com')

# 검색어 입력
#search_input = driver.find_element_by_name('input')  # 검색어 입력 필드의 name 속성을 확인하여 변경 가능
#search_input = driver.find_element_by_css_selector('input[name="q"]')
search_input = driver.find_element(By.CSS_SELECTOR, 'input[name="q"]')
search_input.send_keys('멋진 카페 site:sweeting.tistory.com')

# 검색 수행
search_input.send_keys(Keys.RETURN)


sleep(10)

# 웹 드라이버 종료
driver.quit()
