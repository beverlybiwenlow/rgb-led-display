import requests
import json
from collections import OrderedDict
import fileinput
from datetime import datetime
import time
import logging
import logging.handlers

url = "http://ec2-54-213-39-245.us-west-2.compute.amazonaws.com:5775"
endpoint = "/api/v1/totals_allcustomers/"

def success_callback(response):
	logger.info("API Call Success")
#	data = response.json()
	data = response.text
	data = json.loads(data, object_pairs_hook=OrderedDict)
	f_keys = open('data_keys.txt','w')
	f_values = open('data_values.txt','w')
#	print(data)
	print(data)

	for key in data:
		key_string = json.dumps(key)
		key_string = key_string.replace('"', '')
		key_string = key_string.replace('_', ' ')
		key_string = key_string.replace('total ', '')
		f_keys.write(key_string)
		f_keys.write("\n")

		if isinstance(data[key], dict):
			value_dict = data[key]
			value_dict["value"] = "{:,}".format(value_dict["value"])
			value_dict["unit"] = value_dict["unit"].replace("gallons", "gal")
			value_string = value_dict["value"] + " " + value_dict["unit"]

		else:
			num = data[key]
			value_string = "{:,}".format(num)

		f_values.write(value_string)
		f_values.write("\n")

	f_keys.close()
	f_values.close()


def error_callback(response):
	logger.info("API Call FAIL with status code %i and error %s" %response.status_code %response.error)


f = "load_sensors_total_data.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
handler = logging.handlers.RotatingFileHandler(f, maxBytes=10000000, backupCount=5)
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

while(True):
	response = requests.get(url + endpoint)
	response_status = response.status_code
	if(response_status == 200):
		success_callback(response)
		print("ok")
		time.sleep(20)
		#break
	else:
		error_callback(response)
		time.sleep(60)
