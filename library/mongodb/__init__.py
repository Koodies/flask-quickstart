from pymongo import MongoClient, ASCENDING
import os
import utils
import datetime


#TODO: not using mongodb connection pooling

def get_mongo_db():
	cfg = utils.parse_config()
	db_name = cfg['MONGODB']['INSTANCE']
	client = MongoClient(os.getenv("TRC_MONGODB_CONN"))
	return client[db_name]


def add_case(case):
	return get_mongo_db().test_users.insert_one(case).inserted_id


def get_case(filter={}, projection={}):
	return get_mongo_db().test_users.find_one(filter, projection)


def get_cases(filter={}):
	return get_mongo_db().test_users.find(filter)


def update_case(filter={}, update={}):
	result = get_mongo_db().test_users.update_one(filter, {'$set':update})
	return result.matched_count and result.modified_count


def delete_case(filter={}):
	result = get_mongo_db().test_users.delete_one(filter)
	return result.deleted_count == 1


if __name__ == '__main__':
	cases = get_latest_cases()
	for case in cases:
		print(case['alert_id'])
