from flask import url_for
from pytest import fixture
from sqlalchemy.orm import close_all_sessions

from mylove.app import create_app


@fixture(scope="package")
def app():
    app = create_app()
    app.testing = True
    app_context = app.test_request_context()
    app_context.push()

    db = app.extensions["sqlalchemy"]
    db.drop_all()
    db.create_all()

    yield app

    db.session.close()
    close_all_sessions()


@fixture(scope="module")
def client(app):
    return app.test_client()


def test_register_message_in_database(client):
    message_body = {"message": "love you testing", "date": ""}

    expected = {
        "message": "love sended",
    }

    response = client.post(
        url_for("love_messages.send_love_to_my_babe"), json=message_body
    )

    assert response.status_code == 201
    assert response.json == expected


def test_json_must_have_message(client):
    message = {}

    expected = {"message": ["Missing data for required field."]}

    response = client.post(url_for("love_messages.send_love_to_my_babe"), json=message)

    assert response.status_code == 400
    assert response.json == expected


def test_messages_are_returned(client):
    expected = {"id": 1, "message": "love you testing"}

    response = client.get(url_for("love_messages.get_love_messages"))

    assert response.status_code == 200
    assert isinstance(response.json, (list, list[dict]))
    assert response.json[0]["message"] == expected["message"]
    assert response.json[0]["id"] == expected["id"]


def test_id_not_found(client):
    message = {"message": "luv testing"}

    mock_id = 2

    response = client.put(
        url_for("love_messages.update_love_message", id=mock_id), json=message
    )

    assert response.status_code == 404
    assert b"<p>message not found</p>" in response.data
