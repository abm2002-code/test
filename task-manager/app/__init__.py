import os
from flask import Flask
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-key')
    
    # MongoDB connection
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/taskmanager')
    app.client = MongoClient(mongo_uri)
    app.db = app.client.get_database()
    app.tasks_collection = app.db.tasks
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app