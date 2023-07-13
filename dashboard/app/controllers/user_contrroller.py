from flask import Blueprint, jsonify
from app.decorators.action_filters.authorize_filter import authorize, abac_authorize

user_contrroller = Blueprint('user_contrroller', __name__)

@user_contrroller.route("/users", methods=["GET"])
# @abac_authorize()
def get_users():
    # raise Exception("Sorry, no numbers below zero")
    return jsonify("123")