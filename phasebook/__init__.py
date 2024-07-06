from flask import Flask
import logging

from . import match, search, length
from .api import call_api, schedule

from phasebook.data.match_data import MATCHES

def create_app():
    app = Flask(__name__)
    logging.basicConfig(level=logging.DEBUG)
    # logger = logging.getLogger(__name__) call this on the different files
    app.logger.setLevel(logging.DEBUG)

    @app.route("/")
    def hello():
        # logger.debug("test")
        return "Hello World!"

    app.register_blueprint(match.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(length.bp)
    app.register_blueprint(call_api.bp)
    app.register_blueprint(schedule.bp)



    return app
