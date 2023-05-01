from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 웹 드라이버 로드
driver = webdriver.Chrome()

# 페이지 접속
driver.get("https://news.naver.com")

# 첫 번째 기사 클릭
first_article = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#today_main_news > div.hdline_news > ul > li:nth-child(1) > div.hdline_article_tit > a"))
)
first_article.click()

# 기사 제목과 내용 추출
title = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#articleTitle"))
).text

content = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#articleBodyContents"))
).text

# 추출한 데이터 저장
with open('article.txt', 'w', encoding='utf-8') as f:
    f.write(f"제목 : {title}\n\n")
    f.write(content)

# 브라우저 닫기
driver.quit()