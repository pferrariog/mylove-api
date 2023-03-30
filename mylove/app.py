from flask import Flask
from flask_migrate import Migrate

from mylove.blueprints.routes import bp_messages
from mylove.extensions.config import init_app
from mylove.extensions.config import load_extensions


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp_messages)

    init_app(app)
    load_extensions(app)

    Migrate(app, app.db)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port="5000", debug=True)
