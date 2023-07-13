from mongoengine import StringField

from app.common.constants import STRING_LENGTH
from app.db.mongo.documents import CollectionBase
from app.db.mongo.documents.translation import IndexedTranslation


class AmenityProviderMapping(CollectionBase):
    source_code = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                              required=True)
    source_provider = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                                  required=True)
    destination_code = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                                   required=True)
    destination_provider = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                                       required=True)

    meta = {
        'indexes': [
            'source_code',
            'destination_code',
            'source_provider',
            'destination_provider'
        ]
    }
