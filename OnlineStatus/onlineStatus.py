#!/usr/bin/python

import time
import pyrebase
import json
import datetime
import os
import sys

###########################################
# cd to Script Directory
###########################################
scriptDirectory = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(scriptDirectory)

###########################################
#Initialize Firebase Configuration and DB
###########################################
####### Load Configuration Settings for Firebase Project #######
try:
    with open('../../firebaseCredentials/firebaseCredentials.json') as json_data:
        config = json.load(json_data)
except:
    print("Error: Could not load firebaseCredentials")

####### Initialize Firebaseand Set DataBase "db" Instance #######
firebase = pyrebase.initialize_app(config)
db = firebase.database()

## Initialize Old Date and Time
dateOld = 0
timeOld = 0

while True:
    ## Get Current Time and Date
    now = datetime.datetime.now()
    currentDate = now.strftime("%Y-%m-%d")
    currentTime = now.strftime("%H:%M")

    ## Update Device Status ##
    if currentTime != timeOld:
        timeOld = currentTime
        try:
            db.child("MainThermostat").update({"lastOnlineTime": currentTime})
        except:
            pass

    if currentDate != dateOld:
        dateOld = currentDate
        try:
            db.child("MainThermostat").update({"lastOnlineDate": currentDate})
        except:
            pass

    ## Sleep 1 second Before Next Reading ##
    time.sleep(1)
