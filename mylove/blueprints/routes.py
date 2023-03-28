from datetime import datetime

from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import request

from mylove.extensions.database import Love_messages
from mylove.extensions.serializer import LoveMessageSchema

bp_messages = Blueprint("love_messages", __name__, url_prefix="/api")


@bp_messages.route("/", methods=["GET"])
def love():
    return jsonify({"message": "popo i love you"})


@bp_messages.route("/lovemessages", methods=["GET"])
def get_love_messages():
    love_schema = LoveMessageSchema(many=True)
    love_messages = Love_messages.query.all()
    return love_schema.jsonify(love_messages), 200


@bp_messages.route("/sendlove", methods=["GET", "POST"])
def send_love_to_my_babe():
    love_schema = LoveMessageSchema()
    request.json["date"] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    message = love_schema.load(request.json)
    current_app.db.session.add(message)
    current_app.db.session.commit()
    return jsonify({"message": "love sended"}), 201


@bp_messages.route("/lovemessages/<id>", methods=["PUT"])
def update_love_message(id):
    love_schema = LoveMessageSchema()
    query = Love_messages.query.filter(Love_messages.id == id)
    query.update(request.json)
    current_app.db.session.commit()

    return love_schema.jsonify(query.first())


@bp_messages.route("/lovemessages/<id>", methods=["DELETE"])
def delete_love_message(id):
    Love_messages.query.filter(Love_messages.id == id).delete()
    current_app.db.session.commit()

    return jsonify({"message": "message deleted :c"})