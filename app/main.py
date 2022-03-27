from flask import Flask
from resources import api
# from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

# db = SQLAlchemy(app)
ma = Marshmallow(app)

api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
