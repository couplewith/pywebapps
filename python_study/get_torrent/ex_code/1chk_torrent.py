
import re
import urllib.request
import http.client
import requests


DEBUG = 1
def debug(msg, mode=0):
    if (mode >0):
        print(msg)


def http_get(url, fn=2):
    #url = 'http://www.example.com'
    status_code = 0
    try :
        if (fn == 1) :
            status_code = urllib.request.urlopen(url).getcode()
        elif ( fn == 2) :
            request_response = requests.head(url)
            status_code = request_response.status_code
        else:
            conn = http.client.HTTPConnection(url)
            conn.request("HEAD", "/")
            response = conn.getresponse()
            status_code = response.status # response.reason (OK)
    except:
        print(">> http_get (exceprotn) ", url, status_code)
    finally:
        print(">> http_get (finally) ", url, status_code)
    return status_code

def check_url(url, idx):
    url_tmp = url
    idx_tmp = int(idx)
    for i in range(15):
        idx_tmp = int(idx) + i
        url_tmp = url.replace(str(idx), str(idx_tmp))
        print(">> check_url 1: ", url_tmp, idx_tmp)
        status_code = http_get(url_tmp)
        print(">> check_url 2: ", url_tmp, idx_tmp, status_code)

        if status_code == 200 :
            status = True
            url = url_tmp
            break
        else:
            status = False
    return (url, status, status_code)

def find_url(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


url_list=[ "토렌트와이 https://www.torrentwhy40.xyz/ ▶★★★★최신 TOP10", \
"토다와   https://www.토다와.net ▶★★★★ TOP10",\
"토렌트큐큐 https://torrentqq233.com/ ▶ ★★★★★",\
"토렌트모드 https://torrentmode18.com/ ▶ ★★★★★",\
"토렌트 릴 https://www.torrentreel5.site/home.php ▶ ★★★★ 인기자료",\
"토렌트모바일 https://torrentmobile77.com/ ▶ ★★★★",\
"KTX토렌트 https://ktxtorrent63.com/ ▶★★★★ TOP10",\
"토렌트썸 https://torrentsome66.com/ ▶  ★★인기자료",\
"토렌트알지 https://torrentrj65.com/ ▶ ★★★ 인기자료",\
"토렌트썰  https://torrentsir83.com/ ▶ ★★★ 인기자료",\
"토렌트TT https://torrenttt52.com/ ▶★★★ 넷플릭스, 드라마",\
"토렌트 맥스 https://t41.tormax.me/ ▶★★★ 미드",\
"티프리카 https://www.tfreeca22.com/home.php ▶ ★★★★ TOP11",\
"토렌트밤 https://torrentbam51.com/ ▶ ★★★ 드라마넷 플릭스" ]

new_url_list = []
new_urls = []
for item in url_list:
    debug(item, DEBUG)
    #url = re.search("(https://[a-z./]{1,20})([0-9]{1,3})([a-z./]{1,})",url)
    urls = find_url(item)
    debug(urls[0], DEBUG)
    match = re.search("[0-9]{1,}", urls[0])

    if (match ):
        debug (match, DEBUG)
        idx_no = match.group()
    else:
        debug ("no match", DEBUG)
        idx_no = 0
    print(urls[0], idx_no)

    results = check_url(urls[0], idx_no)
    #         (url, status, status_code)

    print (urls[0], results[0], results[1])
    new_item =''
    if ( results[1] == True):
        new_item = item.replace(urls[0], results[0])
        new_url_list.append(new_item)
        new_urls.append(results[0])
    print (" >>> item", item, new_item)


print ("[END - status] ++++++++++++++++++++++++++++++")
print (new_url_list)

cnt = 0
print ("<h4 style='text-align: left;' data-ke-size='size20'>")
for item in new_url_list:
    #debug(item, DEBUG)
    print("<p><a href='%s' target='_blank' rel='noopener'><span>%d. %s</span></a></p>" % (new_urls[cnt], cnt+1, item))

    cnt += 1
print ("</h4>")
print ("[END] ++++++++++++++++++++++++++++++")