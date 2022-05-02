from main import app
from os import environ

debug = environ.get('DEBUG', False) == '1'

if __name__ == "__main__":
    if debug:
        print('Starting in debug mode...')
    app.run(debug=debug)
