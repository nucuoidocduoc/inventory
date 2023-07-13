from flask import Blueprint, jsonify
from app.db.mongo.documents.property import Property

hotel_controller = Blueprint('hotel_controller', __name__)

@hotel_controller.route("/hotels", methods=["GET"])
# @abac_authorize()
def get_users():
    # raise Exception("Sorry, no numbers below zero")
    property = Property.objects.count()
    return jsonify(property)