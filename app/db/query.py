from db.connection import db
from sqlalchemy.sql import text


def query(sql, values):
    result = db.session.execute(text(sql), values)
    return result.mappings().all()
