from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from os import path
from sqlalchemy.orm import scoped_session, sessionmaker

db      = SQLAlchemy()
DB_NAME = "database.db"

api_loaded_start   = {}
api_loaded_problem = {}
api_loaded_result  = {}


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'semicircle_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .webpage import webpage
    from .apis import apis
    app.register_blueprint(webpage, url_prefix='/')
    app.register_blueprint(apis, url_prefix='/')

    from . import models
    with app.app_context():
        db.create_all()
        
    return app

