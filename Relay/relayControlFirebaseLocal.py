import time
import RPi.GPIO as GPIO
import json
import os
import pyrebase

###########################################
# cd to Script Directory
###########################################
scriptDirectory = os.path.dirname(os.path.realpath(sys.argv[0]))
print(scriptDirectory)
os.chdir(scriptDirectory)
# file = open("../TempSensor/temp.txt", "r")
# print(file.read())

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

####### Referring to the pin number #######
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

####### Initiate list with pin numbers #######
#empty = NA #Relay1
heaterPin = 32 #Relay2
acPin = 38 #Relay3
fanPin = 40 #Relay4
pinList = [heaterPin, acPin, fanPin]

####### Define pin modes and set to off (Default) #######
for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, 1) #1 is off and 0 is on

####### Define Upper and Lower Bounds for On #######
threshold = 2
topThreshold = 1+threshold
bottomThreshold = 1-threshold

####### Initialize Verification Variables #######
sysVOld = True
acVOld = False
heaterVOld = False
fanVOld = False

while True:
    ####### Try Opening the Database File and Importing Data #######
    try:
        with open('../Firebase/firebaseData.json') as json_data:
            firebaseData = json.load(json_data)
    except:
        pass

    ####### Sort Data into Elements #######
    for key,val in firebaseData.items():
        exec(key + '=val')

    ####### Try Opening the Temperature File and Importing Data #######
    try:
        with open('../TempSensor/temp.json') as json_data:
            tempData = json.load(json_data)
    except:
        pass

    ####### Sort Data into Elements #######
    for key,val in tempData.items():
        exec(key + '=val')

    ####### Control Relay #######
    if systemMode == 0:
        GPIO.output(heaterPin, 1) # Set heater to off
        GPIO.output(acPin, 1) # Set ac to off
        systemV = False
        acV = False
        heaterV = False
        if fanMode == "on":
            GPIO.output(fanPin, 0) # Set fan to on
            fanV = True
        if fanMode == "auto":
            GPIO.output(fanPin, 1) # Set fan to off
            fanV = False

    if systemMode == 1:
        systemV = True
        ### Auto Fan Mode ###
        if fanMode == "auto":
            if airMode == "ac":
                if tempLocal == setPoint or tempLocal < setPoint:
                    GPIO.output(fanPin, 1) # Set fan to off
                    GPIO.output(heaterPin, 1) # Set heater to off
                    GPIO.output(acPin, 1) # Set ac to off
                    acV = False
                    heaterV = False
                    fanV = False
                if tempLocal >= round(setPoint+threshold):
                    GPIO.output(heaterPin, 1) # Set heater to off
                    GPIO.output(fanPin, 0) # Set fan to on
                    GPIO.output(acPin, 0) # Set ac to on
                    acV = True
                    heaterV = False
                    fanV = True

            if airMode == "heater":
                if tempLocal == setPoint or tempLocal > setPoint:
                    GPIO.output(fanPin, 1) # Set fan to off
                    GPIO.output(acPin, 1) # Set heater to off
                    GPIO.output(heaterPin, 1) # Set ac to off
                    acV = False
                    heaterV = False
                    fanV = False
                if tempLocal <= round(setPoint-threshold):
                    GPIO.output(acPin, 1) # Set heater to off
                    GPIO.output(fanPin, 0) # Set fan to on
                    GPIO.output(heaterPin, 0) # Set ac to on
                    acV = False
                    heaterV = True
                    fanV = True

        ### Manual Fan Mode ###
        if fanMode == "on":
            GPIO.output(fanPin, 0) # Set fan to on
            fanV = True

    ## Update Verification Status Only If They Change ##
    if systemV != sysVOld or acV != acVOld or heaterV != heaterVOld or fanV != fanVOld:
        sysVOld = systemV
        acVOld = acV
        heaterVOld = heaterV
        fanVOld = fanV

        try:
            db.child("MainThermostat").update({'systemVerify': systemV, 'acVerify': acV, 'heaterVerify': heaterV, 'fanVerify': fanV})
        except:
            pass

    ## Sleep 0.1 seconds before next iteration ##
    time.sleep(0.1)
