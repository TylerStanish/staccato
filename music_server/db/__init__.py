from peewee import PostgresqlDatabase, SqliteDatabase

from utils import get_config


_database = None
_base_model = None

def get_database():
    global _database
    if _database:
        return _database
    conf = get_config()
    db_conf = {
        'database': conf.DB.DBNAME,
        'user': conf.DB.USER,
        'password': conf.DB.PASSWORD,
        'host': conf.DB.HOST
    }
    if conf.DB.VENDOR == 'postgres':
        _database = PostgresqlDatabase(
            **db_conf
        )
    elif conf.DB.VENDOR == 'sqlite':
        _database = SqliteDatabase(
            **db_conf
        )
    
    return _database


def get_base_model():
    global _base_model
    if not _base_model:
        class BaseModel(peewee.Model):
            class Meta:
                database = get_database()
        _base_model = BaseModel
    return _base_model

