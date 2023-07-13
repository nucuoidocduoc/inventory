from mongoengine import (
    StringField, FloatField, IntField,
    BooleanField, ListField, GeoPointField,
    PolygonField, EmbeddedDocumentField, EmbeddedDocumentListField,
    ObjectIdField, DictField
)
from app.common.constants import STRING_LENGTH
from app.db.mongo.documents import Model, BaseEmbeddedDocument


class ImageUrls(BaseEmbeddedDocument):
    sm = StringField(max_length=STRING_LENGTH['LONG'])
    md = StringField(max_length=STRING_LENGTH['LONG'])
    lg = StringField(max_length=STRING_LENGTH['LONG'])


class Image(Model):
    object_id = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                            required=True)
    object_type = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                              required=True)

    urls = EmbeddedDocumentField(ImageUrls, required=True)

    meta = {
        'indexes': [
            'object_type',
            'object_id',
        ]
    }
