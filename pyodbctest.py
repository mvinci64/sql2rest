####################################################################################################
#'''
# Created on 28.10.2018 initially
# This program reads from MS SQL Server of 2i Rete Gas and send sensor data 
# and pushes the data into the SAP Cloud Platform IoT Services for cloud foundry
#
# It needs to be run with the 2iRG VPN connection up and running 
# @author: Marcello Vinci, SAP EMEA SOUTH PDM COE 
#'''
####################################################################################################


# new for odbc connection
import pyodbc 

connection = pyodbc.connect("DSN=SQLServer;uid=USR_SAP;pwd=USR_SAP", autocommit=True) 

if connection :
	print("YES we are connected! \n")
	
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
	,[MAX2]
	,[MED2]
	,[MIN2]
	,[SQM2]
	FROM dbo.V_2I_SAP_2018  WHERE Cod_PuntoMisura = '00000P078028000502' AND DataSms > '2018-10-20T00:00:00.000' ORDER BY DataSms

'''

cursor = connection.execute(sql)

for c in cursor:
	print("CODPuntoMisura:",c[1],"DataSMS:",c[0],"NomeAttributo:",c[4])
	
