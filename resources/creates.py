import models
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

create = Blueprint('creates', 'create')

#GET ROUTE
@create.route('/', methods=["GET"])
def get_all_creates():
    try:
        current_user_id = current_user.id
        creates = [model_to_dict(date) for date in models.Create.select().where(
            models.Create.user == current_user_id
        )]
        #.select is a peewee method that finds all the dates on Date model
        print(creates)
        return jsonify(data=creates, status={"code": 200, "message": "Success"})
   
      

#POST ROUTE
@create.route('/', methods=["POST"])
def create_create():
    payload = request.get_json()
    print(type(payload), 'payload')
    if not current_user.is_authenticated:
        print(current_user)
        return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to create a dog'})
    payload['user'] = current_user.id
    created = models.Create.create(**payload)
    #**payload is short for below
    # date = models.Date.create(name=payload['name'], description=payload['description'])
    #peewee has a create method which creates an entry in
    #our database - **payload is using the spread operator on payload
    return jsonify(data = model_to_dict(created), status={"code": 200, "message": "Creation succesful"})

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
    create_to_update = models.Create.get(id=id)
    if not current_user.is_authenticated:
        return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in '})
    if create_to_update.user.id is not current_user.id:
        return jsonify(data={}, status={'code': 401, 'message': 'you can only update your own date'})
    create_to_update.update(
        name=payload['name'],
        description=payload['description']
    ).execute()

    update_create_dict = model_to_dict(create_to_update)
    return jsonify(data=update_create_dict, status={'code': 200, 'message': 'success'})

#DELETE ROUTE
@create.route('/<id>', methods=["DELETE"])
def delete_create(id):
    #grab create to do a check on id and user id
    create_to_delete = models.Create.get(id=id)
    if not current_user.is_authenticated:
        return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in'})
    if create_to_delete.user.id is not current_user.id:
        return jsonify(data={}, status={'code': 401, 'message': 'have to have created this'})
   
    create_to_delete.delete()
 
    return jsonify(data = "Date deleted", status = {"code": 200, "msg": "OK"})