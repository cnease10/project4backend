from peewee import *
from flask_login import UserMixin
#UserMixin gives our User class default features
#Mixins are smal classes that add some specific feature 
#UserMixin also always us to set up our session
DATABASE = SqliteDatabase('dates.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()
    class Meta: 
        database = DATABASE

class Date(Model):
    username = CharField()
    description = CharField()
    class Meta:
        # database_table = 'dates'
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Date], safe=True)
    print("TABLES Created")
    DATABASE.close()