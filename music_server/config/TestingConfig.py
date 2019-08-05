from .BaseConfig import Config
from utils import read_from_file


class TestingConfig(Config):
    DEBUG = True
    TESTING = True

    class DB(Config.DB):
        USER = 'tyler'
        PASSWORD = read_from_file('secret/test_db_password')
        HOST = 'localhost'
        DBNAME = 'staccato-testing'
