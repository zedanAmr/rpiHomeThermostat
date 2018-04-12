#!/usr/bin/python

import os
import glob
import time
import pyrebase
import json

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

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

####### Initialize Old Temp to Keep Track of Temp Change #######
tempOld = 30

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return int(round(temp_f,0))#, int(round(temp_c,0))
	
while True:
    ## Record Temperature Reading ##
    temp = read_temp()
    #print('temp: ' + repr(temp))

    ## Update the Old Temp and Update Server Only if Temp Changes ##
    if temp != tempOld:
        tempOld = temp
        try:
            with open('/home/pi/rpiHomeThermostat/TempSensor/temp.json', 'w') as json_data:
                json.dump({'tempLocal': temp}, json_data, sort_keys = True, indent = 4, ensure_ascii = False)
        except:
            pass
        try:
            db.child("MainThermostat").update({"currentTemp": temp})
        except:
            pass
         #print('tempOld: ' + repr(tempOld))

    ## Sleep 1 second Before Next Reading ##
    time.sleep(1)
