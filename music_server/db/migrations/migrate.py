import importlib
import sys

from config import TestingConfig, ProductionConfig, DevConfig

from playhouse.migrate import PostgresqlDatabase


def main(mode, up_down, version):
    if not mode:
        print('missing mode arg')
        exit(1)
    if not up_down:
        print('missing up or down arg')
        exit(1)
    if mode == 'testing':
        database = PostgresqlDatabase(
            TestingConfig.DB.DBNAME,
            user=TestingConfig.DB.USER,
            host=TestingConfig.DB.HOST,
            password=TestingConfig.DB.PASSWORD,
        )
    elif mode == 'development':
        database = PostgresqlDatabase(
            DevConfig.DB.DBNAME,
            user=DevConfig.DB.USER,
            host=DevConfig.DB.HOST,
            password=DevConfig.DB.PASSWORD
        )
    elif mode == 'production':
        print('WARNING: You do not have any production migration set up!')
        pass
    else:
        print('Did not specify correct parameter for mode')
        exit(1)
    if up_down == 'up':
        mod = importlib.import_module(version)
        mod.up(database)
    elif up_down == 'down':
        mod = importlib.import_module(version)
        mod.down(database)
    else:
        print('Did not specify "up" or "down" for mode')

if __name__ == '__main__':
    main(*sys.argv[1:])
