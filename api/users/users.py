from flask.helpers import make_response
from flask.json import jsonify
from flask import request
from api import api
from flask_apispec import use_kwargs, marshal_with
from marshmallow import fields
from library.logger import logger
from library.mongodb import add_case, get_case, update_case, delete_case
from schemas.User import UserSchema
from bson.objectid import ObjectId
import utils


# Main Route
@api.route('/user/<string:id>', methods=['GET'])
def get_user(id):
        try:
                user = get_case({'_id': ObjectId(id)})
                logger.info(f'User id: {id} found')
                data = utils.mongo_encoder(user)
                resp = make_response(jsonify(status='success', data=data))
                return resp
        except Exception as e:
                logger.error(f"{e}")
                resp = make_response(jsonify(status='error', message=f'{e}'))
                return resp


@api.route('/user', methods=['POST'])
@use_kwargs({
        "name": fields.String(required=True)
})
@marshal_with(UserSchema, code=200, apply=False)
def create_new_user(**kwargs):
        data = dict(**kwargs)
        user = {'name':data.get('name')}
        id = add_case(user)
        logger.info(f'User id: {id} created')
        payload = {"id":str(id)}
        resp = make_response(jsonify(status='success',data=payload),201)
        return resp


@api.route('/user/<string:id>', methods=['PUT'])
@use_kwargs({
        "name": fields.String(required=False)
})
@marshal_with(UserSchema, code=200, apply=False)
def update_user(id, **kwargs):
        try:
                data = dict(**kwargs)
                user = {'name':data.get('name')}
                result = update_case({'_id': ObjectId(id)}, user)
                if not bool(result): raise NameError('Failed to update user')
                logger.info(f'User id: {id} updated')
                resp = make_response(jsonify(status='success', message=f'Successfully update 1 new user with id: {id}'), 200)
                return resp
        except Exception as e:
                logger.error(f'{e}')
                resp = make_response(jsonify(status='error', message=f'{e}'))
                return resp


@api.route('/user/<string:id>', methods=['DELETE'])
def delete (id):
        try:
                result = delete_case({'_id': ObjectId(id)})
                if not result: raise NameError('Failed to delete user')
                logger.info(f'User id: {id} deleted')
                resp = make_response(jsonify(status='success', message=f'Successfully delete 1 user with id: {id}'), 200)
                return resp
        except Exception as e:
                logger.error(f'{e}')
                resp = make_response(jsonify(status='error', message=f'{e}'))
                return resp

