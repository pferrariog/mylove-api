from flask_marshmallow import Marshmallow

from .database import Love_messages

marsh = Marshmallow()


def init_app(app):
    marsh.init_app(app)
    app.marsh = marsh


class LoveMessageSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Love_messages
        load_instance = True
