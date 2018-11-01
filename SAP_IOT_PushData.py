####################################################################################################
#'''
# Created on 24.07.2017 initially
# This program reads sensor data from a few sensors *humidity, temperature, light) Raspberry PI 3
# and pushes the data into the SAP Cloud Platform IoT Services for cloud foundry
#
# It needs to be run with Python 3 interpreter and the script needs to be
# located at the following path on your Raspberry PI:
# /home/pi/Desktop/GrovePi/Software/Python
# @author: Matthias Allgaier, SAP SE / Martin Ebert, SAP SE
#'''
####################################################################################################

import sys
sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')
import requests
import json
import time
import math
import random
import os
import Adafruit_DHT
import RPi.GPIO as GPIO
from Naked.toolshed.shell import muterun_js
from uuid import getnode as get_mac
import socket

####################################################################################################
#''' please enter your alternate device ID and your alternate sensorID in the variables below
#for deviceid the hostname is used:
deviceId = socket.gethostname()

#for the sensorid the last two digits of the hostname is used
sensorAlternateId = 'sensor'+ socket.gethostname()[-2:]
sensorTypeAlternateId = socket.gethostname()[-2:]

#'''
####################################################################################################

#call node script for converting the certificate from json to pem
response = muterun_js('/home/pi/converter/converter.js')
if response.exitcode == 0:
    print(response.stdout)
else:
    print(response.stderr)
    exit(3)


# find out mac address and hostname
#deviceID = mac
#for i in range (16-len(mac)):
#    deviceID= deviceID + '0'

#mac = (hex(get_mac())).lstrip('0x')
#host = socket.gethostname()
#hostn = int(host[3:])
# tenant = 'https://iotaeexplore.eu10.cp.iot.sap/iot/gateway/rest/measures/'
# tenant = 'https://304dfcd6-d9b4-4fa8-b7e0-e18e11196aa9.eu10.cp.iot.sap/iot/gateway/rest/measures/'
# tenant = 'https://presales-it.eu10.cp.iot.sap/iot/gateway/rest/measures/'

tenant = 'http://192.168.1.36:8699/measures/'

postAddress = (tenant + deviceId)
factor = 0

#print ('MAC:' , mac)
print ('Device ID: ', deviceId)
print ('Sensor ID: ', sensorAlternateId)
#print ('Hostname:', host)
print ('Posting to:', postAddress)

# Time intervall for polling the sensor data in seconds
# timeIntervall = 5
timeIntervall = 1

#'''
# Sensor & Measure Definitions
# ====================================
# Sensor 1: Temperature (analog)   -> GPIO 4
# Sensor 2: Humidity (analog)      -> GPIO 4
# Sensor 3: Light Switch (digital) -> GPIO 17
#'''

# Setup Light Sensor
# Set GPIO Mode to BCM and define GPIO17 (#11) as input, initial value 0)

GPIOPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIOPin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
valueLight = 0

while True:
    
    try:
        print("")
        print("============================================")
        print("Reading sensor data ...")
  
        # Read temperature & humiditiy 
        # GPIO 4 Setup (Combined sensor for temperature and humidity DHT11)

        humidity, temperature = Adafruit_DHT.read_retry(11,4)
        if math.isnan(humidity) == False and math.isnan(temperature) == False:
            valueHumidity = humidity
            valueTemp = temperature
            valueTempF = temperature * 1.8 + 32
            print("Temperature value = %d" %valueTemp, "°C", "/ %d°F" %valueTempF)
            print("Hummidity value = %d" %valueHumidity, "%")

        # Read Light Sensor via Digital Input GPIO17 (Pin#11)
        factor = random.uniform(0.01, 0.1)
        if GPIO.input(17) == GPIO.HIGH:
            valueLight = (1 - factor) * 1000
        else:
            valueLight = (0 + factor) * 1000
        print("Light value = %f" %valueLight, "Lum")
        
####################################################################################################
# Create http post
####################################################################################################



#        data = json.dumps({"capabilityAlternateId":"d14db55aec99c947", "measures":[[valueTemp,valueLight,valueHumidity]],"sensorAlternateId": sensorId})
#        headers = {'content-type': 'application/json'}
#        r = requests.post(postAddress,data=data, headers = headers,cert='/home/pi/converter/keyStore.pem', timeout=5)
#        responseCode = r.status_code
#        print ("==> HTTP Response: %d" %responseCode)

#       data = json.dumps({ \"capabilityAlternateId\":\"d14db55aec99c947\", \"sensorTypeAlternateId\": "sensorId",  \"measures\": [ [ \"temperature\" : "str(valueTemp)", \"light\" : "str(valueLight)", \"humidity\" : "str(valueHumidity)" ] ] })

#        data = json.dumps({ \"capabilityAlternateId\":\"d14db55aec99c947\", \"measures\":[[ \"temperature\" : "valueTemp", \"light\" : "valueLight", \"humidity\" : "valueHumidity]],"\sensorId\": \"sensorId\"}) 

#        data = "{\"capabilityAlternateId\": \"d14db55aec99c947\", \"measures\": [[\""+valueTemp+"\", \""+valueLight+"\", \""+valueHumidity+"\"]],\"sensorTypeAlternateId\": \""+sensorId+"\"}"

        strTemp=str(valueTemp) 
        strLight=str(valueLight) 
        strHumidity=str(valueHumidity) 

#        data = "{\\\"capabilityAlternateId\\\": \\\"d14db55aec99c947\\\", \\\"measures\\\": [[\\\""+strTemp+"\\\", \\\""+strLight+"\\\", \\\""+strHumidity+"\\\"]],\\\"sensorTypeAlternateId\\\": \\\""+sensorTypeAlternateId+"\\\",\\\"sensorAlternateId\\\": \\\""+sensorAlternateId+"\\\"}"
        data = "{\\\"capabilityAlternateId\\\": \\\"intEnv\\\", \\\"measures\\\": [[\\\""+strLight+"\\\", \\\""+strHumidity+"\\\", \\\""+strTemp+"\\\"]],\\\"sensorTypeAlternateId\\\": \\\"50\\\"}"
        data_onlyTemp = "{\\\"capabilityAlternateId\\\": \\\"100-30\\\", \\\"measures\\\": [[\\\""+strTemp+"\\\"]],\\\"sensorTypeAlternateId\\\": \\\"30\\\",\\\"sensorAlternateId\\\": \\\"30100-30\\\"}"
        data_onlyLight = "{\\\"capabilityAlternateId\\\": \\\"102-29\\\", \\\"measures\\\": [[\\\""+strLight+"\\\"]],\\\"sensorTypeAlternateId\\\": \\\"29\\\",\\\"sensorAlternateId\\\": \\\"29102-29\\\"}"


        certfile='/home/pi/converter/keyStore.pem'



        print ("POST data: %s" %data) 
        
        command = "curl -v -H 'Content-Type: application/json' --cert '"+certfile+"' -d \""+data+"\" "+postAddress
        print ("command=%s" %command)
        os.system(command)

        
        # wait timeIntervall [s] before reading the sensor values again
        time.sleep(timeIntervall)

        command = "curl -v -H 'Content-Type: application/json' --cert '"+certfile+"' -d \""+data_onlyTemp+"\" "+postAddress
        print ("command=%s" %command)
        os.system(command)
        command = "curl -v -H 'Content-Type: application/json' --cert '"+certfile+"' -d \""+data_onlyLight+"\" "+postAddress
        print ("command=%s" %command)
        os.system(command)

        # wait timeIntervall [s] before reading the sensor values again
        time.sleep(timeIntervall)


        
    except IOError:
        print ("Error")
       
