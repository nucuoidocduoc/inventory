from flask import Blueprint, jsonify
from flask.helpers import url_for
from flask.templating import render_template

home_controller = Blueprint('home_controller', __name__)


@home_controller.route('/', defaults={'path': ''})
@home_controller.route('/<path:path>')
def default_route(path):
    # Xử lý logic ở đây
    script_url = url_for('static', filename='js/main.bundle.js')
    return render_template('index.html', script=script_url)
