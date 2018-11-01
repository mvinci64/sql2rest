# sql2rest
Python script reading from MS SQL Server and writing to SAP CP IOT Service via REST API
####################################################################################################
#'''
# Created on 28.10.2018 initially
# This program reads from MS SQL Server of 2i Rete Gas and send sensor data 
# and pushes the data into the SAP Cloud Platform IoT Services for cloud foundry
#
# It needs to be run with the 2iRG VPN connection up and running 
# @author: Marcello Vinci, SAP EMEA SOUTH PDM COE 
# Rel 1.0 - very little use of config.json file
# Rel 1.1 - github 'parametrization'
# - how to generate device certificate with proper API calls
# - add NomeSistema on the config.json file and then retrieve all the PDMs and for each PDM retrieve all the measures 
# - add CODPuntoMisura as the main parameter to retrieve the measures - in the absense of NomeSistema single sql call
# - add the database information on the config.json file
# - check the last read file - why this is not a json file? Ask Stefano
# - 202 is the new code and therefore this is normally Accepted
####################################################################################################
