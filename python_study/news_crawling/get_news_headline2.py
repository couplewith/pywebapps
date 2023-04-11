import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEBUG = 1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


url='https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101'   #경제-헤드라인
html_selector='#main_content > div > div._persist > div:nth-child(1) > div:nth-child(-n+10) > div.cluster_body > ul > li:nth-child(1) > div.cluster_text'

response = requests.get(url,headers=headers, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')

news_titles = []
news_links = []
no=0
for news in soup.select(html_selector):
    no = no + 1

    item_href  = news.select_one('a')['href']
    item_title = news.select_one('a').text
    item_desc  = news.select_one('div.cluster_text_lede').get_text().strip().replace('\n', '')

    if (DEBUG) :
        # print("[%d] %s\n" % (no, news))
        print("[%d] %s | %s | %s\n" % (no, item_href, item_title, item_desc))

    news_titles.append({"no": no, 'title': item_title, 'desc': item_desc})


if (DEBUG) :
   print(news_titles[0])
   print(news_titles[no])
   print (no)



# ********************************************************************************************
#url='https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101'   #경제-헤드라인
#html_selector='#main_content > div > div._persist > div:nth-child(1) > div:nth-child(-n+10) > div.cluster_body > ul > li:nth-child(1) > div.cluster_text'
#
#  <div class="cluster_text">
# <a class="cluster_text_headline nclicks(cls_eco.clsart)" href="https://n.news.naver.com/mnews/article/008/0004872792?sid=101">삼성 감산 결정, 반도체 업황 반등 빨라진다…'매수' 의견-신한</a>
# <div class="cluster_text_lede">신한투자증권이 10일 삼성전자에 대해 투자의견 '매수', 목표주가 8만2000원을 제시했다. 삼성전자의 감산 결정으로 반도체 업황이 예상보다 이르게 상승 …</div>
# <div class="cluster_text_info" data-comment="{gno:'news008,0004872792',params:{sid1:'101'},nclicks:'cmt.count','type':'sectionHomeCluster'}">
# <div class="cluster_text_press">머니투데이</div>
# </div>
# </div>

# # url= 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=101&sid2=258' #증권
# # html_selector="#main_content > div.list_body.newsflash_body > ul.type06_headline > li:nth-child(-n+10)"
#
# # url='https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101'   #경제-헤드라인
# # html_selector='#main_content > div > div._persist > div:nth-child(1) > div:nth-child(-n+10)'  #경제-클러스터-headline