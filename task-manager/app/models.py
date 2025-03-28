from bson.objectid import ObjectId

class TaskManager:
    def __init__(self, db):
        self.collection = db.tasks
    
    def get_all_tasks(self):
        return list(self.collection.find())
    
    def add_task(self, content):
        return self.collection.insert_one({
            'content': content,
            'completed': False
        })
    
    def complete_task(self, task_id):
        return self.collection.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': {'completed': True}}
        )
    
    def delete_task(self, task_id):
        return self.collection.delete_one({'_id': ObjectId(task_id)})