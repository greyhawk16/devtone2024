from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

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

    from .models import SessionDB
    create_database(app)

    return app
    
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('>>> Create DB')