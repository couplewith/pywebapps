# pyflask
python flash example


# flask http error handle

* http error codes

```
# 100
* 100 : 
* 200 : OK success 
* 300 : cache & redirect
* 301 :
* 302 :

# 400
* 400 : Bad Request : browser가 요청을 못함 
* 401 : Unauthorize : 인증이 요구되는 리소스에 접근할때 인증하지 않은 상태
* 403 : Forbiddend : 권한이 필요한 리소스에 접근 권한이 필요할때, 인증된 사용자가 접근 권한 없이 접근할때
* 404 : not found : 해당 리소스가 없음 
* 405 : Method Not Allowed : GET, POST 으로 리소스를 요청하고 웹프로그램이 접근을 허용하지 않을때

# 500
* 500 : Internal Server Error : 웹프로그램의 내부 오류 (ex 서블릿 엔진 java가 작동되지 않음)
* 501 : Not Implemented : 브라우저가 요청한 기능이 구현되지 않았을때 (리소스에 대해 지원할 수 없을 때 적절한 응답)
* 502 : Bad Gateway : 웹프로그램이 외부 서비스와 연동하면서 오류가 발생 했을때, Proxy )
* 503 : Service Unavailable : 서비스는 구현이 되어있지만 서비스를 사용할수 없을때 (다운되었거나 과부하된 서버 상태)
```

# route decorator를 이용한 사용자 오류 처리

   1. erorhandler decorator
* route 데코레이터와 같은 동장을 하는 errorhandler 데코레이터
```
   @app.errorhandler(404)
   def page_not_found(e):
       retrun render_templage('404.html'), 404
```

   2. abort decorator
* abort : Flask에서 에러를 발생 시키는 객체 
 -  abort(404) 라고 지정하면 서버에서 발생하는 404 에러가 발생됨
```
    @app.route('/')
    def route_main():
        abort(404)
        return render_template('main.html')
```

example) 사용자 세션 값 확인하여 오류 처리 하기 
```
@app.route('/add_message'), methods=['POST'])
def add_message():
   if 'user_id' not in session:
        abort(401)
```
    
