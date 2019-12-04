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
    print(type(payload), 'payload')
    #when the request is sent over from the client we turn it into json
    date = models.Date.create(**payload)
    #**payload is short for below
    # date = models.Date.create(name=payload['name'], description=payload['description'])
    #peewee has a create method which creates an entry in
    #our database - **payload is using the spread operator on payload
    date_dict = model_to_dict(date)
    return jsonify(data=date_dict, status={"code": 200, "message": "Creation succesful"})

# SHOW ROUTE
@date.route('/<id>', methods=["GET"])
def show_one_date(id):
    #does the id match what i think it should match?
    print(id)
    date = models.Date.get_by_id(id)
    return jsonify(data = model_to_dict(date), status = {"code": 200, "msg": "OK"})

#EDIT ROUTE 
@date.route('/<id>', methods=["PUT"])
def edit_date_idea(id):
    payload = request.get_json()
    # if the id of the thing I am searching is == to the id in the url, execute this peewee method
    query = models.Date.update(**payload).where(models.Date.id == id)
    query.execute()
    date = models.Date.get_by_id(id)
    date_dict = model_to_dict(date)
    return jsonify(data = date_dict, status = {"code": 200, "msg": "OK"})

#DELETE ROUTE
@date.route('/<id>', methods=["DELETE"])
def delete_date(id):
    # making sure that the id of the thing I get back is the same as the id in the url
    # if it is, then the peewee/SQL query/method of delete should execute when the execute method
    # is invoked 
    query = models.Date.delete().where(models.Date.id == id)
    # execute the delete query
    query.execute()
    return jsonify(data = "Date deleted", status = {"code": 200, "msg": "OK"})