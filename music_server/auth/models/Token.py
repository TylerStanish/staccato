import peewee

from db import get_base_model


class Token(get_base_model()):
    token = peewee.TextField()
