from flask import Flask
from flask_cors import CORS
from os import environ

app = Flask(__name__)

if environ.get('DEBUG', False) == '1':
    print('Starting in debug mode...')
    app.debug = True

CORS(app)
