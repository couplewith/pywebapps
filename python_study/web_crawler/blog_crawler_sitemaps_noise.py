import re
import time
import requests
import urllib3
from bs4 import BeautifulSoup

# undetected-chromedriver 적용
import undetected_chromedriver as uc

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
    UnexpectedAlertPresentException,
    NoSuchElementException
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import module_webdriver as WD

urllib3.disable_warnings()

###################################################################
# 0. Noise Injection (Canvas / WebGL / Audio Fingerprint 난독화 JS)
###################################################################
NOISE_INJECTION_SCRIPT = """
// 1) Canvas 노이즈 주입 (toDataURL / getImageData 난독화)
const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
HTMLCanvasElement.prototype.toDataURL = function(...args) {
    const ctx = this.getContext('2d');
    if (ctx) {
        const imgData = ctx.getImageData(0, 0, Math.min(this.width, 16), Math.min(this.height, 16));
        for (let i = 0; i < imgData.data.length; i += 4) {
            imgData.data[i] = imgData.data[i] ^ 1; // 1비트 미세 노이즈
        }
        ctx.putImageData(imgData, 0, 0);
    }
    return originalToDataURL.apply(this, args);
};

// 2) WebGL 노이즈 주입 (Renderer/Vendor 고정 및 파라미터 모의)
const getParameterProto = WebGLRenderingContext.prototype.getParameter;
WebGLRenderingContext.prototype.getParameter = function(parameter) {
    // UNMASKED_VENDOR_WEBGL (37445), UNMASKED_RENDERER_WEBGL (37446)
    if (parameter === 37445) {
        return 'Intel Inc.';
    }
    if (parameter === 37446) {
        return 'Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0';
    }
    return getParameterProto.apply(this, [parameter]);
};

// 3) AudioContext 핑거프린팅 노이즈 주입
if (window.AudioBuffer) {
    const originalGetChannelData = AudioBuffer.prototype.getChannelData;
    AudioBuffer.prototype.getChannelData = function(channel) {
        const data = originalGetChannelData.apply(this, [channel]);
        for (let i = 0; i < data.length; i += 100) {
            data[i] += (Math.random() * 0.0000001); // 미세 오디오 노이즈 추가
        }
        return data;
    };
}
"""

###################################################################
ui_mode = 1 # 1 : with browser UI, other: without browser UI

# get sitemap.xml for web listing
sitemap_urls = [
    "https://sweeting.tistory.com/sitemap.xml",
    "https://couplewith.tistory.com/sitemap.xml",
    "https://agilebus.blogspot.com/sitemap.xml",
    "https://sweetlifecafe.blogspot.com/sitemap.xml"
]

blog_links = []
page_lists = []

#pattern = r'com/[0-9]{1,3}'
pattern = r'com/[0-9]{1,4}'

# 1. Get webpage url list #####################
# get sitemap.xml for web listing
for sitemap_url in sitemap_urls:
    try:
        response = requests.get(sitemap_url, verify=False, timeout=10)
        #soup = BeautifulSoup(response.content, 'xml')
        soup = BeautifulSoup(response.content, 'html.parser')

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

            page_url = loc_tag.text
            page_lists.append(page_url)
    except Exception as e:
        print(f" > Sitemap read error: {sitemap_url} -> {e}")

# 2. Search Web pages #####################

# selenium page Webdriver -> undetected-chromedriver로 설정
options = uc.ChromeOptions()
if ui_mode == 1:
    options.add_argument("--start-maximized")
else:
    options.add_argument("--headless")

options.add_argument("--lang=ko-KR")

# undetected-chromedriver 드라이버 생성
#driver = uc.Chrome(options=options)
driver = uc.Chrome(options=options, version_main=151)

# CDP(Chrome DevTools Protocol)를 통해 신규 문서 생성 시 노이즈 주입 스크립트 선행 평가
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": NOISE_INJECTION_SCRIPT
})

page_timeout = 5 # Set a timeout value in seconds
action_timeout = 3 # Set event timeout
no = 0
page_title = ''

