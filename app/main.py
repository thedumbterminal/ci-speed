from resources import api
from flask_marshmallow import Marshmallow
from f_app import app
from flask_dance.contrib.github import make_github_blueprint


ma = Marshmallow(app)

api.init_app(app)

github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/oauth")

@app.cli.command()
def routes():
    'Display registered routes'
    rules = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        rules.append((rule.endpoint, methods, str(rule)))

    sort_by_rule = operator.itemgetter(2)
    for endpoint, methods, rule in sorted(rules, key=sort_by_rule):
        route = '{:50s} {:25s} {}'.format(endpoint, methods, rule)
        print(route)
