from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


@dataclass
class LoveMessages(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    message = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime)


def init_app(app):
    db.init_app(app)
    app.db = db
    with app.app_context():
        db.create_all()
