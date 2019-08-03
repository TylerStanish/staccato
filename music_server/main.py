from flask import Flask


def create_app(env: str):
    app = Flask(__name__)
    
    if config == 'development':
        pool = psycopg2.ThreadedConnectionPool(
            minconn=1,
            maxconn=8,
            dbname=DevelopmentConfig.DB.DBNAME,
            user=DevelopmentConfig.DB.USER,
            host=DevelopmentConfig.DB.HOST,
            password=DevelopmentConfig.DB.PASSWORD,
        )

    elif config == 'testing':
        pool = psycopg2.ThreadedConnectionPool(
            minconn=1,
            maxconn=8,
            dbname=TestingConfig.DB.DBNAME,
            user=TestingConfig.DB.USER,
            host=TestingConfig.DB.HOST,
            password=TestingConfig.DB.PASSWORD,
        )

    elif config == 'production':
        pool = psycopg2.ThreadedConnectionPool(
            minconn=1,
            maxconn=8,
            dbname=ProductionConfig.DB.DBNAME,
            user=ProductionConfig.DB.USER,
            host=ProductionConfig.DB.HOST,
            password=ProductionConfig.DB.PASSWORD,
        )


    @app.before_request
    def before_request():
        g.db = pool.getconn()
    
    @app.after_request
    def after_request():
        pool.putconn(g.db)


    return app

