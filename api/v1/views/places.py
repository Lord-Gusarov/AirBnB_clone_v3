#!/usr/bin/python3
"""
Index for our web flask
"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def list_all_places(city_id):
    """
    Returns the list of all Places objects of a City
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if request.method == 'POST':
        new_place_name = None
        place_userId = None
        try:
            res_dict = request.get_json()
            new_place_name = res_dict.get('name')
            place_userId = res_dict.get('user_id')
        except:
            abort(400, description='Not a JSON')
        if new_place_name is None:
            abort(400, description='Missing name')
        if place_userId is None:
            abort(400, description='Missing user_id')
        user = storage.get('User', place_userId)
        if user is None:
            abort(404)
        new_place = Place(name=new_place_name, place_userId=place_userId)
        new_place.save()
        return jsonify(new_place.to_dict()), 201
    list_places_as_dicts = [s.to_dict() for s in city.places]
    return jsonify(list_places_as_dicts)


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_one_place(place_id):
    """
    Retrieves a place by id
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            res_dict = request.get_json()
            res_dict['id'] = place.id
            res_dict['created_at'] = place.created_at
            place.__init__(**res_dict)
            place.save()
            return jsonify(place.to_dict()), 200
        except:
            abort(400, description='Not a JSON')
    return jsonify(place.to_dict())
