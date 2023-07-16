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
        {"$unwind": "$amenity_ids"},
        {
            "$group": {
                "_id": None,
                "stars": {"$addToSet": "$star"},
                "amenities": {"$addToSet": "$amenity_ids"}
            }
        },
        {
            "$lookup": {
                "from": "amenity_provider_mapping",
                "let": {
                    "amenity_ids": "$amenities"},
                "pipeline": [{
                    "$match": {
                        "$expr": {
                            "$and": [{
                                "$in": [
                                    "$destination_code", "$$amenity_ids"]}, {
                                "$eq": ["$source_provider", "bamboo"]}]}}}, {
                    "$lookup": {
                        "from": "amenity",
                        "let": {
                            "amenity_foregin_code": "$source_code"},
                        "pipeline": [{
                            "$match": {
                                "$expr": {
                                    "$eq": ["$code", "$$amenity_foregin_code"]}}}
                        ],
                        "as": "bamboo_amenities"
                    }}],
                "as": "bamboo_amenities_mapping"}
        },
        {
            "$project": {
                "stars": "$stars",
                "amenities": {
                    "$map": {
                        "input": "$bamboo_amenities_mapping",
                        "as": "mapping",
                        "in": {
                            "$let": {
                                "vars": {
                                    "first_amenity": {"$arrayElemAt": ["$$mapping.bamboo_amenities", 0]}
                                },
                                "in":{
                                    "value": {"$arrayElemAt": ["$$first_amenity.value.value", 0]},
                                    "code":"$$first_amenity.code"
                                }
                            }}
                    }}
            }
        }
    ]

    properties = Property.objects.aggregate(pipeline)
    return jsonify(list(properties))


@hotel_controller.route("/api/get-hotel-ids/<region_id>", methods=["GET"])
# @abac_authorize()
def get_hotel_ids(region_id: string):
    json_data = request.get_json()  # Lấy dữ liệu từ JSON body
    stars = json_data.get('stars')
    amenities = json_data.get('amenities')
    places = json_data.get('places')



    pipeline = [
        {"$match": {"region_ids": {"$in": [region_id]}}},
        {"$unwind": "$amenity_ids"},
        {
            "$group": {
                "_id": None,
                "stars": {"$addToSet": "$star"},
                "amenities": {"$addToSet": "$amenity_ids"}
            }
        },
        {
            "$lookup": {
                "from": "amenity_provider_mapping",
                "let": {
                    "amenity_ids": "$amenities"},
                "pipeline": [{
                    "$match": {
                        "$expr": {
                            "$and": [{
                                "$in": [
                                    "$destination_code", "$$amenity_ids"]}, {
                                "$eq": ["$source_provider", "bamboo"]}]}}}, {
                    "$lookup": {
                        "from": "amenity",
                        "let": {
                            "amenity_foregin_code": "$source_code"},
                        "pipeline": [{
                            "$match": {
                                "$expr": {
                                    "$eq": ["$code", "$$amenity_foregin_code"]}}}
                        ],
                        "as": "bamboo_amenities"
                    }}],
                "as": "bamboo_amenities_mapping"}
        },
        {
            "$project": {
                "stars": "$stars",
                "amenities": {
                    "$map": {
                        "input": "$bamboo_amenities_mapping",
                        "as": "mapping",
                        "in": {
                            "$let": {
                                "vars": {
                                    "first_amenity": {"$arrayElemAt": ["$$mapping.bamboo_amenities", 0]}
                                },
                                "in":{
                                    "value": {"$arrayElemAt": ["$$first_amenity.value.value", 0]},
                                    "code":"$$first_amenity.code"
                                }
                            }}
                    }}
            }
        }
    ]

    properties = Property.objects.aggregate(pipeline)
    return jsonify(list(properties))


@hotel_controller.route("/api/get-hotels", methods=["POST"])
# @abac_authorize()
def get_hotel():
    json_data = request.get_json()  # Lấy dữ liệu từ JSON body
    region_ids = json_data.get('region_ids')
    pipeline = [
        {"$match": {"region_ids": {"$in": region_ids}}},
        {"$unwind": "$amenity_ids"},
        {
            "$group": {
                "_id": None,
                "stars": {"$addToSet": "$star"},
                "amenities": {"$addToSet": "$amenity_ids"}
            }
        }
    ]

    result = Property.objects.aggregate(pipeline)
    return jsonify(list(result))
