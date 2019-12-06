import os 
from peewee import *
from flask_login import UserMixin
#UserMixin gives our User class default features
#Mixins are smal classes that add some specific feature 
#UserMixin also always us to set up our session
from playhouse.db_url import connect #need this for heroku

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('dates.sqlite')


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()
    # userdates: []
    class Meta: 
        database_table = 'users'
        database = DATABASE

class Date(Model):
    date_id = IntegerField(primary_key=True)
    name = CharField()
    description = CharField()
    class Meta:
        database_table = 'dates'
        database = DATABASE

class Create(Model):
    name = CharField()
    description = CharField()
    user = ForeignKeyField(User, backref='userdates')
    class Meta:
        database_table = 'creates'
        database = DATABASE

# class DateRating(Model):
#     # Userdate.date.name = 'Bumper Cars'
#     # Create could be a star/save button -> Creates UserDate with 
#     # date = date clicked in front end and user = user who clicked it
#     user = ForeignKeyField(User, backref="userdates")
#     date = ForeignKeyField(Date)
#     liked = BooleanField()
#     class Meta:
#         database_table = 'dateratings'
#         database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Date, Create], safe=True)
    print("TABLES Created")
    DATABASE.close()