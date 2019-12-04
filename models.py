from peewee import *

DATABASE = SqliteDatabase('dates.sqlite')


class Date(Model):
    name = CharField()
    description = CharField()
    class Meta:
        # database_table = 'dates'
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Date], safe=True)
    print("TABLES Created")
    DATABASE.close()