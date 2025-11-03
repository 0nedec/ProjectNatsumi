from flask_mongoengine import MongoEngine

#Intialize MongoEngine and our database
db = MongoEngine()

def initialize_db(app):
    db.init_app(app)
