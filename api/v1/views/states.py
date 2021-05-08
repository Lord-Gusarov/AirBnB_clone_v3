#!/usr/bin/python3
"""
Index for our web flask
"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def list_all_states():
    """
    Returns the list of all State objects
    """

    if request.method == 'POST':
        new_state_name = None
        try:
            res_dict = request.get_json()
            new_state_name = res_dict.get('name')
        except:
            abort(400, description='Not a JSON')
        if new_state_name is None:
            abort(400, description='Missing name')
        new_state = State(name=new_state_name)
        new_state.save()
        return jsonify(new_state.to_dict()), 201
    states = storage.all('State')
    list_states_as_dicts = [s.to_dict() for s in states.values()]
    return jsonify(list_states_as_dicts)


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_one_state(state_id):
    """
    Retrieves a state by id
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            res_dict = request.get_json()
            res_dict['id'] = state.id
            res_dict['created_at'] = state.created_at
            state.__init__(**res_dict)
            state.save()
            return jsonify(state.to_dict()), 200
        except:
            abort(400, description='Not a JSON')
    return jsonify(state.to_dict())
