from mongoengine import (
    StringField, FloatField, IntField, ListField,
    EmbeddedDocumentField, EmbeddedDocumentListField,
    DictField, BooleanField
)
from app.common.constants import STRING_LENGTH
from app.db.mongo.documents import Model, BaseEmbeddedDocument

from .image import ImageUrls
from .place import PlaceRelation, PlaceTimezone
from .translation import IndexedTranslation


class TourSupplier(BaseEmbeddedDocument):
    name = StringField(
        max_length=STRING_LENGTH['SHORT'])
    reference = StringField(
        max_length=STRING_LENGTH['SHORT'])
    code = StringField(
        max_length=STRING_LENGTH['SHORT'])


class TourReviewSource(BaseEmbeddedDocument):
    provider_code = StringField(
        max_length=STRING_LENGTH['EX_SHORT'],
        required=True
    )
    total_reviews = IntField()
    average_rating = FloatField()


class TourReviews(BaseEmbeddedDocument):
    total_reviews = IntField()

    average_rating = FloatField()

    sources = EmbeddedDocumentListField(TourReviewSource)


class TourPriceInfo(BaseEmbeddedDocument):
    currency_code = StringField(required=True,
                                max_length=STRING_LENGTH['EX_SHORT'])

    price_from = FloatField(default=0)


class TourTag(Model):
    _translatable_fields = ['name']

    viator_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    hms_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])

    name = EmbeddedDocumentListField(IndexedTranslation)

    priority = IntField(default=0)

    parent_id = StringField(
        max_length=STRING_LENGTH['EX_SHORT'],
        default=None
    )

    parent_ids = ListField(
        StringField(max_length=STRING_LENGTH['EX_SHORT']),
        default=[]
    )

    avatar = DictField()

    meta = {
        'indexes': [
            'viator_id',
            'parent_id',
            'parent_ids',
            'priority',
            'name.language_code',
            '$name.value'
        ]
    }


class Tour(Model):
    _translatable_fields = ['title']

    viator_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    hms_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])

    provider_name = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    provider_code = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    country_code = StringField(max_length=STRING_LENGTH['EX_SHORT'])

    hotel_pickup = BooleanField(default=False)
    enabled = BooleanField(default=True)

    age_policies = DictField()

    avatar = EmbeddedDocumentField(ImageUrls)
    timezone = EmbeddedDocumentField(PlaceTimezone)

    booking_questions = ListField(StringField(), default=[])
    tag_ids = ListField(StringField(), default=[])

    places = EmbeddedDocumentListField(PlaceRelation)
    title = EmbeddedDocumentListField(IndexedTranslation)

    supplier = EmbeddedDocumentField(TourSupplier)
    price_info = EmbeddedDocumentField(TourPriceInfo)
    reviews = EmbeddedDocumentField(TourReviews)

    metadata = DictField(default={})

    meta = {
        'indexes': [
            'viator_id',
            'country_code',
            'places.id',
            'places.type',
            'places.code',
            'reviews.total_reviews',
            'reviews.average_rating',
            'timezone.name',
            'timezone.gmt',
            'supplier.name',
            'supplier.reference',
            'title.language_code',
            'price_info.currency_code',
            '$title.value',
            'enabled',
        ]
    }
