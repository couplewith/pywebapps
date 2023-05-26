# Web Crawling with Selenium
# 셀레니움을 이용한 웹크롤링


# Alert 창 정리
  Alert 창이 생기면 화면이 넘어가지 않는다.
  Browser의 Alert 에 대한 창을 나오지 않도록 하는 것도 하지만 
  작동이 안되었다.

 
  * Alert창이 컨트롤 되지 않는다.
    - alert = Alert(driver) 은 작동이 안된다.
    - alert_present = EC.alert_is_present() 는 작동이 된다.
  
  * alert_handle(driver, True, 5)
     
  * def alert_handle(driver, accept=True, timeout=5):
    - driver.implicitly_wait(timeout)
    - alert = Alert(driver)
    - alert.accept()
   
  * def alert_handle2(driver, timeout=5):
    - alert_present = EC.alert_is_present()
    - alert = driver.switch_to.alert()
    - alert.accept()


-----------------------------
try:
	result = driver.switch_to.alert()
    result.accept()
except:
	pass


-----------------------------
expected_conditions 모듈
-----------------------------
import time
from selenium.webdriver.support import expected_conditions as EC

time.sleep(1)

if EC.alert_is_present():
	result = driver.switch_to.alert()
    result.accept()
