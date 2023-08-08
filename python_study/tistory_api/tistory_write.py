import requests
import os, json
from dotenv import load_dotenv

# client_id == app_id
load_dotenv()
client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")
access_token = os.environ.get("access_token")
redirect_uri = os.environ.get("redirect_uri")


# 인증 요청 및 Authentication code 발급
# https://tistory.github.io/document-tistory-apis/auth/authorization_code.html
def getAuthenticationCode():
    response_type = "code"
    state = "anything"

    url = "https://www.tistory.com/oauth/authorize?" + \
          "client_id=" + client_id + "&" + \
          "redirect_uri=" + redirect_uri + "&" + \
          "response_type=" + response_type + "&" + \
          "state=" + state
    return url

# Access Token 발급
# https://tistory.github.io/document-tistory-apis/auth/authorization_code.html
def getAccessToken():
    code = "9d456e72dbe8fd3b468310028a3055d0212632b25d7c0da2e7beacdee67b830e74132cdd"
    grant_type = "authorization_code"

    url = "https://www.tistory.com/oauth/access_token?" + \
          "client_id=" + client_id + "&" + \
          "client_secret=" + client_secret + "&" + \
          "redirect_uri=" + redirect_uri + "&" + \
          "code=" + code + "&" + \
          "grant_type=" + grant_type

    res = requests.get(url)
    return res

# 자신의 블로그 정보
# https://tistory.github.io/document-tistory-apis/apis/v1/blog/list.html
def BlogInfo(output_type="xml"):
    url = "https://www.tistory.com/apis/blog/info?" + \
          "access_token=" + access_token + "&" + \
          "output=" + output_type
    res = requests.get(url).content
    print("getBLogInfo : ", url)
    return json.loads(res)

# 글 목록
# https://tistory.github.io/document-tistory-apis/apis/v1/post/list.html
def PostList(blog_name, page=1, output='xml'):
    url = "https://www.tistory.com/apis/post/list?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output + "&"
    url += "blogName=" + blog_name + "&"
    url += "page=" + str(page) + "&"
    res = requests.get(url).content
    print("getPostList : ", url)
    return json.loads(res)

# 글 읽기
# https://tistory.github.io/document-tistory-apis/apis/v1/post/read.html
def PostRead(blog_name,post_id):
    url = "https://www.tistory.com/apis/post/read?"
    url += "access_token=" + access_token + "&"
    #url += "output=" + output + "&"
    url += "blogName=" + blog_name + "&"
    url += "postId=" + str(post_id) + "&"
    res = requests.get(url).content

    print("getPostRead : ", url)
    return json.loads(res)

# 글 작성
# https://tistory.github.io/document-tistory-apis/apis/v1/post/write.html
def postWrite(blog_name, title, content="", visibility=None, category_id=None, published=None, slogan=None, tag=None,
              acceptComment=None, password=None, output_type="json"):
    url = "https://www.tistory.com/apis/post/write?"
    data = {}
    data['access_token'] = access_token
    data['output'] = output_type
    data['blogName'] = blog_name
    data['title'] = title
    data['content'] = content
    #url += "access_token=" + access_token + "&"
    #url += "output=" + output_type + "&"
    #url += "blogName=" + blog_name + "&"
    #url += "title=" + title + "&"
    #url += "content=" + content + "&"
    if visibility is not None:
        url += "visibility=" + visibility + "&"
    if category_id is not None:
        url += "category=" + category_id + "&"
    if published is not None:
        url += "published=" + published + "&"
    if slogan is not None:
        url += "slogan=" + slogan + "&"
    if tag is not None:
        url += "tag=" + tag + "&"
    if acceptComment is not None:
        url += "acceptComment=" + acceptComment + "&"
    if password is not None:
        url += "password=" + password
    #data += "category=" + "1024642"
    res = requests.post(url, data=data).content
    return json.loads(res)

