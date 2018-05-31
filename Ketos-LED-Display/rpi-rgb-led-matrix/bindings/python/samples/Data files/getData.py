import requests
import json
import fileinput
from datetime import datetime
import time
import logging
import logging.handlers

url = "http://ec2-54-213-39-245.us-west-2.compute.amazonaws.com:5775/api/v1/wave/21/Anahuac%20oi%20oficinas/1525935600000/1526108399827"

def success_callback(response):
    logger.info("API Call Success")
    data = response.json()
    sensors_data = data["sensors_total"]
    f_keys = open('data-keys.txt','w')
    f_values = open('data-values.txt','w')

    for key in sensors_data:
        key_string = json.dumps(key)
        key_string = key_string.replace('"', '')
        key_string = key_string.replace('_', ' ')
        key_string = key_string.replace('total ', '')
        f_keys.write(key_string)
        f_keys.write("\n")
 #       value_string = json.dumps(sensors_data[key])
        value_string = json.dumps(round(sensors_data[key]))
        value_string = value_string.replace('.0', '')
        f_values.write(value_string)
        f_values.write("\n")
    
    f_keys.close()
    f_values.close()
    

def error_callback(response):
    logger.info("API Call FAIL with status code %i and error %s" %response.status_code %response.error)


f = "loadSensorsTotalData.log"
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
    response = requests.get(url)
    response_status = response.status_code
    if(response_status == 200):
        success_callback(response)
        print("ok")
        time.sleep(20)
        #break
    else:
        error_callback(response)
        time.sleep(60)


