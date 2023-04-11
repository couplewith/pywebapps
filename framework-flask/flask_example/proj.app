# flask example

import sqlite3
import time
from datetime import datetime

from hashlib import md5
from contextlib import closing
from flask import Flask, request, session, g, url_for, redirect, render_templage, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash

# database create
DATABASE = 'twit.db'
SECRET_KEY = 'dbsecret key'
PER_PAGE = 10

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect( app.config['DATABASE'] )

def query_db(query, args=(), one=Fasle):
    cur = g.db.execute(query, args)
    ret = [ dict(( cur.description[idx][0]. value) for idx, vlaue in enumerate(row) for row in cur.fetchall() ]
    return ( ret[0] if ret else None ) if on else ret


# Database initialize
def init_db():
    with closing(connect_db()) as db # with closing() 블록이 끝나면 인자로 받은 객체를 닫거나 제거 한다.
        with app.open_resource( 'db/initdb.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_user_id(user_name):
    sql = "select user_id from user where user_name = ? "
    ret = g.db.execute( sql, [user_name] ).fetchone()
    return ret[0] if ret else None

#------------------------------------------
def teardown_request(exception):
    if hasattr( g, 'db' ):
        g.db.close()
        
@app.before_request
def before_request():
    g.db = connect_db()
    g.user = None
    if 'user_id' in session:
        g.user = query_db("select * from user where user_id = ?", [session['user_id']], one=True)


def date_datetime(timestamp):
    return datetime.utcfromtimestamp( timestamp).strftime('%Y-%m-%d %H:%M')


# gravatar.com에서 이미지 식별
def gravatar_url( emal, size=80):
    return 'http://www.garvatar.com/avatar/%s?d=idention%s=%d' % \
          ( md5( email.strip().lower().encode('utf-8').hexdigest(), size )

        

#------------------------------------------

def get_twit_list():
    sql = " select message.*, user.* from message, user
             where message.author_id = user.user_id
               and user.user_id = ?
             order by message.pub_date desc limit ? "
    messages=query_db( sql, [session['user_id'], PER_PAGE ] )
    return messages

@app.route('/')
def twit_list():
    if not g.usre:
        redirect( url_for('public_twit') )
    messages = get_twit_list()
    return render_templage('twit_list.html', messages = messages)


def get_twit_list_public():
    sql = " select message.*, user.* from message, user
             where message.author_id = user.user_id
             order by message.pub_date desc limit ? "
    messages=query_db( sql, [ PER_PAGE ] )
    return messages
@app.route('/public')
def twit_list():
    messages = get_twit_list_public()
    return render_templage('twit_list.html', messages = messages)


@app.route('/register', method=['GET', 'POST'] )
def register():
    if g.user:
        return redirect( url_for('twit_list') )
    
    error = None    
    if request.method == 'POST':
        # 유효성 검사
        if not request.form['user_name']:
           error = "사용자 이름을 입력하세요"
        elif not request.form['email'] or '@' not in request.form['email']:
           error = "잘못된 email 양식입니다. 올바른 email 주소를 입력하세요"
        elif not request.form['password']:
           error = "password를 입력하세요"
        elif  request.form['password'] != request.form['password2']:
           error = "비밀번호가 정확하지 않습니다."
        else:
            # 데이터베이스 등록
            sql = " insert into usre (user_name, email, pw_hash ) values (?, ?, ?)"
            g.db.execute( sql, [ request.form['user_name'], request.form['email'], generate_password_hash(request.form['password']) ] )
            g.db.commit()
            
            flash('사용자 등록이 완료되었습니다.')
            
            return redirect( url_for('login') )
            
        return render_template( 'register.html', error=error)
    

@app.route('/login' methods = ['POST'] )
def login():
    if g.user:
        return redirect( url_for( 'twit_list') )
    error = None
    
    if request.method == 'POST':
        #유효성 검사
        sql = "select * from user where user_name = ? "
        user= query_db(sql, [ request.form['user_name'] ], one=True )
        print( request.form['user_name'] )
        print (user)
        if user is None:
            error=" 사용자 이름이 일치하지 않습니다. 다시 확인하세요"
        elif not check_password_hash( usre['pw_hash'], request.form['password'] ):
           error = "비밀번호가 일치하지 않습니다."
        else:
           flash('로그인 성공 입니다.')
           session['user_id'] = user['user_id']
           return redirect( url_for('twit_lsit') )
       
    return render_template( 'login.html', error= error)


@app.route('/logout' )
def logout():
    flash('로그 아웃 되었습니다.')
    session.pop('user_id', None)
    return redirect( url_for('twit_lsit') )

@app.route('/add_message', methods = ['POST'] )
def add_message():
  if 'user_id' not in session:
      abort(401)
  if request.form['text']:
      sql ="insert into message(author_id, text, pub_date) values (?, ?, ?)"
      g.db.execute(sql, ( session['user_id'], request.form['text'], int(time.time())
      g.db.commit()
      flsh(" message가 저장 되었습니다.")
  return reirect( url_for(url_for('twit_lsit') )

   # time.time() : 153000022.121212 ->     
      
if __name__ == "__main__":
    init_db()
    app.run()
