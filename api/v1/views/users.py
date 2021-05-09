#!/usr/bin/python3
"""
New view for User to handle RestFul API
"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def list_all_users():
    """
    Return a list of all users
    """
    if request.method == 'POST':
        new_user_name = None
        try:
            res_dict = request.get_json()
            new_user_name = res_dict.get('name')
            new_email = res_dict.get('email')
            new_pass = res_dict.get('password')
        except:
            abort(400, description='Not a JSON')
        if new_user_name is None:
            abort(400, description='Missing name')
        if new_email is None:
            abort(400, description='Missing email')
        if new_pass is None:
            abort(400, description='Missing password')
        new_user = User(name=new_user_name)
        new_user.save()
        return jsonify(new_user.to_dict()), 201
    users = storage.all('User')
    list_user_dict = [s.to_dict() for s in users.values()]
    return jsonify(list_user_dict)


@app_views.route('/user/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def list_one_user(user_id):
    """
    Returns a single user
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(400)
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            res_dict = request.get_json()
            res_dict['id'] = user.id
            res_dict['email'] = user.email
            res_dict['created_at'] = user.create_at
            user.__init__(**res_dict)
            user.save()
            return jsonify(user.to_dict()), 200
        except:
            abort(400, description='Not a JSON')
    return jsonify(user.to_dict())
