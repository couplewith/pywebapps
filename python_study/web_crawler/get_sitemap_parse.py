import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sitemap_url = "https://couplewith.tistory.com/sitemap.xml"
#sitemap_url = "https://example.com/sitemap.xml"
response = requests.get(sitemap_url, verify=False)
soup = BeautifulSoup(response.content, 'lxml')

for url in soup.find_all('url'):
    print(" >> url %s start" % (url))
    page_url = url.findNext('loc').text
    page_response = requests.get(page_url, verify=False)
    print(" >> response %s %s" % (page_url, page_response))
    page_soup = BeautifulSoup(page_response.content, 'html.parser')
    page_title = page_soup.title.text
    print(page_title)
