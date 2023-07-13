from mongoengine import (
    StringField
)
from app.common.constants import STRING_LENGTH
from app.db.mongo.documents import Model


class Airline(Model):
    _id = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                       required=True)

    name = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                       required=True)
    code = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                       required=True)
    avatar_url = StringField(max_length=STRING_LENGTH['LARGE'])

    meta = {
        'indexes': [
            'code',
            'name',
        ]
    }
