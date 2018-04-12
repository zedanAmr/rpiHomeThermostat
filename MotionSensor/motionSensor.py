#!/usr/bin/python

import time
import RPi.GPIO as GPIO

# Referring to the pin number not name (reference GPIO Header Map)
GPIO.setmode(GPIO.BOARD)

# Initiate list with output pin numbers
#Pin1 = 12
#Pin2 = 36
#Pin3 = 38
#Pin4 = 40
#pinListOut = [Pin1, Pin2, Pin3, Pin4]

# Initiate list with input pin numbers
motionSensorPin = 12
pinListIn = [motionSensorPin]

# Define Output pin modes and set to off (Default)
#for i in pinListOut:
    #GPIO.setup(i, GPIO.OUT)
    #GPIO.output(i, 1) #1 is off and 0 is on

# Define Input pin modes
for i in pinListIn:
    GPIO.setup(i, GPIO.IN)

while True:
    # Store Motion Sensor Signal
    motionSensorSignal=GPIO.input(motionSensorPin)

    # If there is no motion do action
    if motionSensorSignal==0:
        print "Coast is clear",motionSensorSignal
        #time.sleep(2)
        
    # If there is motion do different action
    elif motionSensorSignal==1:
        print "Intruder detected",motionSensorSignal
        #time.sleep(2)
