from unittest import TestCase

from flask import url_for

from mylove.app import create_app


class TestFlaskBase(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.drop_all()


class TestLoveMessagesBP(TestFlaskBase):
    def test_register_message_in_database(self):
        message_body = {"message": "love you testing", "date": ""}

        expected = {
            "message": "love sended",
        }

        response = self.client.post(
            url_for("love_messages.send_love_to_my_babe"), json=message_body
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, expected)

    def test_json_must_have_message(self):
        message = {}

        expected = {"message": ["Missing data for required field."]}

        response = self.client.post(
            url_for("love_messages.send_love_to_my_babe"), json=message
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, expected)
