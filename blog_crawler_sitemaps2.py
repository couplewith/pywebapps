# pip install lxml bs4

import random
import re
import time
import requests
import urllib3
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
    UnexpectedAlertPresentException,
    NoAlertPresentException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import module_webdriver2 as WD

urllib3.disable_warnings()

###################################################################
ui_mode = 1  # 1 : with browser UI, other: without browser UI

# get sitemap.xml for web listing
sitemap_urls = [
    "https://sweeting.tistory.com/sitemap.xml",
    "https://couplewith.tistory.com/sitemap.xml",
    "https://smartbus.tistory.com/sitemap.xml",
    "https://sweetlifecafe.blogspot.com/sitemap.xml",
]

blog_links = []
page_lists = []

pattern = r"com/[0-9]{1,4}"

# 1. Get webpage url list #####################
for sitemap_url in sitemap_urls:
    response = requests.get(sitemap_url, verify=False)
    soup = BeautifulSoup(response.content, "xml")

    for url in soup.find_all("url"):
        loc_tag = url.find("loc")
        if loc_tag is None:
            print(" > Skipped ~ Tag continue - ", url)
            continue
        url_str = loc_tag.text
        matched = re.search(pattern, url_str)
        if not matched:
            print(" > Skipped ~ continue - ", url_str)
            continue

        page_url = url.findNext("loc").text
        page_lists.append(page_url)


# 2. Search Web pages #####################
driver = WD.set_driver("edge", ui_mode)

# 브라우저 시작 시 무작위 창 크기 1회 설정 (루프 내부에서 매번 실행 방지)
window_sizes = [(1366, 768), (1440, 900), (1920, 1080), (1536, 864)]
w, h = random.choice(window_sizes)
driver.set_window_size(w, h)

page_timeout = 5  # Set a timeout value in seconds
action_timeout = 3  # Set event timeout
no = 0
N = 5  # 브라우저 재시작 주기 (5회마다 브라우저 재시작)
page_title = ""

# 2. Search Web pages #####################
for go_url in page_lists:
    no = no + 1

    # 5회 마다 브라우저 재시작하여 완전히 새로운 세션 생성
    if no > 1 and (no - 1) % N == 0:
        print("  [System] Resetting browser session...")
        driver.quit()
        time.sleep(2)
        driver = WD.set_driver("edge", ui_mode)
        w, h = random.choice(window_sizes)
        driver.set_window_size(w, h)
    
    WD.get_elapsed(init=1)  # init elapsed time

    driver.set_page_load_timeout(page_timeout)  # 5 seconds
    driver.implicitly_wait(action_timeout)  # default 5 seconds : implicitly_wait
    like_text = ""
    like_text_aft = ""

    try:
        driver.get(go_url)

        # scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page_soup = BeautifulSoup(driver.page_source, "html.parser")
        page_title = page_soup.title.text

        print(no, page_title, go_url)

        print("  > check element_to_be_clickable  ")
        like_button = WebDriverWait(driver, action_timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn_post.uoc-icon"))
        )
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

        like_button_aft = WebDriverWait(driver, action_timeout).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.uoc-icon.empathy_up_without_ani.like_on")
            )
        )
        like_text_aft = like_button_aft.text.strip()
        print("  > catch new LikeBtn ---->", like_text, like_text_aft)

    except TimeoutException:
        print("  >> Like button is not found. - TimeoutException")
    except ElementClickInterceptedException:
        print(
            "  >> ElementClickInterceptedException: Like button is not clickable.- ",
            WD.get_elapsed(),
        )
    except UnexpectedAlertPresentException:
        print(
            "  >> UnexpectedAlertPresentException Alert: 유효하지 않은 요청입니다.- ",
            WD.get_elapsed(),
        )
        WD.alert_handle(driver, action_timeout, True)
    finally:
        # [수정 완료] driver.set_page_load_timeout(0) 제거 (타임아웃 현상 원인 차단)
        blog_links.append(
            {
                "title": page_title,
                "url": go_url,
                "like": like_text,
                "like_aft": like_text_aft,
            }
        )
        print(
            "  >> finally done !! - ",
            no,
            like_text,
            like_text_aft,
            WD.get_elapsed(),
        )


driver.quit()
print(no, blog_links)

if no > 1:
    print(len(blog_links), blog_links[-1:])
else:
    print(len(blog_links), blog_links)