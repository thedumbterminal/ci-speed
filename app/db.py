from f_app import app
from flask_sqlalchemy import SQLAlchemy
import os

default_dsn = "postgresql://myusername:mypassword@localhost:5432/myusername"

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', default_dsn)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
