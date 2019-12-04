import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user')

@user.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    payload['username'].lower
    try:
        #query to check is username is already in use
        models.User.get(models.User.username == payload['username'])
        return jsonify(data={}, status={"code": 401, "message": "Username taken"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)
        #puts user in database
        login_user(user) #starts session & logs them in
        user_dict = model_to_dict(user)
        del user_dict['password']  #delete password before returning request
        return jsonify(data=user_dict, status={"code": 200, "message": "User Created"})
