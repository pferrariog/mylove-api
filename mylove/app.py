from flask import Flask

from mylove.blueprints.routes import bp_messages
from mylove.extensions.config import init_app
from mylove.extensions.config import load_extensions

app = Flask(__name__)
app.register_blueprint(bp_messages)

init_app(app)
load_extensions(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
