import os

from .exceptions import BadRequestException


def get_config():
    from config import Config, DevelopmentConfig, ProductionConfig, TestingConfig
    env = os.environ['FLASK_ENV']
    if env == 'development':
        return DevelopmentConfig
    elif env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig


def read_from_file(filename: str, default: str='') -> str:
    if not os.path.exists(filename):
        return default
    with open(filename) as f:
        return f.read()


def get_token_from_authorization_header(auth_header: str) -> str:
    if auth_header is None:
        return ''
    split_res = auth_header.split(' ')
    if len(split_res) != 2:
        raise BadRequestException('Invalid Authorization header')
    return split_res[1]
