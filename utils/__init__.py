import os
import json
import yaml
import math
import traceback
import numpy as np
import multiprocessing as mp
from time import time
from pathlib import Path
from flask.json import JSONEncoder
from library.logger import logger
from contextlib import contextmanager
from utils.Exception import DataNotReadyException
from bson import json_util, ObjectId
from datetime import datetime, timedelta


def parse_config_env(env):
	config_file = Path(__file__).absolute().parent.parent / "config.yaml"
	if not config_file.exists():
		logger.exception("Missing Configuration file 'config.yaml ")
		raise UserWarning("Missing Configuration file 'config.yaml ")
	config = yaml.safe_load(config_file.read_text())
	env_settings = config[env]
	return env_settings if env_settings else None


def parse_config():
	try:
		env = os.getenv("FLASK_ENV")
	except KeyError:
		logger.exception("The TRC_ENV variable is not set!..Exiting")
		raise UserWarning("Missing TRC_ENV variable ")
	return parse_config_env(env)


class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


# ability to return the process error to the parent for handling
class Process(mp.Process):
	def __init__(self, *args, **kwargs):
		mp.Process.__init__(self, *args, **kwargs)
		self._pconn, self._cconn = mp.Pipe()
		self._exception = None

	def run(self):
		try:
			mp.Process.run(self)
			self._cconn.send(None)
		except BaseException as e:
			tb = traceback.format_exc()
			logger.error(f"{e} during Process {tb}")
			self._cconn.send(e)

	@property
	def exception(self):
		if self._pconn.poll():
			self._exception = self._pconn.recv()
		return self._exception


# context manager for exception swallowing and default setting
@contextmanager
def suppress_with_default(exceptions=Exception, default=np.nan):
	try:
		yield default
	except exceptions as e:
		logger.error(f"Assignment error {e}", exc_info=True)
		pass


# decorator to log and time function
def log(func):
	def wrapper(*args, **kwargs):
		try:
			start = time()
			logger.info("[START FUNCTION] '{0}', parameters : {1} and {2}".format(func.__name__, args, kwargs))
			return func(*args, **kwargs)
		except DataNotReadyException as e:
			logger.info("[DATA_NOT_READY FUNCTION] '{0}', parameters : {1} and {2}".format(func.__name__, args, kwargs))
			raise
		except BaseException as e:
			tb = traceback.format_exc()
			logger.error(f"[ERROR ON FUNCTION] {func.__name__}: {e} {tb}")
			raise
		finally:
			end = time()
			logger.info("[END FUNCTION] '{0}' took {1}s to execute, parameters : {2} and {3}".format(func.__name__, end - start, args, kwargs))
	return wrapper