from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, \
    UnexpectedAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import re
import time

import urllib3
from bs4 import BeautifulSoup

import module_webdriver as WD
urllib3.disable_warnings()


###################################################################
ui_mode = 1   # 1 : with browser UI,  other: without browser UI


# get sitemap.xml for web listing
sitemap_urls = ["https://sweeting.tistory.com/sitemap.xml","https://couplewith.tistory.com/sitemap.xml", "https://agilebus.blogspot.com/sitemap.xml","https://sweetlifecafe.blogspot.com/sitemap.xml"]

blog_links = []
page_lists = []

#pattern = r'com/[0-9]{1,3}'
pattern = r'com/[0-9]{1,4}'

# 1. Get webpage url list #####################
# get sitemap.xml for web listing
for sitemap_url in sitemap_urls:

    response = requests.get(sitemap_url, verify=False)
    soup = BeautifulSoup(response.content, 'xml')

    for url in soup.find_all('url'):
        loc_tag = url.find('loc')
        if loc_tag is None:
            print(" > Skipped ~ Tag continue - ", url)
            continue
        url_str = loc_tag.text
        matched = re.search(pattern, url_str)
        if not matched:
            print(" > Skipped ~ continue - ", url_str)
            continue

        page_url = url.findNext('loc').text
        page_lists.append(page_url)



# 2. Search Web pages  #####################

# selenium page Webdriver
ui_mode = 1   # 1 : with browser UI,  other: without browser UI
driver = WD.set_driver("edge", ui_mode)
#driver = set_driver("chrome", ui_mode)

action_timeout = 3
page_timeout = 5  # Set a timeout value in seconds
action_timeout = 3  # Set event timeout
no = 0
page_title = ''

# 2. Search Web pages  #####################
for go_url in page_lists:
    no = no + 1
    WD.get_elapsed(init=1)# init elapsed time

    driver.set_page_load_timeout(page_timeout)  # 5 seconds
    driver.implicitly_wait(action_timeout)  # default 5 seconds : implicitly_wait
    like_text = ''
    like_text_aft = ''

    try:
        driver.get(go_url)

        # scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page_soup = BeautifulSoup(driver.page_source, 'html.parser')
        page_title = page_soup.title.text


        print(no, page_title, go_url)

        print("  > check element_to_be_clickable  ")
        # button = driver.find_element(By.CSS_SELECTOR, "button.btn_post.uoc-icon")
        # like_button = WebDriverWait(driver, action_timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.uoc-icon')))
        like_button = WebDriverWait(driver, action_timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn_post.uoc-icon')))
        like_text = like_button.text.strip()
        like_text_aft = like_text

        try:
            # Disable alerts temporarily
            driver.switch_to.alert.accept()

        except NoAlertPresentException:
            pass  # No alert window present, continue with the code

        like_button.click()

        print("  > after click holding - ", WD.get_elapsed())

        time.sleep(1)

        WD.action_escape(driver)
        WD.alert_handle(driver, action_timeout, True)
        print("  > after alert_handle - ", WD.get_elapsed())
        # alert except : UnexpectedAlertPresentException

        like_button_aft = WebDriverWait(driver, action_timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.uoc-icon.empathy_up_without_ani.like_on')) )
        like_text_aft = like_button_aft.text.strip()
        print("  > catch new LikeBtn ---->", like_text, like_text_aft)

    except TimeoutException:
        #like_button = driver.find_element(By.CSS_SELECTOR, 'div.uoc-icon.empathy_up_without_ani.like_on')
        print("  >> Like button is not found. - TimeoutException")
    except ElementClickInterceptedException:
        print("  >> ElementClickInterceptedException: Like button is not clickable.- ", WD.get_elapsed())
    except UnexpectedAlertPresentException:
        print("  >> UnexpectedAlertPresentException Alert: 유효하지 않은 요청입니다.- ", WD.get_elapsed())
        WD.alert_handle(driver, action_timeout, True)
    finally:
        driver.set_page_load_timeout(0)
        blog_links.append({'title': page_title, 'url': go_url, 'like': like_text, 'like_aft': like_text_aft})
        print("  >> finally done !! - ", no, like_text, like_text_aft, WD.get_elapsed())
        continue


driver.quit()
print(no, blog_links)

if no > 1:
    print(len(blog_links),blog_links[-1:])
else:
    print(len(blog_links), blog_links)


# Usage :
# python get_sitemap_webdrive_like.py
# 1) cannot browser in PATH  :
#  - First Execute your browser(edge,firefox...) on your desktop then beautifulsoup can access browser.
#    if not it will occur error with "not found edge browser".
# 2) Using WebDriverWait
#  - "If the requested contents are not presented, driver.find_element will not find any matching element."
#
# 브라우저가 작동이 안될때 pycharm 터미널에 실행
# D:\github\pywebapps\venv\Lib\site-packages\selenium\webdriver\common\windows\selenium-manager.exe --browser edge --output json
# Selenium Grid의 구성 요소 중 하나인 Selenium Standalone Server를 시작하는 데 사용됩니다.
# 3) Alert 창 관련  https://couplewith.tistory.com/428
#                  https://couplewith.tistory.com/427
#                  https://couplewith.tistory.com/426
#   - UnexpectedAlert Alert Text: 유효하지 않은 요청입니다.
#   - Message: unexpected alert open: {Alert text : 유효하지 않은 요청입니다.}