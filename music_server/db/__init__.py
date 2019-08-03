from peewee import PostgresqlDatabase

from music_server.utils import get_config


_database = None

def get_database():
    global _database
    if _database:
        return _database
    conf = get_config()
    db_conf = {
        'dbname': conf.DB.DBNAME,
        'user': conf.DB.USER,
        'password': conf.DB.PASSWORD,
        'host': conf.DB.HOST
    }
    if conf.DB.VENDOR == 'postgres':
        _database = PostgresqlDatabase(
            **db_conf
        )
    
    return _database
