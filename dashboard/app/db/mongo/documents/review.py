from mongoengine import (
    StringField, FloatField, IntField,
    BooleanField, ListField, GeoPointField,
    PolygonField, EmbeddedDocumentField, EmbeddedDocumentListField,
    ObjectIdField, DictField
)
from app.common.constants import STRING_LENGTH
from app.db.mongo.documents import Model, BaseEmbeddedDocument


class ReviewAuthor(BaseEmbeddedDocument):
    name = StringField(max_length=STRING_LENGTH['EX_SHORT'], required=True)
    country_code = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    avatar_url = StringField(max_length=STRING_LENGTH['LONG'])


class Review(Model):
    object_id = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                              required=True)
    object_type = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                              required=True)
    viator_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    expedia_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    content = StringField(max_length=STRING_LENGTH['LARGE'],
                          required=True)
    rating = FloatField()

    author = EmbeddedDocumentField(ReviewAuthor, required=True)

    meta = {
        'indexes': [
            'object_type',
            'object_id',
            'author.country_code',
            'author.name',
            'viator_id',
            'expedia_id',
            'rating',
        ]
    }
