from f_app import app
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate

default_dsn = "postgresql://myusername:mypassword@localhost:5432/myusername"

configured_dsn = os.environ.get('DATABASE_URL', default_dsn)
configured_dsn = configured_dsn.replace('postgres:', 'postgresql:', 1) # Support heroku default DSNs

app.config["SQLALCHEMY_DATABASE_URI"] = configured_dsn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
