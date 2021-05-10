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
    list_amenities_dict = [a.to_dict() for a in place.amenities]
    return jsonify(list_amenities_dict)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
def manage_single_amenity(place_id, amenity_id):
    """
    Allows management of an amenity inside a place
    """
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if request.method == 'POST':
        new_amenity_text = None
        res_dict = None
        try:
            res_dict = request.get_json()
            new_amenity_text = res_dict.get('text')
        except:
            abort(400, description='Not a JSON')
        new_amenity = Amenity(text=new_amenity_text, place_id=place_id,
                              amenity_id=amenity_id)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201

    if request.method == 'DELETE':
        if storage_t == 'db':
            list_id = [a.id for a in place.amenities]
            if amenity_id in list_id:
                place.amenities.remove(amenity_id)
                storage.save()
                return jsonify({}), 200
            else:
                abort(404)
        else:
            if amenity_id in place.amenity_ids:
                place.amenity_ids.remove(amenity_id)
                storage.save()
            else:
                abort(404)
