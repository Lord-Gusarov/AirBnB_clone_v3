#!/usr/bin/python3
"""
Index for our web flask
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes_all = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
               "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Return json status of web flask
    """
    status = {'status': 'OK'}
    return jsonify(status)


@app_views.route('/stats', strict_slashes=False)
def obj_count():
    """ 
    Retrieves the number of each objects
    """
    obj_cnt = {}
    for key in classes_all:
        obj_cnt[key] = storage.count(key)

    return jsonify(obj_cnt)
