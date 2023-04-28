from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# 직접 tag 내용 추출
def get_tag_element(tag_name):
    element = None
    status = False
    try:
        element = driver.find_element_by_css_selector(tag_name)
        status = True
        print(element, tag_name )
    except NoSuchElementException:
        print("요소가 존재하지 않습니다.",tag_name)
    finally:
        return element, status

#  화면 로딩 대기 후 tag 항목 추출 : 태그가 화면에 나타날 때까지 기다린 뒤 해당 요소를 반환
def get_tag_element_wait(tag_name, wait_time=10):
    element = None
    status = False
    try:
        wait = WebDriverWait(driver, wait_time)
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, tag_name)))
        status = True
    except TimeoutException:
        print("요소가 존재하지 않습니다.",tag_name)
    finally:
        return element, status

####################################################
# 웹 드라이버 로드
driver = webdriver.Chrome()



tag_first_article = "#today_main_news > div.hdline_news > ul > li:nth-child(1) > div.hdline_article_tit > a"
tag_title = "#articleTitle"
tag_contents = "#articleBodyContents"

# 메인 헤드라인
news_url="https://news.naver.com"
tag_first_article = "#ct > div > section.main_content > div.main_brick > div > div:nth-child(1) > div.main_brick_item._press_main_status_wrapper > div > div.cjs_news_flash_wrap.cjs_nf_close._newsflash_wrapper > div.cjs_nf_list._item_list > a:nth-child(2) > div > h4"

# 경제 - 헤드라인
news_url="https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"
tag_biz_artitle = "#main_content > div > div._persist > div:nth-child(1) > div:nth-child(1) > div.cluster_body > ul > li:nth-child(1) > div.cluster_text > a"
tag_title = "#title_area"
tag_contents = "#contents"

tag_first_article = tag_biz_artitle
tag_title = tag_title
tag_contents = tag_contents

# 페이지 접속
driver.get(news_url)
driver.implicitly_wait(5) # 10초 대기
# 첫 번째 기사 클릭
# 특정 영역을 포함한 부모 요소를 찾아서 저장

(first_article, status) = get_tag_element_wait(tag_first_article)
print (first_article)
if first_article != None:
    first_article.click()
else:
    print(" article not found")
    exit(1)


driver.implicitly_wait(5) # 10초 대기

title = ''
(element, status ) = get_tag_element_wait(tag_title)
if element!=None:
    title = element.text
print(title, status, tag_title )

content = ''
(element, status ) = get_tag_element_wait(tag_contents)
if element!=None:
    content = element.text
print(content, status, tag_contents )



# 추출한 데이터 저장
with open('article.txt', 'w', encoding='utf-8') as f:
    f.write(f"제목 : {title}\n\n")
    f.write(content)

# 브라우저 닫기
driver.quit()