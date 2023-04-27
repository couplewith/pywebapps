import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
from time import sleep



def set_driver(browser, mode):
    # http://httpbin.org/user-agent
    # chrome
    user_agent  = '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    # edge
    user_agent1 = '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58'

    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        if ui_mode != 1:
            options.add_argument('--headless')  # run Chrome in headless mode (without a UI)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument(user_agent)

        driver = webdriver.Chrome(options=options)
    else:
        options = webdriver.EdgeOptions()
        if ui_mode != 1:
            options.add_argument('--headless')  # run Chrome in headless mode (without a UI)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument(user_agent)

        driver = webdriver.Edge(options=options)
    return driver

###################################################################
ui_mode = 1   # 1 : with browser UI,  other: without browser UI

sitemap_url = "https://couplewith.tistory.com/sitemap.xml"

driver = set_driver("edge", ui_mode)

# get sitemap.xml for web listing
response = requests.get(sitemap_url, verify=False)
soup = BeautifulSoup(response.content, 'xml')
blog_links = []
no = 0

for url in soup.find_all('url'):
    page_url = url.findNext('loc').text
    driver.get(page_url)
    sleep(0.9)  # wait for page to load
    # scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    page_soup = BeautifulSoup(driver.page_source, 'html.parser')
    page_title = page_soup.title.text
    print(no, page_title, page_url)
    blog_links.append({'title': page_title, 'url': page_url})
    # Like 클릭 여부 확인
    try:
        #like_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.uoc-icon')))
        #like_button.click()
        # like 화면이 보이지 않는 상태에서 오류가 나는 것을 방지
        # ActionChains를 이용하여, like_button 요소의 위치로 이동한 후, click() 메소드를 실행 클릭합니다.
        like_button = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.uoc-icon')))
        # 요소를 클릭할 수 있는 위치로 이동
        ActionChains(driver).move_to_element(like_button).perform()
        # 클릭 실행
        ActionChains(driver).click().perform()

        print (">> new Liked ----")
    except TimeoutException:
        #like_button = driver.find_element(By.CSS_SELECTOR, 'div.uoc-icon.empathy_up_without_ani.like_on')
        print("Like button is not found.")
    finally:
        no = no + 1
        sleep(2)  # delay for next page


driver.quit()
print(len(blog_links),blog_links[no-1] )