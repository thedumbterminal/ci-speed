from resources import api
from flask_restx import Api


def test_resources():
    assert isinstance(api, Api)
