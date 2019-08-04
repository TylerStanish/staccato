from flask import Flask, request

from auth.models import Token
from config import ProductionConfig
from db import get_database
from utils import get_token_from_authorization_header


def create_app():
    app = Flask(__name__)
    
    db = get_database()

    @app.before_request
    def before_request():
        db.connect()
        # TODO authenticate all requests here
        # TODO don't forget to cache, and don't forget to invalidate cache upon token destruction/modification
        query = Token.select().where(Token.token=get_token_from_authorization_header(request.headers.get('Authorization')))
        if not query.exists():
            raise Exception('Invalid token')
    
    @app.after_request
    def after_request(res):
        db.close()
        return res

    @app.route('/')
    def sanity():
        return 'hi'

    return app

