from resources import api
from flask_marshmallow import Marshmallow
from f_app import app
from oauth_blueprint import blueprint
from models import security, user_datastore
from db import db
from requests import get
import os

ma = Marshmallow(app)

api.init_app(app)

app.register_blueprint(blueprint, url_prefix="/oauth")

security.init_app(app, user_datastore)


ui_url_base = os.environ.get("UI_URL_BASE", "http://localhost:3000/")
ui_url_path = os.environ.get("UI_URL_PATH", "")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    #print('requested:', path)
    if path == '':
        path = ui_url_path
    new = f'{ui_url_base}{ui_url_path}{path}'
    print('Proxy to:', new)
    return get(new).content

@app.route('/static/js/<path:path>')
def static_proxy(path):
    new = f'{ui_url_base}{ui_url_path}static/js/{path}'
    print('Proxy to:', new)
    return get(new).content


@app.cli.command()
def routes():
    'Display registered routes'
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        route = '{:50s} {:25s} {}'.format(rule.endpoint, methods, str(rule))
        print(route)

@app.cli.command()
def cleardb():
    'Drop all db tables'
    db.drop_all()
