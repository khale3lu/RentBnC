#!/usr/bin/python3
""" objects that handle all default RestFul API actions for States """
from models.rentbnc_place import RentbncPlace
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/rentbncplaces', methods=['GET'], strict_slashes=False)
@swag_from('documentation/rentbncplace/get_rentbncplace.yml', methods=['GET'])
def get_rentbncplaces():
    """
    Retrieves the list of all RentbncPlace objects
    """
    all_rentbncplaces = storage.all(RentbncPlace).values()
    list_places = []
    for rentbncplace in all_rentbncplaces:
        list_places.append(rentbncplace.to_dict())
    return jsonify(list_places)


@app_views.route('/rentbncplaces/<rentbncplace_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/rentbncplace/get_id_rentbncplace.yml', methods=['get'])
def get_rentbncplace(rentbncplace_id):
    """ Retrieves a specific RentbncPlace """
    rentbncplace = storage.get(RentbncPlace, rentbncplace_id)
    if not rentbncplace:
        abort(404)

    return jsonify(rentbncplace.to_dict())


@app_views.route('/rentbncplaces/<rentbncplace_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/rentbncplace/delete_rentbncplace.yml', methods=['DELETE'])
def delete_rentbncplace(rentbncplace_id):
    """
    Deletes a RentbncPlace Object
    """

    rentbncplace = storage.get(RentbncPlace, rentbncplace_id)

    if not rentbncplace:
        abort(404)

    storage.delete(rentbncplace)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/rentbncplaces', methods=['POST'], strict_slashes=False)
@swag_from('documentation/rentbncplace/post_rentbncplace.yml', methods=['POST'])
def post_rentbncplace():
    """
    Creates a RentbncPlace
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'city' not in request.get_json():
        abort(400, description="Missing name")
    if 'address' not in request.get_json():
        abort(400, description="Missing address")
    if 'owner_email' not in request.get_json():
        abort(400, description="Missing owner email")
    if 'price' not in request.get_json():
        abort(400, description="Missing price")
    if 'description' not in request.get_json():
        abort(400, description="Missing description")

    data = request.get_json()
    instance = RentbncPlace(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/rentbncplaces/<rentbncplace_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/rentbncplace/put_rentbncplace.yml', methods=['PUT'])
def put_rentbncplace(rentbncplace_id):
    """
    Updates a RentbncPlace
    """
    rentbncplace = storage.get(RentbncPlace, rentbncplace_id)

    if not rentbncplace:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(rentbncplace, key, value)
    storage.save()
    return make_response(jsonify(rentbncplace.to_dict()), 200)
