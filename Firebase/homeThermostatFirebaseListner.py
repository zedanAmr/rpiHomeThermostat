import time
import pyrebase
import json
import os

###########################################
#Initialize Firebase Configuration and DB
###########################################
####### Load Configuration Settings for Firebase Project #######
try:
    with open('/home/pi/rpiHomeThermostat/Firebase/firebaseCredentials.json') as json_data:
        config = json.load(json_data)
except:
    print("Error: Could not load firebaseCredentials")

####### Initialize Firebaseand Set DataBase "db" Instance #######
firebase = pyrebase.initialize_app(config)
db = firebase.database()

####### Define JSON Dict for Thermostat Data Monitoring #######
firebaseData = {}

###########################################
#Run Listner
###########################################
####### Define Listner Function #######
def stream_handler(message):
    ####### Listen to Data #######
    path = message["path"]
    data = message["data"]

    ####### Record Data to JSON #######
    if isinstance(data, dict):
        for i in data:
            firebaseData[i] = data[i]
    elif isinstance(data, int) or isinstance(data, unicode):
        firebaseData[path[1:len(path)]] = data
        
    ####### Write Data to JSON file on OS #######
    try:
        with open('/home/pi/rpiHomeThermostat/Firebase/firebaseData.json', 'w') as json_data:
            json.dump(firebaseData, json_data, sort_keys = True, indent = 4, ensure_ascii = False)
    except:
        pass
    
####### Run Listner Function #######
my_stream = db.child("MainThermostat").stream(stream_handler)
my_stream.close()
