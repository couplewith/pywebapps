
import os  # for checking file existence
import sys  # for handling errors
import re
import requests
import urllib.request
import http.client
from io import StringIO
from datetime import datetime

import requests


DEBUG = 1
def debug(msg, mode=0):
    if (mode > 0):
        print(msg)


def http_get(url, fn=2):
    #url = 'http://www.example.com'
    status_code = 0
    try:
        if fn == 1:
            status_code = urllib.request.urlopen(url).getcode()
        elif fn == 2:
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

    status = False
    status_code = None
    for i in range(15):
        idx_tmp = int(idx) + i
        url_tmp = url.replace(str(idx), str(idx_tmp))
        print(">> check_url 1: ", url_tmp, idx_tmp)
        status_code = http_get(url_tmp)
        #response = requests.get(url_tmp)
        #status_code = response.status_code
        print(">> check_url 2: ", url_tmp, idx_tmp, status_code)

        if (status_code in [200, 301, 302] ):
            status = True
            url = url_tmp
            break
        elif (status_code in [403] ):
            if url.find('토다와'):
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

def read_file_into_list(filename):
    if not os.path.exists(filename):
        print(f"Error: file '{filename}' does not exist")
        return None

    try:

        with open(filename, 'r', encoding='utf-8') as file:
            #lines = file.readlines()
            lines = [line.strip() for line in file.readlines()]
            print (lines)

    except UnicodeDecodeError:
        print(f"Error: could not read file '{filename}' as UTF-8")
        return None

    return lines


def list_to_html_data(new_url_list):

    # convert to string
    now = datetime.now()
    date_time_str = now.strftime("%Y.%m.%d")

    html_buffer = StringIO()
    html_buffer.write('<html><head><title>torrent update</title></head>\n')
    html_buffer.write('<body>\n')
    html_buffer.write('<h2 style="text-align: left;" data-ke-size="size26">')
    html_buffer.write('<b>주요 토렌트 순위 {} updated</b><br>'.format(date_time_str))
    html_buffer.write('</h2>\n')

    cnt = 0
    color_lst = ["#F44336", "#3D62CE", "#78909C", "#42A5F5",  "#9CCC65", "#FFCA28"]
    for item in new_url_list:
        html_buffer.write('<h4 data-ke-size="size20"><b>')
        idx = cnt // 5
        color = color_lst[idx]
        html_buffer.write('<a href="{}" target="_blank" rel="noopener">'.format(new_urls[cnt]))
        html_buffer.write('<span style="color: {};">{}. {}</span>'.format(color, cnt + 1, item))
        html_buffer.write('</a>')
        html_buffer.write('</b></h4>\n')

        if(cnt % 5 == 4) :
            html_buffer.write('<br/>\n')
        cnt = cnt+1
    html_buffer.write('</body></html>')
    return html_buffer


def write_stringbuffer(buffer, filename='torrent_update.html'):
    with open(filename, 'w') as f:
        f.write(buffer.getvalue())
    f.close()


def write_listdata(listdata, filename='new_torrent_sites.txt'):
    cnt = 0
    with open(filename, 'w') as f:
        for item in listdata:
            f.write(item + '\n')
            cnt = cnt+1
        f.close()
    return cnt

#----------------------------------------------

file_site_list ='torrent_sites.txt'
url_list = read_file_into_list(file_site_list)

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

buffer = list_to_html_data(new_url_list)

write_stringbuffer(buffer, 'data/torrent_update.html')
write_listdata(new_url_list, 'data/new_torrent_sites.txt')

print ("[END] ++++++++++++++++++++++++++++++")