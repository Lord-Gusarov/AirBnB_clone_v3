#!/usr/bin/python3
"""
Index for our web flask
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


classes_rel = {"Amenity": "amenities", "City": "cities", "Place": "places",
               "Review": "reviews", "State": "states", "User": "users"}


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

    for key, value in classes_rel.items():
        number = storage.count(key)
        obj_cnt[value] = number

    return jsonify(obj_cnt)
