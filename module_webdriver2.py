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


def set_driver(browser, ui_mode=1):
    # ui_mode :: 0 : headless (without ui) , 1: browser with ui
    # http://httpbin.org/user-agent
    # chrome
    user_agent  = '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    # edge
    user_agent1 = '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58'

    driver = None

    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        if ui_mode != 1:
            options.add_argument('--headless')  # run Chrome in headless mode (without a UI)
            options.add_argument('--log-level=3')
            options.add_argument('--disable-logging')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')

        options.add_argument("--incognito")  # secret mode
        options.add_argument('--ignore-certificate-errors')
        
        # --- [추가] 자동화 탐지 방지 및 제어 알림창 제거 옵션 ---
        options.add_argument("--disable-blink-features=AutomationControlled")  # navigator.webdriver 플래그 비활성화
        options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 제어 알림 메시지 제거
        options.add_experimental_option("useAutomationExtension", False)  # 자동화 확장 모듈 로드 해제
        # ----------------------------------------------------

        # options.add_argument("--disable-notifications"); # < old version 50.x
        # > new version 50.x
        options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
        options.add_argument(user_agent)
        driver = webdriver.Chrome(options=options)

    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        if ui_mode != 1:
            options.headless = True # run Firefox in headless mode (without a UI)
        options.accept_insecure_certs = True
        options.set_preference("general.useragent.override", user_agent)
        options.set_preference("dom.webnotifications.serviceworker.enabled", False)
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("dom.push.enabled", False)
        
        # --- [추가] 파이어폭스 전용 navigator.webdriver 방지 설정 ---
        options.set_preference("dom.webdriver.enabled", False)
        # -----------------------------------------------------

        driver = webdriver.Firefox(options=options)

    else:
        options = webdriver.EdgeOptions()
        if ui_mode != 1:
            options.add_argument('--headless')  # run Chrome in headless mode (without a UI)
            options.add_argument('--log-level=3')
            options.add_argument('--disable-logging')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
        options.add_argument("-inprivate")
        options.add_argument("--incognito")  # secret mode
        options.add_argument('--ignore-certificate-errors')

        # --- [추가] 에지(Chromium) 자동화 탐지 방지 옵션 ---
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        # --------------------------------------------------

        options.add_argument("--disable-notifications")
        options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
        options.add_argument(user_agent)
        driver = webdriver.Edge(options=options)

    # --- [추가] JavaScript 탐지 완벽 우회 (페이지 변경/이동 후에도 유효하게 적용) ---
    if driver and browser in ['chrome', 'edge']:
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                """
            }
        )
    # ----------------------------------------------------------------------------

    return driver

start_time = time.time()
def get_elapsed(init=0):
    global start_time  # global variable
    if init == 1 or start_time is None :
        start_time = time.time()
    end_time = time.time()
    elapsed_time = end_time - start_time
    return " > Elapsed: {:.2f} seconds".format(elapsed_time)


def alert_handle2(driver, timeout=5, accept=True ):
    try:
        print(" def> alert_handle2: - ", get_elapsed())
        driver.implicitly_wait(timeout)

        alert = Alert(driver)
        alert_text = alert.text
        if (accept == True):
            print(" def> alert_handle2: alert.accept()")
            alert.accept()
        else:
            print(" def> alert_handle2: alert.dismiss()")
            alert.dismiss()

    except Exception as err:
        print(f" def> alert_handle2 {err=}, {type(err)=}")
        pass

def alert_handle(driver, timeout=5, accept=True):
    # alert handle  deprecated
    alert_present=''
    try:

        #driver.implicitly_wait(timeout)
        alert_present = WebDriverWait(driver, timeout).until(EC.alert_is_present())

        if alert_present:
            print(" > alert_handle: Alert window is present", get_elapsed())
            alert = driver.switch_to.alert
            alert.dismiss()
            #alert.accept()
            print(" > alert.dismiss - ", get_elapsed())
        else:
            print(" > alert_handle:  Alert window is not present")
            action_escape(driver)
    except Exception as err:
        print(f" def> alert_handle {err=}, {type(err)=}")
        alert_handle2(driver, timeout)
        pass
    finally:
        print(f" > alert_handle : done !! alert_present={alert_present}, {type(alert_present)=}", get_elapsed())

def action_escape(driver):
    # Simulate pressing the Escape key
    actions = ActionChains(driver)
    actions.send_keys(Keys.ESCAPE).perform()
    print(" > action_escape: send escape key - ", get_elapsed())