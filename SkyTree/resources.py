import uuid
import json

from flask import request, Response
from flask_restful import Resource
from database.db import initialize_db
from database.models import Task

class Tasks(Resource):
    #list Tasks
    def get(self):
        #Add behavior for GET here:
        tasks = Task.objects().to_json()
        return Response(tasks, mimetype="application/json", status=200)

    #Add Tasks
    def post(self):
        #Add behavior for POST here:
        body = request.get_json()
        json_obj = json.loads(json.dumps(body))
        #Get the number of Task objects in the Request
        obj_num = len(body)
        #For each Task object, add it to the db
        for i in range(len(body)):
            #add a UUID to each task object for tracking
            json_obj[i]['task_id'] = str(uuid.uuid4())
            #save task object to db
            Task(**json_obj[i]).save()
            #Load the options provided for the task into an array for tracking history
            task_options = []
            for key in json_obj[i].keys():
                #anything that comes after task_type and task_id is treated as an option
                if (key != "task_type" and key != "task_id"):
                    task_options.append(key +": " + json_obj[i][key])
        #return the last Task objects that were added
        return Response(Task.objects.skip(Task.objects.count() - obj_num).to_json(), mimetype="application/json", status=200)
