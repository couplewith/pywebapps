from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, \
    UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

start_time = time.time()
def get_elapsed():
    global start_time  # global variable
    end_time = time.time()
    elapsed_time = end_time - start_time
    return " > Elapsed: {:.2f} seconds".format(elapsed_time)

go_url = 'https://couplewith.tistory.com/42'
user_agent = '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58'
options = webdriver.EdgeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--disable-notifications");
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
options.add_argument(user_agent)
driver = webdriver.Edge(options=options)


page_timeout = 30  # Set a timeout value in seconds
action_timeout = 3  # Set event timeout
no = 0
page_title = ''

driver.set_page_load_timeout(page_timeout)

try:
        driver.get(go_url)
        driver.implicitly_wait(3)  # default 0 seconds : implicitly_wait

        # scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page_soup = BeautifulSoup(driver.page_source, 'html.parser')
        page_title = page_soup.title.text


        like_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.uoc-icon')))
        like_text = like_button.text.strip()


        #time.sleep(3)

except TimeoutException:
        #like_button = driver.find_element(By.CSS_SELECTOR, 'div.uoc-icon.empathy_up_without_ani.like_on')
        print(">  Like button is not found. - TimeoutException")
except ElementClickInterceptedException:
        print(">  ElementClickInterceptedException: Like button is not clickable.- ", get_elapsed())
except UnexpectedAlertPresentException:
        print(">  UnexpectedAlertPresentException Alert: 유효하지 않은 요청입니다.- ", get_elapsed())
finally:
        driver.set_page_load_timeout(0)
        print(no, page_title, go_url, like_text, get_elapsed())