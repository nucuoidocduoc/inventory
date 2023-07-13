from mongoengine import EmbeddedDocumentListField, StringField

from app.common.constants import STRING_LENGTH
from app.db.mongo.documents import CollectionBase
from app.db.mongo.documents.translation import IndexedTranslation


class Amenity(CollectionBase):
    code = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                       required=True)
    provider = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                           required=True)
    value = EmbeddedDocumentListField(IndexedTranslation, default=[])

    type = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                           required=True)

    meta = {
        'indexes': [
            'code',
            'value.language_code',
        ]
    }
