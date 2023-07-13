from mongoengine import (
    StringField,
    DynamicField,
)
from app.common.constants import STRING_LENGTH
from app.db.mongo.documents import Model, BaseEmbeddedDocument


class IndexedTranslation(BaseEmbeddedDocument):
    language_code = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                                required=True)
    value = StringField(max_length=STRING_LENGTH['LONG'],
                        required=True)


class Translation(Model):
    language_code = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                                required=True)
    object_type = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                              required=True)
    object_id = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                            required=True)
    key = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                      required=True)
    value = DynamicField(required=True)

    meta = {
        'indexes': [
            'object_type',
            'language_code',
            'object_id',
            'key',
        ]
    }

    def to_dict(self, *args, **kwargs):
        includes = [
            'language_code',
            'object_type',
            'object_id',
            'value',
            'key',
        ]
        return super(Translation, self).to_dict(
            includes=includes
        )
