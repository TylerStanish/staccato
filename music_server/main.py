from http import HTTPStatus

from flask import Flask, request, jsonify

from auth.models import Token
from config import ProductionConfig
from db import get_database
from utils import get_token_from_authorization_header
from utils.exceptions import BadRequestException


def create_app():
    app = Flask(__name__)
    
    db = get_database()

    @app.before_request
    def before_request():
        db.connect()
        # TODO authenticate all requests here
        # TODO don't forget to cache, and don't forget to invalidate cache upon token destruction/modification
        query = Token.select().where(Token.token == get_token_from_authorization_header(request.headers.get('Authorization')))
        if not query.exists():
            raise BadRequestException('Invalid token')
    
    @app.after_request
    def after_request(res):
        db.close()
        return res

    @app.route('/')
    def sanity():
        return 'hi'
    
    @app.errorhandler(BadRequestException)
    def handle_bad_request_exception(e: BadRequestException):
        return jsonify({
            'error': str(e)
        }), HTTPStatus.BAD_REQUEST

    @app.errorhandler(Exception)
    def catchall_exceptions(e: Exception):
        return jsonify({
            'error': str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

    return app

