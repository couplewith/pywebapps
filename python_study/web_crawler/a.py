import re
url1="https://brownbears.tistory.com/506"
url2="https://brownbears.tistory.com/adfasdfsas234dfadf"
pattern=r'/[0-9]{1,3}$'
url_list=[]
url_list.append(url1)
url_list.append(url2)
for url in url_list:
    matched = re.search(pattern, url)
    if not matched:
        print ("continue", url)
        continue
    print(url, "OK")
