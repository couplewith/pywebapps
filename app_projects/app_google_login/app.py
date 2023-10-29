import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request
from flask import render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask("Google Login App")
app.secret_key = "CodeSpecialist.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "1080543750314-4tqcor45bikmjpmtejaoa3359pgjv52p.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "config/client_secret.json")

flow = Flow.from_client_secrets_file(
     client_secrets_file=client_secrets_file,
     scopes=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
     redirect_uri="http://127.0.0.1:5000/login/callback"
 )

DEBUG=1
def debug(msg,v1=None,v2=None,v3=None):
    if DEBUG > 0 :
        print("callback", msg, v1, v2, v3)



def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
    return wrapper

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    debug(">>login", authorization_url, session )
    return redirect(authorization_url)

@app.route("/login/callback")
def callback():
    #  Google로부터 받은 인증 응답을 사용하여 액세스 토큰 및 리프레시 토큰을 가져옵니다
    flow.fetch_token(authorization_response=request.url)


    # CSRF 공격을 방지하기 위해 상태(state)가 일치하지 않으면 500 상태 코드로 요청을 중단시킵니다.
    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    # flow.credentials를 사용하여 얻은 자격 증명(credentials)을 가져옵니다.
    #  이 자격 증명은 Google API와의 향후 요청에 사용됩니다.
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    debug(">>callback.credentials", credentials )
    debug(">>callback.id_info", id_info)
    debug(">>callback.token_request",token_request)
    debug(">>callback.cached",cached_session )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session['email'] = id_info.get("email")
    session['email_verified'] = id_info.get('email_verified')
    debug("redirect->protected_area", session)

    return redirect("/protected_area")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/")
def index():
    #return "Hello World <a href='/login'><button>Login</button></a>"
    return render_template("index.html")

@app.route("/protected_area")
@login_is_required
def protected_area():

    data = {
            'name': session.get("name"),
            'state': session.get("state"),
            'google_id' : session.get("google_id")
    }
    debug('>>protected_area', data, session)
    return render_template("protected_area.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
