from resources import api
from flask_marshmallow import Marshmallow
from f_app import app

ma = Marshmallow(app)

api.init_app(app)

if __name__ == '__main__':
    print('Starting in debug mode...')
    app.run(debug=True)
