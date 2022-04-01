from resources import api
from flask_marshmallow import Marshmallow
from f_app import app
from db import db

ma = Marshmallow(app)

api.init_app(app)

print('Building DB tables...')
db.create_all()

if __name__ == '__main__':
    print('Starting in debug mode...')
    app.run(debug=True)
