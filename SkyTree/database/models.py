from database.db import db

#define Task object in Database
class Task(db.DynamicDocument):
    task_id = db.StringField(required=True)
