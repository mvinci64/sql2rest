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
# sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')
import requests
import json
import time
import math
import random
import os
# import Adafruit_DHT
# import RPi.GPIO as GPIO
from Naked.toolshed.shell import muterun_js
# from uuid import getnode as get_mac

import socket

# new for odbc connection
import pyodbc 


#############################
#''' please enter your alternate device ID and your alternate sensorID in the variables below
deviceId = '00000P000007968174'
deviceAlternateId = '00000P000007968174'
sensorId = 'SPDM'
sensorAlternateId = '10002'

#######################################################################
# tenant = 'https://iotaeexplore.eu10.cp.iot.sap/iot/gateway/rest/measures/'
# tenant = 'https://304dfcd6-d9b4-4fa8-b7e0-e18e11196aa9.eu10.cp.iot.sap/iot/gateway/rest/measures/'
# tenant = 'http://192.168.1.36:8699/measures/'


tenant = 'https://presales-it.eu10.cp.iot.sap/iot/gateway/rest/measures/'
postAddress = (tenant + deviceId)
#######################################################################

#call node script for converting the certificate from json to pem
response = muterun_js('converter.js')
if response.exitcode == 0:
    print(response.stdout)
else:
    print(response.stderr)
    exit(3)




connection = pyodbc.connect("DSN=SQLServer;uid=USR_SAP;pwd=USR_SAP", autocommit=True) 

if connection :
        print("YES we are connected! \n")
        print ('Device ID: ', deviceId)
        print ('Sensor ID: ', sensorAlternateId)
        print ('Posting to:', postAddress)
        with open("config/config.json", "r") as read_file:
                configdata = json.load(read_file)

        print ('DeviceID', configdata["sensors"][0]["deviceAltId"])


sql='''\
SELECT 
        [DataSms]
        ,[Cod_PuntoMisura]
        ,[ID_PuntoMisura]
        ,[ID_Attributo]
        ,[NomeAttributo]
        ,[UltimaLettura]
        ,[MAX1]
        ,[MED1]
        ,[MIN1]
        ,[SQM1]
        ,[NAL1]
        ,[TFL1]
        ,[TGC1]
        ,[MAX2]
        ,[MED2]
        ,[MIN2]
        ,[SQM2]
        ,[NAL2]
        ,[TFL2]
        ,[TGC2]
        FROM dbo.V_2I_SAP_2018  WHERE Cod_PuntoMisura = '00000P000007968174' AND DataSms > '2018-01-02T00:00:00.000' ORDER BY DataSms

'''

cursor = connection.execute(sql)

for c in cursor:
        DataSMS = c[0]
        CODPuntoMisura = c[1]
        IDPuntoMisura = c[2]
        IDAttributo = c[3]
        NomeAttributo = c[4]
        UltimaLettura = c[5]
        MAX1 = c[6]
        MED1 = c[7]
        MIN1 = c[8]
        SQM1 = c[9]
        NAL1 = c[10]
        TFL1 = c[11]
        TGC1 = c[12]
        MAX2 = c[13]
        MED2 = c[14]
        MIN2 = c[15]
        SQM2 = c[16]
        NAL2 = c[17]
        TFL2 = c[18]
        TGC2 = c[19]

        print("CODPuntoMisura:", c[1],"DataSMS:", str(c[0]))


####################################################################################################
# Create http post
####################################################################################################
        data = json.dumps({"capabilityAlternateId":"100001", "measures":[[IDAttributo,NomeAttributo,IDPuntoMisura,CODPuntoMisura,str(DataSMS),float(MIN1),float(MED1),float(MAX1),float(SQM1),float(NAL1),float(TFL1),str(TGC1),float(MIN2),float(MED2),float(MAX2),float(SQM2),float(NAL2),float(TFL2),str(TGC2)]],"sensorAlternateId": sensorAlternateId})
        dataul = json.dumps({"capabilityAlternateId":"100003", "measures":[[str(UltimaLettura)]],"sensorAlternateId": sensorAlternateId})
        headers = {'content-type': 'application/json'}

