from flask import current_app as app, Response, request, g, redirect, url_for
from flask_oidc import OpenIDConnect
from okta.client import Client as UsersClient



app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = "yc9!N&nB8UBN7B"
oidc = OpenIDConnect(app)

client_config = {
                "orgUrl": "https://dev-9239130.okta.com",
                "token": "00--WuaKx41U62Dk4a7ugEz-cHRR20bbqUhWcI91uz"  
                }
okta_client = UsersClient(client_config)





@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
    else:
        g.user = None


# @app.route('/login', methods=['POST'])
# def login():
#     return 'success'


# @app.route('/register', methods=['POST'])
# def register():


# @app.route('/logout', methods=['POST'])
# def logout():

@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for(".index"))


@app.route("/logout")
def logout():
    oidc.logout()
    return redirect(url_for(".index"))

@oidc.require_login
@app.route("/index")
def index():
    return "Hello World!"