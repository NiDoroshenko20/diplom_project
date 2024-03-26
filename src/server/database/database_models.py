from peewee import Model, CharField, IntegerField, ForeignKeyField
from peewee import *  
import sys

sys.path.append('C:/Beauty_studio_data_base')

import settings


db = SqliteDatabase(database=f'{settings.DATABASE_PATH}/{settings.DATABASE_NAME}')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    position = CharField(default='')
    login = CharField(default='')
    password = CharField(default='')
    power_level = IntegerField(default=0)

class Workers(BaseModel):
    post_id = IntegerField(default=0)
    name = CharField(default='')
    surname = CharField(default='')
    telephone_number = CharField(default='')

class Post(BaseModel):
    post = CharField(default='')

class Services(BaseModel):
    name = CharField(default='')
    price = CharField(default='')
    description = CharField(default='')

class Client(BaseModel):
    name = CharField(default='')
    address = CharField(default='')
    telephone_number = CharField(default='')

class Visits(BaseModel):
    visit_id = IntegerField(default=0)
    client_id = IntegerField(default=0)
    service_id = IntegerField(default=0)
    worker_id = IntegerField(default=0)
    datetime = CharField(default='')

db.create_tables([User, Workers, Post, Services, Client, Visits])
    