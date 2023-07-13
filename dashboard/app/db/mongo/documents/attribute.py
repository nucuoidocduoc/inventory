from mongoengine import (
    StringField,
    ListField
)
from app.common.constants import STRING_LENGTH
from app.db.mongo.documents import Model


class Attribute(Model):
    type = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                       required=True)
    content_type = StringField(max_length=STRING_LENGTH['EX_SHORT'])

    meta = {
        'indexes': [
            'type',
            'content_type',
        ]
    }
