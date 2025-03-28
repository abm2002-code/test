from flask import Blueprint, render_template, request, redirect, url_for, current_app
from bson.objectid import ObjectId

main = Blueprint('main', __name__)

@main.route('/')
def index():
    tasks = list(current_app.tasks_collection.find())
    return render_template('index.html', tasks=tasks)

@main.route('/add_task', methods=['POST'])
def add_task():
    task_content = request.form.get('content')
    if task_content:
        current_app.tasks_collection.insert_one({
            'content': task_content,
            'completed': False
        })
    return redirect(url_for('main.index'))

@main.route('/complete_task/<task_id>')
def complete_task(task_id):
    current_app.tasks_collection.update_one(
        {'_id': ObjectId(task_id)},
        {'$set': {'completed': True}}
    )
    return redirect(url_for('main.index'))

@main.route('/delete_task/<task_id>')
def delete_task(task_id):
    current_app.tasks_collection.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('main.index'))