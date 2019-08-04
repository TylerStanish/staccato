from .BaseConfig import Config
from utils import read_from_file


class DevConfig(Config):
    class DB(Config.DB):
        USER = 'tyler'
        PASSWORD = read_from_file('secret/dev_db_password')
        DBNAME = 'staccato-dev'
        HOST = 'localhost'
