"""
Home page, in [[updaterMain.py]]
"""
import configparser as cparser1
import configparser as cparser2
import sshFunctions
from fabric import Connection, Config
from invoke import Responder
from clients import tomcats, clientsToRun
from params import propertiesFile, remotePropertiesFile
# === Deploy missing properties script ===
"""
Script to missing deploy properties in application.properties to remote
"""
# create a dummy section as configParser library needs section to work
section='dummy'
# === Deploy ===	
def deployLocalPropertiesToRemote(tomcat):
	
	# Get properties files as string
	localPropertiesStr = readFileAsString(propertiesFile)
	RemotePropertiesStr = readRemotePropertiesFile(tomcat)
	
	# Get parser objects based on strings
	# reading local properties file
	parserLocal = readPropertiesFile(localPropertiesStr, cparser1)
	# reading remote properties file
	parserRemote = readPropertiesFile(RemotePropertiesStr, cparser2)
	# Comparing local with remote
	compareLocalPropertiesWithRemote(parserLocal,parserRemote, tomcat)
	
# === Compare local with remote ===		
def compareLocalPropertiesWithRemote(parserLocal,parserRemote,tomcat):
	con = sshFunctions.connectSSH(tomcat)
	# Loop through local properties file and add missing properties to remote
	for each_section in parserLocal.sections():
		for (each_key, each_val) in parserLocal.items(each_section):
			# Check if remote properties file does not contain key
			if not parserRemote.has_option(section, each_key):
				writePropertyToPropertiesFile(each_key, each_val, tomcat, con)
	con.close()

# === Read remote ===					
def readRemotePropertiesFile(tomcat):
	filePath = '{location}{remoteFile}'.format(location=tomcat['location'], remoteFile = remotePropertiesFile)
	con = sshFunctions.connectSSH(tomcat)
	#If client has another machine on which we need to connect to access files
	
	fileStr = sshFunctions.readRemoteFileAddingDummyForProperty(con, filePath, tomcat)
	con.close()
	return fileStr

# === Write local ===
def writePropertyFileToLocalFile():

	for t in tomcats:
		try:
			RemotePropertiesStr = readRemotePropertiesFile(t)
			print(RemotePropertiesStr)
			
			f = open(t['name']+"_.py", "w")
			f.write(RemotePropertiesStr)
			f.close()
			
		except Exception as err:
				print(err)
	
# === Write remote ===		
def writePropertyToPropertiesFile(key, value, tomcat, connection):
	if 'dataSourceFilePath' == key:
		value = tomcat['location'] + 'edgarbi/datasources.yaml'
	propertyToWrite = '{pKey}={pValue}'.format(pKey=key, pValue=value)
	filePath = '{location}{remoteFile}'.format(location=tomcat['location'], remoteFile = remotePropertiesFile)
	sshFunctions.writeToRemoteFile(connection, ' ', filePath, tomcat)
	sshFunctions.writeToRemoteFile(connection, propertyToWrite, filePath, tomcat)

# === Read local ===		
def readPropertiesFile(propertiesString, parser):
	result = parser.ConfigParser(strict=False)
	result.optionxform = str
	result.read_string(propertiesString)
	return result	

# === Read as string ===	
def readFileAsString(filePath):
	fileString = ''
	with open(filePath) as file:
		fileString = '['+ section +'] \n' + file.read()
	return fileString

# === Deploy All ===		
def deploy():
	print ('')
	# Loop in all tomcats
	for t in tomcats:
		if (t['name'] in clientsToRun) or (len(clientsToRun) == 0):
			print ('Adding properties for: ' + t['name'])
			try:
				# Deploy missing properties
				deployLocalPropertiesToRemote(t)
			except Exception as err:
				print(err)	
