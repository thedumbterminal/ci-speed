from resources import api
from flask_marshmallow import Marshmallow
from f_app import app
from oauth_blueprint import blueprint
from models import security, user_datastore

ma = Marshmallow(app)

api.init_app(app)

app.register_blueprint(blueprint, url_prefix="/oauth")

security.init_app(app, user_datastore)


@app.cli.command()
def routes():
    'Display registered routes'
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        route = '{:50s} {:25s} {}'.format(rule.endpoint, methods, str(rule))
        print(route)
