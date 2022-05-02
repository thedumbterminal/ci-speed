from resources import api
from flask_marshmallow import Marshmallow
from f_app import app
from os import environ

ma = Marshmallow(app)

api.init_app(app)

debug = environ.get('DEBUG', False) == '1'

if __name__ == '__main__':
    if debug:
        print('Starting in debug mode...')
    app.run(debug=debug)