#   certfile='config/certificates/00000P000007968174-device_certificate.pem'

        r1 = requests.post(postAddress,data=data, headers = headers,cert='config/converter/keyStore.pem')
        r2 = requests.post(postAddress,data=dataul, headers = headers,cert='config/converter/keyStore.pem')
        responseCode1 = r1.status_code
        responseCode2 = r2.status_code

        print ("POST data: %s" %data) 
        print ("POST data: %s" %dataul) 
        print ("==> HTTP Responses: %d" %responseCode1)
        print ("==> HTTP Responses: %d" %responseCode2)

#        print ('Data: ', data)


# except IOError:
#   print ("Error")

# factor = 0

####################################################################################################
# Create CURL commands to run on On-Premise EDGE Gateway and EDGE Services
####################################################################################################

#       data = json.dumps({ \"capabilityAlternateId\":\"d14db55aec99c947\", \"sensorTypeAlternateId\": "sensorId",  \"measures\": [ [ \"temperature\" : "str(valueTemp)", \"light\" : "str(valueLight)", \"humidity\" : "str(valueHumidity)" ] ] })
#       data = json.dumps({ \"capabilityAlternateId\":\"d14db55aec99c947\", \"measures\":[[ \"temperature\" : "valueTemp", \"light\" : "valueLight", \"humidity\" : "valueHumidity]],"\sensorId\": \"sensorId\"}) 
#       data = "{\"capabilityAlternateId\": \"d14db55aec99c947\", \"measures\": [[\""+valueTemp+"\", \""+valueLight+"\", \""+valueHumidity+"\"]],\"sensorTypeAlternateId\": \""+sensorId+"\"}"

#       strTemp=str(valueTemp) 
#       strLight=str(valueLight) 
#       strHumidity=str(valueHumidity) 

#        data = "{\\\"capabilityAlternateId\\\": \\\"d14db55aec99c947\\\", \\\"measures\\\": [[\\\""+strTemp+"\\\", \\\""+strLight+"\\\", \\\""+strHumidity+"\\\"]],\\\"sensorTypeAlternateId\\\": \\\""+sensorTypeAlternateId+"\\\",\\\"sensorAlternateId\\\": \\\""+sensorAlternateId+"\\\"}"
#        data = "{\\\"capabilityAlternateId\\\": \\\"intEnv\\\", \\\"measures\\\": [[\\\""+strLight+"\\\", \\\""+strHumidity+"\\\", \\\""+strTemp+"\\\"]],\\\"sensorTypeAlternateId\\\": \\\"50\\\"}"

#        data_onlyTemp = "{\\\"capabilityAlternateId\\\": \\\"100-30\\\", \\\"measures\\\": [[\\\""+strTemp+"\\\"]],\\\"sensorTypeAlternateId\\\": \\\"30\\\",\\\"sensorAlternateId\\\": \\\"30100-30\\\"}"
#        data_onlyLight = "{\\\"capabilityAlternateId\\\": \\\"102-29\\\", \\\"measures\\\": [[\\\""+strLight+"\\\"]],\\\"sensorTypeAlternateId\\\": \\\"29\\\",\\\"sensorAlternateId\\\": \\\"29102-29\\\"}"

#        command = "curl -v -H 'Content-Type: application/json' --cert '"+certfile+"' -d \""+data+"\" "+postAddress
#        print ("command=%s" %command)
#        os.system(command)

# wait timeIntervall [s] before reading the sensor values again
#        time.sleep(timeIntervall)

#        command = "curl -v -H 'Content-Type: application/json' --cert '"+certfile+"' -d \""+data_onlyTemp+"\" "+postAddress
#        print ("command=%s" %command)
#        os.system(command)

#        command = "curl -v -H 'Content-Type: application/json' --cert '"+certfile+"' -d \""+data_onlyLight+"\" "+postAddress
#        print ("command=%s" %command)
#        os.system(command)

# wait timeIntervall [s] before reading the sensor values again
#        time.sleep(timeIntervall)
