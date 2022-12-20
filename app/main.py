from resources import api
from flask_marshmallow import Marshmallow
from f_app import app
from oauth_blueprint import blueprint
from db.models import security, user_datastore
from db.connection import db
from requests import get
import os
from flask import make_response

ma = Marshmallow(app)

api.init_app(app)

app.register_blueprint(blueprint, url_prefix="/oauth")

security.init_app(app, user_datastore)


ui_url_base = os.environ.get("UI_URL_BASE", "http://localhost:3000/")
ui_url_path = os.environ.get("UI_URL_PATH", "")


def _proxy_request(url):
    print("Proxy to:", url)
    proxy_response = get(url)
    response = make_response(proxy_response.content)
    response.headers["Content-Type"] = proxy_response.headers["Content-Type"]
    return response


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def proxy(path):
    print("Original path: ", path)
    if path == "":
        path = ui_url_path
    new = f"{ui_url_base}{path}"
    return _proxy_request(new)


@app.route("/static/js/<path:path>")
def static_js_proxy(path):
    new = f"{ui_url_base}{ui_url_path}static/js/{path}"
    return _proxy_request(new)


@app.route("/static/media/<path:path>")
def static_media_proxy(path):
    new = f"{ui_url_base}{ui_url_path}static/media/{path}"
    return _proxy_request(new)


@app.route("/static/css/<path:path>")
def static_css_proxy(path):
    new = f"{ui_url_base}{ui_url_path}static/css/{path}"
    return _proxy_request(new)


@app.cli.command()
def routes():
    "Display registered routes"
    for rule in app.url_map.iter_rules():
        methods = ",".join(sorted(rule.methods))
        route = "{:50s} {:25s} {}".format(rule.endpoint, methods, str(rule))
        print(route)


@app.cli.command()
def cleardb():
    "Drop all db tables"
    db.drop_all()
