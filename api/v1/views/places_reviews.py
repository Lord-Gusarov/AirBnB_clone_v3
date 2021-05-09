#!/usr/bin/python3
"""
Index for our web flask
"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def list_all_reviews(place_id):
    """
    Returns the list of all Reviews of a Place
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if request.method == 'POST':
        new_review_text = None
        res_dict = None
        try:
            res_dict = request.get_json()
            new_review_text = res_dict.get('text')
        except:
            abort(400, description='Not a JSON')
        user_id = res_dict.get('user_id')
        if user_id is None:
            abort(400, description='Missing user_id')
        user = storage.get('User', user_id)
        if user is None:
            abort(404)
        if new_review_text is None:
            abort(400, description='Missing txt')
        new_review = Review(text=new_review_text, place_id=place_id,
                            user_id=user_id)
        new_review.save()
        return jsonify(new_review.to_dict()), 201
    list_reviews_as_dicts = [r.to_dict() for r in place.reviews]
    return jsonify(list_reviews_as_dicts)


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def acess_one_review(review_id):
    """
    Retrieves a state by id
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            res_dict = request.get_json()
            res_dict.update({'id': review_id, 'created_at': review.created_at})
            for att in ['user_id', 'place_id']:
                res_dict.pop(att, None)
            review.__init__(**res_dict)
            review.save()
            return jsonify(review.to_dict()), 200
        except:
            abort(400, description='Not a JSON')
    return jsonify(review.to_dict())
