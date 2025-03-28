from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-key')

# Get MongoDB connection parameters from environment variables
mongo_username = os.environ.get('MONGO_USERNAME', 'admin')
mongo_password = os.environ.get('MONGO_PASSWORD', 'password')
mongo_host = os.environ.get('MONGO_HOST', 'mongodb')
mongo_port = os.environ.get('MONGO_PORT', '27017')
mongo_db = os.environ.get('MONGO_DB', 'taskmanager')

# Construct MongoDB URI with actual values
mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}?authSource=admin"
print(f"MongoDB URI (without password): mongodb://{mongo_username}:****@{mongo_host}:{mongo_port}/{mongo_db}?authSource=admin")

# Connect to MongoDB
client = None
db = None
tasks_collection = None
try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    # Test the connection
    client.admin.command('ping')
    db = client[mongo_db]
    tasks_collection = db.tasks
    print(f"Connected to MongoDB at {mongo_host}:{mongo_port}/{mongo_db}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def index():
    try:
        tasks = []
        # Changed this line to check if tasks_collection is None
        if tasks_collection is not None:
            tasks = list(tasks_collection.find())
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        print(f"Error in index route: {e}")
        return f"An error occurred: {str(e)}", 500

@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        # Changed this line to check if tasks_collection is None
        if tasks_collection is not None:
            task_content = request.form.get('content')
            if task_content:
                tasks_collection.insert_one({
                    'content': task_content,
                    'completed': False
                })
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error in add_task route: {e}")
        return f"An error occurred: {str(e)}", 500

@app.route('/complete_task/<task_id>')
def complete_task(task_id):
    try:
        # Changed this line to check if tasks_collection is None
        if tasks_collection is not None:
            tasks_collection.update_one(
                {'_id': ObjectId(task_id)},
                {'$set': {'completed': True}}
            )
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error in complete_task route: {e}")
        return f"An error occurred: {str(e)}", 500

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    try:
        # Changed this line to check if tasks_collection is None
        if tasks_collection is not None:
            tasks_collection.delete_one({'_id': ObjectId(task_id)})
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error in delete_task route: {e}")
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)