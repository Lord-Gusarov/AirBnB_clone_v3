#!/usr/bin/python3
"""
Creating a new view for Amenity to handle RestFul API actions
"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def list_all_amenities():
    """
    Returns a list of all Amenity objects
    """

    if request.method == 'POST':
        new_amenity_name = None
        try:
            res_dict = request.get_json()
            new_amenity_name = res_dict.get('name')
        except:
            abort(400, description='Not a JSON')
        if new_amenity_name is None:
            abort(400, description='Missing name')
        new_amenity = Amenity(name=new_amenity_name)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201
    amenities = storage.all('Amenity')
    list_amenity_dict = [s.to_dict() for s in amenities.values()]
    return jsonify(list_amenity_dict)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def list_single_amenity(amenity_id):
    """
    Returns amenity object by id
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            res_dict = request.get_json()
            res_dict['id'] = amenity.id
            res_dict['created_at'] = amenity.created_at
            amenity.__init__(**res_dict)
            amenity.save()
            return jsonify(amenity.to_dict()), 200
        except:
            abort(400, description='Not a JSON')
    return jsonify(amenity.to_dict())
