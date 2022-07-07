from flask import Blueprint
from api.user_v1 import user_api_v1

api = Blueprint('api', __name__)

api.register_blueprint(user_api_v1)