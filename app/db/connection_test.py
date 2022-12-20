from db.connection import db
from flask_sqlalchemy import SQLAlchemy


def test_db():
    assert isinstance(db, SQLAlchemy)
