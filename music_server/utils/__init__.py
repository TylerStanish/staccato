import os


def get_config():
    from config import Config, DevConfig, ProductionConfig, TestingConfig
    env = os.environ['FLASK_ENV']
    if env == 'development':
        return DevConfig
    elif env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig


def read_from_file(filename: str, default: str='') -> str:
    if not os.path.exists(filename):
        return default
    with open(filename) as f:
        return f.read()
