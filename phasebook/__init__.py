from flask import Flask

from . import match, search
from phasebook.data.match_data import MATCHES

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello World!"

    @app.route("/length")
    def length():
        return str(len(MATCHES))

    app.register_blueprint(match.bp)
    app.register_blueprint(search.bp)

    return app
