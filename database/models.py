from peewee import *
db = SqliteDatabase('database/history.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    chat_id = IntegerField(unique=True)
    username = CharField()
    full_name = TextField(null=True)


class Query(BaseModel):
    user_id = ForeignKeyField(User, backref='queries', on_delete='CASCADE')
    date_time = DateTimeField()
    input_city = CharField()
    destination_id = CharField()
    photo_need = BooleanField()
    response_id = IntegerField(null=True)


class Response(BaseModel):
    query_id = ForeignKeyField(Query, backref='responses', on_delete='CASCADE')
    hotel_id = CharField()
    name = CharField()
    address = CharField()
    price = FloatField()
    distance = FloatField()


class Image(BaseModel):
    hotel_id = ForeignKeyField(Response, backref='images', on_delete='CASCADE')
    link = TextField()


with db:
    db.create_tables([User, Query, Response, Image])
