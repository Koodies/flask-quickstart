# from flask import Flask
# from api import api
# from utils import MongoJsonEncoder
# from flask_cors import CORS

# app = Flask(__name__)

# CORS(app)
# app.json_encoder = MongoJsonEncoder
# app.register_blueprint(api)


from flask import current_app as app
from flask_apispec.extension import FlaskApiSpec
from api import api
from datetime import datetime, timedelta, timezone
import os

# generate documentation
# _security_schemes is an internal member, but works anyway
# /!\possibility to break during library update
docs = FlaskApiSpec(app, document_options=True)
#auth_scheme = {"type": "apiKey", "in": "cookie", "name": "jwt"}
#docs.spec.components._security_schemes["cookieAuth"] = auth_scheme


app.register_blueprint(api)
