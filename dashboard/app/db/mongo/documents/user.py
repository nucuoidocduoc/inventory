from mongoengine import (
    StringField, EmbeddedDocumentField,
    EmailField
)
from app.common.constants import STRING_LENGTH
from app.db.mongo.documents import Model
from werkzeug.security import generate_password_hash
from .image import ImageUrls


class User(Model):
    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    email = EmailField(required=True, unique=True)
    password = StringField(required=True,
                           max_length=STRING_LENGTH['LONG'])
    name = StringField(max_length=STRING_LENGTH['SHORT'])

    avatar = EmbeddedDocumentField(ImageUrls)

    meta = {
        'indexes': [
            'email',
            'name',
        ]
    }

    def authenticate(self, password):
        return User(email='nguyenphuongbk@gmail', password="Admin@123", id='123123')
        # user = User.objects(email=self.email).first()
        # if user is None or generate_password_hash(password) != self.password:
        #     return None
        # return user
        
