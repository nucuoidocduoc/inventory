from mongoengine import (DateTimeField, DictField, EmbeddedDocumentField,
                         EmbeddedDocumentListField, FloatField, IntField,
                         ListField, PointField, StringField)

from app.common.constants import STRING_LENGTH
from app.db.mongo.documents import BaseEmbeddedDocument, CollectionBase

from .image import ImageUrls
from .place import PlaceRelation
from .translation import IndexedTranslation


class PropertyLocation(BaseEmbeddedDocument):
    point = PointField(required=True)

    country_code = StringField(max_length=STRING_LENGTH['EX_SHORT'])


class PropertyRankings(BaseEmbeddedDocument):
    expedia = FloatField()


class PropertyRatings(BaseEmbeddedDocument):
    expedia = DictField()
    tripadvisor = DictField()


class Property(CollectionBase):
    _translatable_fields = ['name', 'street_address']

    type = StringField(max_length=STRING_LENGTH['EX_SHORT'],
                       required=True)
    expedia_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    tripadvisor_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    goquo_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    giata_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    phone = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    fax = StringField(max_length=STRING_LENGTH['EX_SHORT'])

    star = FloatField()

    expedia_updated_at = DateTimeField()
    viator_updated_at = DateTimeField()
    goquo_updated_at = DateTimeField()
    tripadvisor_updated_at = DateTimeField()

    airport_codes = ListField(StringField(
        max_length=STRING_LENGTH['EX_SHORT'])
    )

    nearest_airports = EmbeddedDocumentListField(PlaceRelation, default=[])
    places = EmbeddedDocumentListField(PlaceRelation, default=[])
    name = EmbeddedDocumentListField(IndexedTranslation, default=[])
    street_address = EmbeddedDocumentListField(IndexedTranslation, default=[])

    location = EmbeddedDocumentField(PropertyLocation)
    rankings = EmbeddedDocumentField(PropertyRankings)
    avatar = EmbeddedDocumentField(ImageUrls)
    ratings = EmbeddedDocumentField(PropertyRatings)

    amenity_ids = ListField(StringField(
        max_length=STRING_LENGTH['EX_SHORT'])
    )

    meta = {
        'indexes': [
            'type',
            'airport_codes',
            'nearest_airports.id',
            'nearest_airports.code',
            'places.id',
            'places.type',
            'places.code',
            'expedia_id',
            'tripadvisor_id',
            'goquo_id',
            'giata_id',
            'expedia_updated_at',
            'viator_updated_at',
            'goquo_updated_at',
            'tripadvisor_updated_at',
            'location.country_code',
            'name.language_code',
            'street_address.language_code',
            'amenity_ids',
            'rankings.expedia',
            {
                'fields': ['$name.value',
                           '$street_address.value'],
                'weights': {'name.value': 5,
                            'street_address.value': 1}
            }
        ],
    }


class PropertyRoomOccupancy(BaseEmbeddedDocument):
    total = IntField()
    adults = IntField()
    children = IntField()
    infants = IntField()


class PropertyRoomArea(BaseEmbeddedDocument):
    square_meters = FloatField()
    square_feet = FloatField()


class PropertyRoomBed(BaseEmbeddedDocument):
    quantity = IntField(default=1)
    size = StringField(max_length=STRING_LENGTH['EX_SHORT'], required=True)
    type = StringField(max_length=STRING_LENGTH['EX_SHORT'], required=True)


class PropertyRoom(CollectionBase):
    _translatable_fields = ['name']

    property_id = StringField(required=True,
                              max_length=STRING_LENGTH['EX_SHORT'])
    expedia_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    goquo_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    tripadvisor_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])

    avatar = EmbeddedDocumentField(ImageUrls)
    area = EmbeddedDocumentField(PropertyRoomArea)
    occupancy = EmbeddedDocumentField(PropertyRoomOccupancy)

    name = EmbeddedDocumentListField(IndexedTranslation)
    beds = EmbeddedDocumentListField(PropertyRoomBed)

    meta = {
        'indexes': [
            'property_id',
            'expedia_id',
            'goquo_id',
            'name.language_code',
            {
                'fields': ['$name.value'],
            }
        ]
    }
