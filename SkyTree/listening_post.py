import json
import resources

from flask import Flask, jsonify
from flask_restful import Api, Resource
from database.db import initialize_db

#Initiate our Flask app
app = Flask(__name__)

#configure our database on localhost
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/skytree'
}

#Intialize our database
initialize_db(app)

#Intialize our API
api = Api(app)

#Define the routes for each of our resources
api.add_resource(resources.Tasks, '/tasks', endpoint='tasks')
api.add_resource(resources.Results, '/results')
api.add_resource(resources.History, '/history')

#Start in debug mode
if __name__ == '__main__':
    app.run(debug=True)
