#!/usr/bin/python3
'''places_amenities view'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.amenity import Amenity
from os import environ


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def search_amenity_by_places_id(place_id):
    '''Filter cities in state by id'''
    object = storage.get(Place, place_id)
    if object is None:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        return jsonify([amenity.to_dict() for amenity in object.amenities])
    else:
        return jsonify([storage.get(Amenity, amenity_id).to_dict() for
                        amenity_id in object.amenity_ids])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    '''Delete city of the provided id'''
    object = storage.get(Place, place_id)
    if object is None:
        abort(404)
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity_obj not in object.amenities:
            abort(404)
        object.amenities.remove(amenity_obj)
    else:
        if amenity_id not in object.amenity_ids:
            abort(404)
        object.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_link_amenity(place_id, amenity_id):
    '''Create a new state'''
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity_obj in place_obj.amenities:
            return jsonify(amenity_obj.to_dict()), 200
        else:
            place_obj.amenities.append(amenity_obj)
    else:
        if amenity_id in place_obj.amenity_ids:
            return jsonify(amenity_obj.to_dict()), 200
        else:
            place_obj.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity_obj.to_dict()), 201
