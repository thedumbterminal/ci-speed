from f_app import app
from flask import Flask


def test_app():
    assert isinstance(app, Flask)
