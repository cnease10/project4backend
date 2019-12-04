#resources give us access to our http methods just by
#defining methods on your resource

import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

date = Blueprint('dates', 'date')

#GET ROUTE
@date.route('/', methods=["GET"])
def get_all_dates():
    try:
        dates = [model_to_dict(date) for date in models.Date.select()]
        #.select is a peewee method that finds all the dates on Date model
        print(dates)
        return jsonify(data=dates, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Can't get resources"})

#POST ROUTE
@date.route('/', methods=["POST"])
def create_dates():
    payload = request.get_json()
    #when the request is sent over from the client we turn it into json
    date = models.Date.create(**payload)
    #peewee has a create method which creates an entry in
    #our database - **payload is using the spread operator on payload
    date_dict = model_to_dict(date)
    return jsonify(data=date_dict, status={"code": 200, "message": "Creation succesful"})
