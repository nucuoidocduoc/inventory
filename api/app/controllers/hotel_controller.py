import string
from flask import Blueprint, jsonify
from app.db.mongo.documents.property import Property
from flask import request

hotel_controller = Blueprint('hotel_controller', __name__)


@hotel_controller.route("/api/get-hotel-filter-options/<region_id>", methods=["GET"])
# @abac_authorize()
def get_hotel_filter_options(region_id: string):

    pipeline = [
        {"$match": {"region_ids": {"$in": [region_id]}}},
        {"$unwind": "amenity_ids"},
        {"$group": {{"stars": {"$adToSet": "star"}}, {
            "$amenities": {"$adToSet", "amenity_ids"}}}},
        {"$lookup": {"$from": "amenity_provider_mapping",
                     "$let": {"amenity_ids": "$amenities"},
                     "pipeline": [
                         {"$match": {"$expr": {"$and": [
                             {"destination_code": {"$in": "$$amenity_ids"}},
                             {"eq": {"$source_provider": "bamboo"}},
                         ]}}},
                         {"$lookup":{
                            "from":"amenity",
                            "localField":"code",
                            "foreignField":"source_code",
                            "as":{"$mergeObjects"}
                         }}
                     ],
                     }}
    ]

    property = Property.objects.aggregate()
    return jsonify(property)
