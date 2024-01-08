#!/usr/bin/python3
'''places_reviews view'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def search_review_by_places_id(place_id):
    '''Filter cities in state by id'''
    object = storage.get(Place, place_id)
    if object is None:
        abort(404)
    return jsonify([review.to_dict() for review in object.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def search_review(review_id):
    '''Filter city by id'''
    object = storage.get(Review, review_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''Delete city of the provided id'''
    object = storage.get(Review, review_id)
    if object is None:
        abort(404)
    else:
        storage.delete(object)
        storage.save()
        # Return an empty dictionary with status code 200
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''Create a new state'''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        # if data is in json format, it return python dict or list
        # If the data is not valid JSON, raise an error or return None
        place_rev = storage.get(Place, place_id)
        if place_rev is None:
            abort(404)
        data = request.get_json()
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        user_place = storage.get(User, data["user_id"])
        if user_place is None:
            abort(404)
        if 'text' not in data:
            abort(400, 'Missing text')
        new_review = Review(**data)
        # Create a new instance of state and pass the key value pairs
        setattr(new_review, 'place_id', place_id)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201
    else:
        abort(400, 'Not a JSON')

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''Update city of provided id'''
    object = storage.get(Review, review_id)
    if object is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(object, key, value)
    storage.save()
    return jsonify(object.to_dict()), 200