#!/usr/bin/python3
'''places view'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def search_places_by_city_id(city_id):
    '''Filter cities in state by id'''
    object = storage.get(City, city_id)
    if object is None:
        abort(404)
        return jsonify([place.to_dict() for place in object.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def search_place(place_id):
    '''Filter city by id'''
    object = storage.get(Place, place_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''Delete city of the provided id'''
    object = storage.get(Place, place_id)
    if object is None:
        abort(404)
    else:
        storage.delete(object)
        storage.save()
        # Return an empty dictionary with status code 200
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''Create a new state'''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        city_rev = storage.get(City, city_id)
        if city_rev is None:
            abort(404)
        data = request.get_json()
        # if data is in json format, it return python dict or list
        # If the data is not valid JSON, raise an error or return None
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        user_place = storage.get(User, data["user_id"])
        if user_place is None:
            abort(404)
        if 'name' not in data:
            abort(400, 'Missing name')
        new_place = Place(**data)
        # Create a new instance of state and pass the key value pairs
        setattr(new_place, 'city_id', city_id)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201
    else:
        abort(400, 'Not a JSON')


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''Update city of provided id'''
    object = storage.get(Place, place_id)
    if object is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(object, key, value)
    storage.save()
    return jsonify(object.to_dict()), 200
