from flask import Blueprint, jsonify, request
from flask.templating import render_template
from app.db.mongo.documents.user import User
from app.decorators.action_filters.authorize_filter import authorize, abac_authorize
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from werkzeug.security import generate_password_hash

account_controller = Blueprint('account_controller', __name__)


@account_controller.route('/register', methods=('POST',))
def register():
    data = request.get_json()
    password = data['password']
    username = data['username']

    user = User.objects(email=username).first()
    if user is None:
        user = User(
            email=username,
            name=username,
            password=generate_password_hash(password)
        )

        user.add()
        access_token = create_access_token(identity=user.user_id)
        refresh_token = create_refresh_token(identity=user.user_id)

        response = jsonify()
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response, 201
    else:
        return jsonify(message="Unable to create user."), 400


@account_controller.route('/login', methods=('GET',))
def login_view():
    return render_template('login.html')

@account_controller.route('/login', methods=('POST',))
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = User.authenticate(username, password)
    if user:
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        response = jsonify()
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response, 201
    else:
        return jsonify(message="Unauthorized"), 401
