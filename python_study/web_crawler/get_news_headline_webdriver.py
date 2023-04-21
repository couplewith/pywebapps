from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from time import sleep

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
    url_range = [1, 500]

    for idx in range(url_range[0], url_range[1], 1):
        url = url_base + "/" + str(idx)
        print (url)
        crawler_blog(url, html_selector, DEBUG)

        sleep(1.0)

def webdriver_crawler_blog(url, html_selector, wdriver, DEBUG):

    if wdriver == '':
        wdriver=webdriver.Chrome()
        wdriver.implicitly_wait(2)

    # 웹 페이지를 엽니다.
    wdriver.get(url)

    # JavaScript 코드를 실행합니다.
    wdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    soup = BeautifulSoup(wdriver.page_source, 'html.parser')

    # response = requests.get(url,headers=headers, verify=False)
    # soup = BeautifulSoup(response.text, 'html.parser')

    blog_titles = []
    blog_links = []
    no=0
    for news in soup.select(html_selector):
        no = no + 1

        item_title = news.select_one('h2').text

        if (DEBUG) :
            print("[%d] %s | %s \n" % (no, item_title, url))
        blog_titles.append({"no": no, 'title': item_title,'url': url})

def webdriver_crawler_exec(url_base, html_selector, DEBUG):

    url_range = [500, 1]
    # 웹 드라이버를 엽니다.
    # WebDriver    wdriver = new  ChromeDriver();
    wdriver = webdriver.Chrome()
    wdriver.implicitly_wait(2)

    for idx in range(url_range[0], url_range[1], 1):
        url = url_base + "/" + str(idx)
        print (url)
        webdriver_crawler_blog(url, html_selector, wdriver, DEBUG)

        sleep(1.0)

    wdriver.close()
    wdriver.quit()

####################################################################
def main(DEBUG=2):

    # -- init ---
    DEBUG = 1  # 0 : 정상,  1: 디버깅 ,  2: 테스트

    test_mode="request_all"
    test_mode="request_test"
    test_mode="webdriver_all"
    test_mode="webdriver_test"

    # -- global ---
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    url_base = 'https://couplewith.tistory.com'
    html_selector = '#container > main > div > div.area-view > div.article-header > div > div'  # 제목

    if DEBUG == 2 :
        test_mode="request_test"
        #crawler_blog (url_base + "/" + str(300), html_selector, DEBUG)
    else :
        test_mode = "webdriver_all"
        #crawler_exec(url_base, html_selector, DEBUG)

    print(">> Start [%s] ------", test_mode)
    match test_mode:
        case 'request_all':
            crawler_exec(url_base, html_selector, DEBUG)
        case 'webdriver_all':
            webdriver_crawler_exec(url_base, html_selector, DEBUG)
        case 'request_test':
            crawler_blog (url_base + "/" + str(300), html_selector,  DEBUG)
        case 'webdriver_test':
            wdriver = webdriver.Chrome()
            webdriver_crawler_blog(url_base, html_selector, wdriver, DEBUG)
        case other:
            print (" default action ")

####################################################################
if __name__ == "__main__":
    # Execute when the module is not initialized from an import statement.
    main()