import datetime
import secrets
from flask import Flask, Response
from flask_caching import Cache
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from utils import MongoJsonEncoder
from pathlib import Path
from flask_cors import CORS
import os
import utils
import simplejson
import http.client
from library.logger import logger

# globally accessible
cache = Cache()

CACHE_TIMEOUT = 180
# application timeout for third party APIs requests (120s)
WAIT_TIMEOUT = 60
# max number of retries for a request
MAX_REQUEST_RETRY_COUNT = 3
# exponential multiplier wait between retries in s (2^x)
WAIT_EXPONENTIAL_MULTIPLIER = 1


# log all requests module call to log file
# only log url, X-USER-ID header identified person making the request)
def print_to_log(*args, **kwargs):
	if args[0] == 'send:':
		value = args[1]
		if isinstance(args[1], (bytes, bytearray)):
			value = args[1].decode("utf-8")
		tokens = value.split('\\r\\n')
		url_and_method = tokens[0]
		logger.info(f"[START REQUEST] {url_and_method}")

http.client.print = print_to_log
http.client.HTTPConnection.debuglevel = 2

def create_app():
	info = utils.parse_config()

	_app = Flask(__name__)

	_app.secret_key = os.urandom(24)
	CORS(_app)

	# load Mongo JSON Encoder
	_app.json_encoder = MongoJsonEncoder

	# max payload per request: 16MB (should be more than enough)
	_app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

	# get path of the project
	_app.config['ROOT_PATH'] = f"{Path(__file__).parent}"

	# if hasattr(info, 'domain'):
	# 	_app.config['JWT_COOKIE_DOMAIN'] = info['domain']
	# _app.config["JWT_SECRET_KEY"] = secrets.token_bytes(32)
	# _app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=120)
	# _app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
	# _app.config["JWT_COOKIE_SECURE"] = True
	# _app.config["SQLALCHEMY_DATABAS_EURI"] = "sqlite://"
	# _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

	# initialize db
	#db.init_app(_app)

	# initialize cache
	cache_config = {'CACHE_TYPE': 'null'}
	if info['is_data_cache_enabled'] is True:
		cache_config = {
			'CACHE_TYPE': 'filesystem',
			'CACHE_DIR': 'cache-directory'
		}
	_app.config['CACHE_TIMEOUT'] = CACHE_TIMEOUT
	_app.config.from_mapping(cache_config)
	cache.init_app(_app)

	# swagger url for ui and json
	# default response is 200 json if nothing else is specified when using flaskapispec
	def format_response(obj):
		# dont encode twice if its already valid json
		try:
			simplejson.loads(obj)
		except Exception as e:
			return Response(response=simplejson.dumps(obj, ignore_nan=True, default=str))
		return Response(response=obj)

	_app.config.update({
		'APISPEC_SPEC': APISpec(
			title='Python Flask',
			version='v0.1',
			plugins=[MarshmallowPlugin()],
			openapi_version="2.0"
		),
		"APISPEC_FORMAT_RESPONSE": format_response,
		"APISPEC_SWAGGER_UI_URL": "/docs/",
		"APISPEC_SWAGGER_URL": "/swagger/"
	})

	with _app.app_context():
		# keep it
		import app
		return _app


if __name__ == '__main__':
	from werkzeug.serving import run_simple
	from werkzeug.middleware.dispatcher import DispatcherMiddleware

	app = create_app()
	if os.getenv("FLASK_ENV") == 'development':
		app.config['DEBUG'] = True

	application = DispatcherMiddleware(Flask(__name__), {
		'/api': app,
	})
	run_simple('127.0.0.1', 5000, application, use_reloader=True, threaded=True)
