import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from time import sleep

DEBUG = 1  # 0 : 정상,  1: 디버깅 ,  2: 테스트

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


url_base='https://couplewith.tistory.com'
html_selector='#container > main > div > div.area-view > div.article-header > div > div'  # 제목


def crawler_blog(url, html_selector, DEBUG):
    response = requests.get(url,headers=headers, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    blog_titles = []
    blog_links = []
    no=0
    for news in soup.select(html_selector):
        no = no + 1

        item_title = news.select_one('h2').text

        if (DEBUG) :
            print("[%d] %s | %s \n" % (no, item_title, url))
        blog_titles.append({"no": no, 'title': item_title,'url': url})


def crawler_exec(url_base, html_selector, DEBUG):
    url_range = [1, 400]

    for idx in range(url_range[0], url_range[1], 1):
        url = url_base + "/" + str(idx)
        print (url)
        crawler_blog(url, html_selector, DEBUG)

        sleep(1.0)




# Test-mode
if DEBUG == 2 :
    crawler_blog (url_base + "/" + str(300), html_selector, DEBUG)
else :
    crawler_exec(url_base, html_selector, DEBUG)
