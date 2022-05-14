from flask import Flask
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app, supports_credentials=True, origins=[
    'http://localhost:5000',
    'http://localhost:3000',
    'https://thedumbterminal.github.io/ci-speed-ui/'
])

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "reallysecret")
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
