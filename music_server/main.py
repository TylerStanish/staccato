from flask import Flask

from .config import ProductionConfig
from music_server.db import get_database


def create_app():
    app = Flask(__name__)
    
    db = get_database()

    @app.before_request
    def before_request():
        db.connect()
    
    @app.after_request
    def after_request(res):
        db.close()
        return res


    return app

