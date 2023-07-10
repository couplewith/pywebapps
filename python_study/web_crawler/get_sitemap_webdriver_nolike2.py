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
urllib3.disable_warnings()


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

    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        if ui_mode != 1:
            options.headless = True # run Firefox in headless mode (without a UI)
        options.accept_insecure_certs = True
        options.set_preference("general.useragent.override", user_agent)
        driver = webdriver.Firefox(options=options)

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


# get sitemap.xml for web listing
sitemap_urls = ["https://sweeting.tistory.com/sitemap.xml","https://couplewith.tistory.com/sitemap.xml"]

blog_links = []
page_lists = []

pattern = r'com/[0-9]{1,3}'
#pattern = r'com/42'

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
driver = set_driver("edge", ui_mode)
#driver = set_driver("chrome", ui_mode)

page_timeout = 15  # Set a timeout value in seconds
action_timeout = 3  # Set event timeout
no = 0
page_title = ''

# 2. Search Web pages  #####################
for go_url in page_lists:
    no = no + 1

    driver.set_page_load_timeout(page_timeout)
    driver.implicitly_wait(5)  # default 0 seconds : implicitly_wait
    like_text = ''
    like_text_aft = ''

    try:
        driver.get(go_url)

        # scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page_soup = BeautifulSoup(driver.page_source, 'html.parser')
        page_title = page_soup.title.text


        print(no, page_title, go_url)

        print(" > check element_to_be_clickable  ")
        # button = driver.find_element(By.CSS_SELECTOR, "button.btn_post.uoc-icon")
        # like_button = WebDriverWait(driver, action_timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.uoc-icon')))
        like_button = WebDriverWait(driver, action_timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn_post.uoc-icon')))
        like_text = like_button.text.strip()
        like_text_aft = like_text

    except TimeoutException:
        #like_button = driver.find_element(By.CSS_SELECTOR, 'div.uoc-icon.empathy_up_without_ani.like_on')
        print(">  Like button is not found. - TimeoutException")
    except ElementClickInterceptedException:
        print(">  ElementClickInterceptedException: Like button is not clickable.- ")
    except UnexpectedAlertPresentException:
        print(">  UnexpectedAlertPresentException Alert: 유효하지 않은 요청입니다.- ")
        alert_handle(driver,True, 10)
    finally:
        driver.set_page_load_timeout(0)
        blog_links.append({'title': page_title, 'url': go_url, 'like': like_text, 'like_aft': like_text_aft})
        print(">  finally done !! - ", no, like_text, like_text_aft)
        continue


driver.quit()
print(no, blog_links)

if no > 1:
    print(len(blog_links),blog_links[-1:])
else:
    print(len(blog_links), blog_links)
