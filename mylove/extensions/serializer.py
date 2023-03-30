from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from marshmallow import fields
from marshmallow import validates

from .database import LoveMessages

marsh = Marshmallow()


def init_app(app):
    marsh.init_app(app)
    app.marsh = marsh


class LoveMessageSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = LoveMessages
        load_instance = True

    message = fields.Str(required=True)

    @validates("id")
    def validate_id(self, value):
        raise ValidationError("Don't send the message id!")
