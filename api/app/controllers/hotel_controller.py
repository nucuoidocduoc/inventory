import string
from app.db.mongo.documents.amenity_provider_mapping import AmenityProviderMapping
from flask import Blueprint, jsonify
from app.db.mongo.documents.property import Property
from flask import request, make_response

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

    match_multiple_condition = [
        {"$in": ["$region_ids", region_id]}
    ]

    if amenities is not None and len(amenities) != 0:
        provider_amenities_pipeline = [
            {"$match": {"$expr": {"$and": [{"$in": ["$source_code", amenities]}, {
                "$eq": ["$source_provider", "bamboo"]}]}}},
            {"$group": {
                "_id": None,
                "amenity_provider_ids": {"$addToSet": "$destination_code"}
            }},
            {"$project": {
                "amenity_provider_ids": "$amenity_provider_ids"
            }}
        ]

        provider_amenities = list(
            AmenityProviderMapping.objects.aggregate(provider_amenities_pipeline))
        if provider_amenities is None:
            return make_response("failure", 400)

        match_multiple_condition.append(
            {"$in": ["$amenity_ids", provider_amenities]})

    if stars is not None and len(stars) != 0:
        match_multiple_condition.append({"$in": ["$star", stars]})

    if places is not None and len(places) != 0:
        match_multiple_condition.append(
            {"places": {"$elemMatch": {"id": {"$in": places}, "code": "multi_city_vicinity"}}})

    match_multiple_condition.append({
        "$project": {
            "hotel_ids": "$goquo_id"
        }
    })

    properties = Property.objects.aggregate(match_multiple_condition)
    return jsonify(list(properties))


@hotel_controller.route("/api/get-hotels", methods=["POST"])
# @abac_authorize()
def get_hotel():
    json_data = request.get_json()  # Lấy dữ liệu từ JSON body
    hotel_ids = json_data.get('hotel_ids')
    pipeline = [
        {"$match": {"goquo_id": {"$in": hotel_ids}}},
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
        {"$set": {
            "amenities": "$bamboo_amenities_mapping"
        }},
        {
            "$unset": {
                "amenity_ids": ""
            }
        }
    ]
    return jsonify(list(Property.objects.aggregate(pipeline)))
