from flask import Flask

from config import ProductionConfig
from db import get_database


def create_app():
    app = Flask(__name__)
    
    db = get_database()

    @app.before_request
    def before_request():
        db.connect()
        # TODO authenticate all requests here
        # TODO don't forget to cache, and don't forget to invalidate cache upon token destruction/modification
    
    @app.after_request
    def after_request(res):
        db.close()
        return res

    @app.route('/')
    def sanity():
        return 'hi'

    return app