# 글 수정
# https://tistory.github.io/document-tistory-apis/apis/v1/post/modify.html
def postModify(blog_name, title, content="", visibility=0, category_id=0, published=None, slogan=None, tag=None,
              acceptComment=1, password=None, output_type="xml"):
    url = "https://www.tistory.com/apis/post/modify?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output_type + "&"
    url += "blogName=" + blog_name + "&"
    url += "title=" + title + "&"
    url += "content=" + content + "&"
    url += "visiblility=" + visibility + "&"
    url += "category=" + category_id + "&"
    url += "published=" + published + "&"
    url += "slogan=" + slogan + "&"
    url += "tag=" + tag + "&"
    url += "acceptComment=" + acceptComment + "&"
    url += "password=" + password + "&"

# 파일 첨부
# https://tistory.github.io/document-tistory-apis/apis/v1/post/attach.html
#tageturl은 api 문서에 없는데 이걸 넣어야지 썸네일 자동등록됨
def postAttach(blog_name, file_name=None):
    url = "https://www.tistory.com/apis/post/attach?"
    url += "access_token=" + access_token + "&"
    url += "blogName=" + blog_name + "&"
    url += 'targetUrl' + blog_name + "&"
    url += "output=json"
    file = dict(uploadedfile=open(file_name, 'rb'))
    res = requests.post(url, files=file).content
    print("postAttach : ", url)

    return json.loads(res)

# 카테고리
# https://tistory.github.io/document-tistory-apis/apis/v1/category/list.html
def CategoryList(blog_name, output='xml'):
    url = "https://www.tistory.com/apis/category/list?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output + "&"
    url += "blogName=" + blog_name

    print("getCategoryID : ", url)
    res = requests.get(url).content
    return json.loads(res)

# 최근 댓글 목록
# https://tistory.github.io/document-tistory-apis/apis/v1/comment/recent.html
def CommentNewest(blog_name, page=1, count=10, output_type="xml"):
    url = "https://www.tistory.com/apis/comment/newest?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output_type + "&"
    url += "blogName=" + blog_name + "&"
    url += "page=" + page + "&"
    url += "count=" + count

    print("getCommentNewest : ", url)
    res = requests.get(url).content
    return json.loads(res)

# 댓글 목록
# https://tistory.github.io/document-tistory-apis/apis/v1/comment/list.html
def CommentList(blog_name, post_id, output_type="xml"):
    url = "https://www.tistory.com/apis/comment/list?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output_type + "&"
    url += "blogName=" + blog_name + "&"
    url += "page=" + post_id

    print("getCommentList : ", url)
    res = requests.post(url).content
    return json.loads(res)

# 댓글 작성
# https://tistory.github.io/document-tistory-apis/apis/v1/comment/write.html
def CommentWrite(blog_name, post_id, parent_id, content, secret=0, output_type="xml"):
    url = "https://www.tistory.com/apis/comment/write?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output_type + "&"
    url += "blogName=" + blog_name + "&"
    url += "page=" + post_id + "&"
    url += "parentId="+parent_id + "&"
    url += "content="+content + "&"
    url += "secret="+secret

    print("CommentWrite : ", url)
    res = requests.post(url).content
    return json.loads(res)

# 댓글 수정
# https://tistory.github.io/document-tistory-apis/apis/v1/comment/modify.html
def CommentModify(blog_name, post_id, comment_id, content, secret=0, output_type="xml"):
    url = "https://www.tistory.com/apis/comment/modify?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output_type + "&"
    url += "blogName=" + blog_name + "&"
    url += "page=" + post_id + "&"
    url += "commentId=" + comment_id + "&"
    url += "content=" + content + "&"
    url += "secret=" + secret

    print("CommentNodify : ", url)
    res = requests.post(url).content
    return json.loads(res)

# 댓글 삭제
# https://tistory.github.io/document-tistory-apis/apis/v1/comment/delete.html
def CommentDelete(blog_name, post_id, comment_id, output_type="xml"):
    url = "https://www.tistory.com/apis/comment/modify?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output_type + "&"
    url += "blogName=" + blog_name + "&"
    url += "page=" + post_id + "&"
    url += "commentId=" + comment_id + "&"

    print("CommentDelete : ", url)
    res = requests.post(url).content
    return json.loads(res)