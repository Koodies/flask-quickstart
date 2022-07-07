from flask.helpers import make_response
from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
# from api import api
from flask_cors import CORS
from marshmallow import fields
from library.logger import logger
from library.mongodb import add_case, get_case, update_case, delete_case
from schemas.User import UserSchema
from bson.objectid import ObjectId
from datetime import datetime

user_api_v1 = Blueprint('user_api_v1', __name__, url_prefix='/v1/user')
CORS(user_api_v1)


# Main Route
@user_api_v1.route('/<string:id>', methods=['GET'])
def get_user(id):
    try:
        user = get_case({'_id': ObjectId(id)})
        logger.info(f'User id: {id} found')
        response = {
            "status": "success",
            "data": user
        }
        return make_response(jsonify(response))
    except Exception as e:
        logger.error(f"{e}")
        response_object = {
            'error': {'internal': e}
        }
        return make_response(jsonify(response_object)), 500


@user_api_v1.route('/', methods=['POST'])
@use_kwargs({
    "name": fields.String(required=True)
})
@marshal_with(UserSchema, code=200, apply=False)
def create_new_user(**kwargs):
    data = dict(**kwargs)
    user = {'name': data.get('name')}
    id = add_case(user)
    logger.info(f'User id: {id} created')
    payload = {"id": str(id)}
    return make_response(jsonify(status='success', data=payload), 201)


@user_api_v1.route('/<string:id>', methods=['PUT'])
@use_kwargs({
    "name": fields.String(required=True),
})
@marshal_with(UserSchema, code=200, apply=False)
def update_user(id, **kwargs):
    try:
        data = dict(**kwargs)
        print(data)
        for value in data:
            print(value)
    except Exception as e:
        logger.error(e)
        response_object = {
            'error': {'internal': e}
        }
        return make_response(jsonify(response_object)), 500


@user_api_v1.route('/<string:id>', methods=['PATCH'])
@use_kwargs({
    "name": fields.String(required=False)
})
@marshal_with(UserSchema, code=200, apply=False)
def patch_user(id, **kwargs):
    try:
        data = dict(**kwargs)
        user = {'name': data.get('name'), 'updated': datetime.now()}
        edit_result = update_case({'_id': ObjectId(id)}, user)
        if edit_result.modified_count == 0: raise ValueError('no document updated')
        logger.info(f'User id: {id} updated')
        resp = make_response(jsonify(status='success', message=f'Successfully update 1 new user with id: {id}'), 200)
        return resp
    except Exception as e:
        logger.error(f'{e}')
        response_object = {
            'error': {'internal': e}
        }
        return make_response(jsonify(response_object)), 500


@user_api_v1.route('/<string:id>', methods=['DELETE'])
def delete(id):
    try:
        delete_result = delete_case({'_id': ObjectId(id)})
        if delete_result.deleted_count == 0: raise ValueError('no document deleted')
        logger.info(f'User id: {id} deleted')
        resp = make_response(jsonify(status='success', message=f'Successfully delete 1 user with id: {id}'), 200)
        return resp
    except Exception as e:
        logger.error(f'{e}')
        response_object = {
            'error': {'internal': e}
        }
        return make_response(jsonify(response_object)), 500