# 2. Search Web pages #####################
for go_url in page_lists:
    no = no + 1
    WD.get_elapsed(init=1)# init elapsed time

    driver.set_page_load_timeout(page_timeout) # 5 seconds
    driver.implicitly_wait(action_timeout) # default 5 seconds : implicitly_wait
    like_text = ''
    like_text_aft = ''

    try:
        driver.get(go_url)

        # scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page_soup = BeautifulSoup(driver.page_source, 'html.parser')
        page_title = page_soup.title.text if page_soup.title else "No Title"

        print(no, page_title, go_url)

        print(" > check element_to_be_clickable ")
        # button = driver.find_element(By.CSS_SELECTOR, "button.btn_post.uoc-icon")
        # like_button = WebDriverWait(driver, action_timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.uoc-icon')))# like_button = WebDriverWait(driver, action_timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn_post.uoc-icon')) )
        like_button = WebDriverWait(driver, action_timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn_post.uoc-icon')))
        like_text = like_button.text.strip()
        like_text_aft = like_text

        time.sleep(1)
        WD.action_mouse_scroll(driver, 400)

        # 페이지를 키워드로 스크롤 합니다.
        for c in range(0, 2):
            # 페이지를 아래 위로 스크롤 합니다.
            driver.find_element(By.TAG_NAME, value='body').send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            driver.find_element(By.TAG_NAME, value='body').send_keys(Keys.PAGE_UP)

        try:
            # Disable alerts temporarily
            driver.switch_to.alert.accept()
        except (UnexpectedAlertPresentException, Exception):
            pass # No alert window present, continue with the code

        like_button.click()

        print(" > after click holding - ", WD.get_elapsed())

        time.sleep(1)

        WD.action_escape(driver)
        WD.alert_handle(driver, action_timeout, True)
        print(" > after alert_handle - ", WD.get_elapsed())
        # alert except : UnexpectedAlertPresentException

        like_button_aft = WebDriverWait(driver, action_timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.uoc-icon.empathy_up_without_ani.like_on')))
        like_text_aft = like_button_aft.text.strip()
        print(" > catch new LikeBtn ---->", like_text, like_text_aft)

    except TimeoutException:
        #like_button = driver.find_element(By.CSS_SELECTOR, 'div.uoc-icon.empathy_up_without_ani.like_on')
        print(" >> Like button is not found. - TimeoutException")
    except ElementClickInterceptedException:
        print(" >> ElementClickInterceptedException: Like button is not clickable.- ", WD.get_elapsed())
    except UnexpectedAlertPresentException:
        print(" >> UnexpectedAlertPresentException Alert: 유효하지 않은 요청입니다.- ", WD.get_elapsed())
        WD.alert_handle(driver, action_timeout, True)
    except Exception as e:
        print(f" >> General Exception ({go_url}): {e}")
    finally:
        driver.set_page_load_timeout(5)
        WD.clear_cookie(driver)
        blog_links.append({'title': page_title, 'url': go_url, 'like': like_text, 'like_aft': like_text_aft})
        print(" >> finally done !! - ", no, like_text, like_text_aft, WD.get_elapsed())
        continue

driver.quit()
print(no, blog_links)

if no > 1:
    print(len(blog_links), blog_links[-1:])
else:
    print(len(blog_links), blog_links)

# Usage :
# python get_sitemap_webdrive_like.py
# 1) cannot browser in PATH :
# - First Execute your browser(edge,firefox...) on your desktop then beautifulsoup can access browser.
# if not it will occur error with "not found edge browser".
# 2) Using WebDriverWait
# - "If the requested contents are not presented, driver.find_element will not find any matching element."
#
# 브라우저가 작동이 안될때 pycharm 터미널에 실행
# D:\github\pywebapps\venv\Lib\site-packages\selenium\webdriver\common\windows\selenium-manager.exe --browser edge --output json
# Selenium Grid의 구성 요소 중 하나인 Selenium Standalone Server를 시작하는 데 사용됩니다.
# 3) Alert 창 관련 https://couplewith.tistory.com/428
# https://couplewith.tistory.com/427
# https://couplewith.tistory.com/426
# - UnexpectedAlert Alert Text: 유효하지 않은 요청입니다.
# - Message: unexpected alert open: {Alert text : 유효하지 않은 요청입니다.}