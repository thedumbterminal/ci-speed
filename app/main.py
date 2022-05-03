from resources import api
from flask_marshmallow import Marshmallow
from f_app import app
import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github

ma = Marshmallow(app)

api.init_app(app)


app.secret_key = os.environ.get("FLASK_SECRET_KEY", "reallysecret")
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")


@app.route("/test")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    return "You are @{login} on GitHub".format(login=resp.json()["login"])
