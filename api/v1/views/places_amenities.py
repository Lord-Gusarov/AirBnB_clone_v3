#!/usr/bin/python3
"""
Index for our web flask
"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage_t, storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def list_places_amenities(place_id):
    """
    Returns a list of all amenities in a place object
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    else:
        list_amenities_dict = [a.to_dict() for a in place.amenities]
        return jsonify(list_amenities_dict)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
def manage_single_amenity(place_id, amenity_id):
    """
    Allows management of an amenity inside a place
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if request.method == 'POST':
        new_amenity_text = None
        res_dict = None
        try:
            res_dict = request.get_json()
            new_amenity_text = res_dict.get('text')
        except:
            abort(400, description='Not a JSON')
        amenity = storage.get('Amenity', amenity_id)
        if amenity is None:
            abort(404)
        new_amenity = Amenity(text=new_amenity_text, place_id=place_id,
                              amenity_id=amenity_id)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201

    if request.method == 'DELETE':
        place = stoage.get('Place', place_id)
        if place is None:
            abort(404)
        amenity = storage.get('Amenity', amenity_id)
        if amenity is None:
            abort(404)
        else:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
