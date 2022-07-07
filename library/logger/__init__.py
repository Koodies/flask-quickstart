""" 
Logger for the project. 
Writes the logs under ./logs of root path if main.py file is ran 
or local logs folder if __init__.py file are ran.
"""
import copy
import datetime
import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pythonjsonlogger import jsonlogger
from pathlib import Path


# from current_user import get_current_user_id


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            log_record['t'] = f"{datetime.now():%Y-%m-%dT%H:%M:%S.%fZ}"
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
# log_record['user'] = get_current_user_id()


# create logger
logger = logging.getLogger('TRC')
logger.setLevel(logging.DEBUG)
formatter = CustomJsonFormatter(
    '(t) (level) (user) (message) (pathname) (funcName) (module) (lineno) (process) (thread)')

# create file handler which logs even debug messages
# try:
# 	logfile = os.getenv("LogFilePath")
# 	# fh = logging.FileHandler(logfile)
# 	# fh.setLevel(logging.DEBUG)
# 	# fh.setFormatter(formatter)

# 	# create a log rotation daily, 1 log file per day, rollover at midnight
# 	fh = TimedRotatingFileHandler(logfile, when="midnight", interval=1)
# except:
# 	logfile = f"{Path(__file__).parent.parent.parent}{os.sep}logs{os.sep}TRC.log"
# 	fh = TimedRotatingFileHandler(logfile, when="midnight", interval=1)

# the date string will be appended to the log file name when it rotates
# fh.suffix = "%Y%m%d"
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(formatter)

# logger.addHandler(fh)

# for local dev environment only, will print out the logger messages to the console
# extend logger methods (debug, info, error, warning, critical) to also write to console when env == dev
if os.getenv('FLASK_ENV') == 'development':
    # methods that will be extended
    method_to_extend = ['info', 'debug', 'error', 'warning', 'critical']
    __temp = {}


    # will create dynamic extended method for each logger methods
    def extend_logger(func):
        def _function(msg, *args, **kwargs):
            # print out the msg
            print(msg)
            func(msg, *args, **kwargs)

        return _function


    for i in method_to_extend:
        if hasattr(logger, i):
            # copy the method
            __temp[i] = copy.copy(getattr(logger, i))

            # overwrite the method with the extended method
            setattr(logger, i, extend_logger(__temp[i]))

if __name__ == "__main__":
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')
    logger.info("classic message", extra={"message_from": "henry", "query": "about citi"})
