from flask import Flask
from flask_jwt_extended import JWTManager
from app.common.utils import hash_string
from app.db import do_connect_databases
from app.db.mongo.documents.account import Account
from app.error_handlers.error_handler import error_hander_register
from app.controllers import register_api
from app.middlewares import Middleware
from app.middlewares.pipeline_inside_app import configure_middlewares


def create_app() -> Flask:
    app = Flask(__name__)

    app.wsgi_app = Middleware(app.wsgi_app)
    app.secret_key = 'sadasdasdas'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']  
    JWTManager().init_app(app)

    do_connect_databases()

    configure_middlewares(app)

    error_hander_register(app)
    
    register_api(app)
    
    return app
