from mongoengine import (
    StringField, PointField,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    MultiPolygonField, DictField, FloatField
)
from app.common.constants import STRING_LENGTH
from app.db.mongo.documents import Model, BaseEmbeddedDocument

from .translation import IndexedTranslation


class PlaceLocation(BaseEmbeddedDocument):
    point = PointField()

    polygon = MultiPolygonField()

    country_code = StringField(max_length=STRING_LENGTH['EX_SHORT'])


class PlaceRelation(BaseEmbeddedDocument):
    id = StringField(required=True,
                     max_length=STRING_LENGTH['EX_SHORT'])
    type = StringField(required=True,
                       max_length=STRING_LENGTH['EX_SHORT'], )
    code = StringField(max_length=STRING_LENGTH['EX_SHORT'], )


class PlaceRankings(BaseEmbeddedDocument):
    expedia = FloatField()


class PlaceTimezone(BaseEmbeddedDocument):
    name = StringField(required=True)
    gmt = FloatField(required=True)


class Place(Model):
    _translatable_fields = ['name', 'long_name']

    type = StringField(required=True,
                       max_length=STRING_LENGTH['EX_SHORT'], )
    expedia_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    viator_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    goquo_id = StringField(max_length=STRING_LENGTH['EX_SHORT'])
    code = StringField(max_length=STRING_LENGTH['EX_SHORT'])

    popular_score = FloatField(default=9999.0)

    location = EmbeddedDocumentField(PlaceLocation)
    rankings = EmbeddedDocumentField(PlaceRankings)
    timezone = EmbeddedDocumentField(PlaceTimezone)

    ancestors = EmbeddedDocumentListField(PlaceRelation, default=[])
    descendants = EmbeddedDocumentListField(PlaceRelation, default=[])
    associations = EmbeddedDocumentListField(PlaceRelation, default=[])
    nearest_airports = EmbeddedDocumentListField(PlaceRelation, default=[])
    name = EmbeddedDocumentListField(IndexedTranslation, required=True)
    long_name = EmbeddedDocumentListField(IndexedTranslation, required=True)

    metadata = DictField(default={})
    avatar = DictField(default={})

    meta = {
        'indexes': [
            'name.language_code',
            'long_name.language_code',
            'popular_score',
            'expedia_id',
            'viator_id',
            'goquo_id',
            'rankings.expedia',
            'nearest_airports.id',
            'nearest_airports.code',
            'type',
            'timezone.name',
            'location.country_code',
            'descendants.type',
            'descendants.id',
            'descendants.code',
            'associations.type',
            'associations.id',
            'associations.code',
            'ancestors.type',
            'ancestors.id',
            'ancestors.code',
            {
                'fields': [
                    '$name.value',
                    '$code',
                    '$long_name.value',
                ],
                'weights': {'name.value': 5,
                            'code': 2,
                            'long_name.value': 1}
            },
        ]
    }
