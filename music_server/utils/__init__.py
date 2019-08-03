import os

from music_server.config import Config, DevConfig, ProductionConfig, TestingConfig


def get_config():
    env = os.environ['FLASK_ENV']
    if env == 'development':
        return DevConfig
    elif env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
