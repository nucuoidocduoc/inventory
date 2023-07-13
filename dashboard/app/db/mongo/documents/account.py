from mongoengine import (
    StringField, FloatField, IntField,
    ListField, PointField,
    EmbeddedDocumentField, EmbeddedDocumentListField,
    ObjectIdField, DictField,
    DynamicField, DateTimeField
)
from app.common.constants import STRING_LENGTH
from app.common.utils import hash_string
from app.db.mongo.documents import Model


class Account(Model):
    status = StringField(
        max_length=STRING_LENGTH['EX_SHORT'], default='active')
    type = StringField(max_length=STRING_LENGTH['EX_SHORT'], null=False)
    email = StringField(
        max_length=STRING_LENGTH['LONG'], null=False, unique=True)
    phone = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    first_name = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    last_name = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    hash_password = StringField(max_length=STRING_LENGTH['LONG'], null=False)

    def encrypt_secret_key(self, value: str) -> str:
        if not self.email:
            raise Exception('MissingEmail')

        return hash_string(value + self.email)

    def validate_secret_key(self, value: str) -> bool:
        return hash_string(value + self.email) == self.hash_password

    def to_json(self,
                *args,
                **kwargs):
        result = super(Account, self).to_json(*args, **kwargs)

        result.pop('secret_key', None)

        return result
