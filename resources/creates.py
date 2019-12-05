import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

create = Blueprint('creates', 'create')

#GET ROUTE
@create.route('/', methods=["GET"])
def get_all_creates():
    try:
        creates = [model_to_dict(date) for date in models.Create.select()]
        #.select is a peewee method that finds all the dates on Date model
        print(creates)
        return jsonify(data=creates, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Can't get resources"})

#POST ROUTE
@create.route('/', methods=["POST"])
def create_create():
    payload = request.get_json()
    print(type(payload), 'payload')
    #when the request is sent over from the client we turn it into json
    create = models.Create.create(**payload)
    #**payload is short for below
    # date = models.Date.create(name=payload['name'], description=payload['description'])
    #peewee has a create method which creates an entry in
    #our database - **payload is using the spread operator on payload
    create_dict = model_to_dict(create)
    return jsonify(data=create_dict, status={"code": 200, "message": "Creation succesful"})

# SHOW ROUTE
@create.route('/<id>', methods=["GET"])
def show_one_create(id):
    #does the id match what i think it should match?
    print(id)
    create = models.Create.get_by_id(id)
    return jsonify(data = model_to_dict(create), status = {"code": 200, "msg": "OK"})

#EDIT ROUTE 
@create.route('/<id>', methods=["PUT"])
def edit_create_idea(id):
    payload = request.get_json()
    # if the id of the thing I am searching is == to the id in the url, execute this peewee method
    query = models.Create.update(**payload).where(models.Create.id == id)
    query.execute()
    create = models.Create.get_by_id(id)
    create_dict = model_to_dict(create)
    return jsonify(data = create_dict, status = {"code": 200, "msg": "OK"})

#DELETE ROUTE
@create.route('/<id>', methods=["DELETE"])
def delete_create(id):
    # making sure that the id of the thing I get back is the same as the id in the url
    # if it is, then the peewee/SQL query/method of delete should execute when the execute method
    # is invoked 
    query = models.Create.delete().where(models.Create.id == id)
    # execute the delete query
    query.execute()
    return jsonify(data = "Date deleted", status = {"code": 200, "msg": "OK"})