from base64 import b64encode
import logging
import os
import secrets

from auth.models import Token
from db import get_database


def generate_token():
    env = os.environ.get('FLASK_ENV')
    if not env:
        print("FLASK_ENV not set. I don't know which database you want to create a token for")
        return
    tok_str = secrets.token_urlsafe(64)
    Token.create(token=tok_str)
    print(tok_str)


if __name__ == '__main__':
    generate_token()
