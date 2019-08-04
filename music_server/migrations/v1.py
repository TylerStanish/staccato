from playhouse.migrate import PostgresqlMigrator, migrate

from auth.models import Token


def up(db):
    with db.atomic():
        migrator = PostgresqlMigrator(db)
        db.create_tables([Token])


def down(db):
    with db.atomic():
        migrator = PostgresqlMigrator(db)
        db.drop_tables([Token])
