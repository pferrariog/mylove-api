from datetime import datetime

from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import request
from marshmallow import ValidationError

from mylove.extensions.database import LoveMessages
from mylove.extensions.serializer import LoveMessageSchema

bp_messages = Blueprint("love_messages", __name__, url_prefix="/api")


@bp_messages.route("/", methods=["GET"])
def love():
    return jsonify({"message": "popo i love you"})


@bp_messages.route("/lovemessages", methods=["GET"])
def get_love_messages():
    love_schema = LoveMessageSchema(many=True)
    love_messages = LoveMessages.query.all()
    return love_schema.jsonify(love_messages), 200


@bp_messages.route("/sendlove", methods=["GET", "POST"])
def send_love_to_my_babe():
    love_schema = LoveMessageSchema()
    request.json["date"] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    try:
        message = love_schema.load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400
    except Exception as unknown_error:
        return jsonify(unknown_error.messages), 500

    current_app.db.session.add(message)
    current_app.db.session.commit()
    return jsonify({"message": "love sended"}), 201


@bp_messages.route("/lovemessages/<id>", methods=["PUT"])
def update_love_message(id):
    love_schema = LoveMessageSchema()
    query = LoveMessages.query.get_or_404(id, description="message not found")
    query.update(request.json)
    current_app.db.session.commit()

    return love_schema.jsonify(query.first()), 200


@bp_messages.route("/lovemessages/<id>", methods=["DELETE"])
def delete_love_message(id):
    LoveMessages.query.filter(LoveMessages.id == id).delete()
    current_app.db.session.commit()

    return jsonify({"message": "message deleted :c"}), 200
