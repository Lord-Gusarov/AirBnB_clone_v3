#!/usr/bin/python3
"""
Index for our web flask
"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def list_all_cities(state_id):
    """
    Returns the list of all City objects of a State
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if request.method == 'POST':
        new_city_name = None
        try:
            res_dict = request.get_json()
            new_city_name = res_dict.get('name')
        except:
            abort(400, description='Not a JSON')
        if new_city_name is None:
            abort(400, description='Missing name')
        new_city = City(name=new_city_name, state_id=state_id)
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    list_cities_as_dicts = [s.to_dict() for s in state.cities]
    return jsonify(list_cities_as_dicts)


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_one_city(city_id):
    """
    Retrieves a state by id
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            res_dict = request.get_json()
            res_dict['id'] = city.id
            res_dict['created_at'] = city.created_at
            city.__init__(**res_dict)
            city.save()
            return jsonify(city.to_dict()), 200
        except:
            abort(400, description='Not a JSON')
    return jsonify(city.to_dict())
