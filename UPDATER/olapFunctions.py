"""
Home page, in [[updaterMain.py]]
"""
"""
Script to deploy OLAP cubes and data sources to remote
"""
import os
from sshFunctions import connectSSH, runOnlyCommandOnRemote
from fabric import Connection
from clients import tomcats, databases, cubeRemoteRelativePath, dataSourceRemoteRelativePath, cubeLocalPath

# === Main function to update Olap cubes to remote destination ===	
def updateOlapComponents():
	
	# Loop in all tomcats
	for t in tomcats:
		# Connect to tomcat
		connection = connectSSH(t)
		pathOfTomcat = t['location']
		cubeCurrency = t['cubeCurrency']
		clientName = t['name']
		updateCubesOnRemote(connection, pathOfTomcat, cubeCurrency, clientName)
		
		
def updateCubesOnRemote(connec, tomcatPath, cubeCurrency, clientName):				

	moveExistingRemoteCubesForBackup(connec, tomcatPath)
	
	# Looping on local cubes to write them on remote client
	for filename in os.listdir(cubeLocalPath):
		if filename.find("Cube") != -1 and filename.endswith(".xml"): 
			
		# Cube Part
			cubeInString = replaceDefaultCurrencyInLocalCube(cubeLocalPath, filename, cubeCurrency)			
			remotePathOfCube = tomcatPath + cubeRemoteRelativePath
			writingDataOnRemote(remotePathOfCube, filename, cubeInString, connec)

		# Data source part			
			# Removing ".xml" extension to use as a file name for the data source file
			dataSourceFileName = filename[0:-4]
			dataSourceInString = replaceDefaultValuesInDataSource(tomcatPath, clientName, filename, dataSourceFileName)	
			remotePathOfDataSource = tomcatPath + dataSourceRemoteRelativePath
			writingDataOnRemote(remotePathOfDataSource, dataSourceFileName, dataSourceInString, connec)
			print("\nDataSource of {0} client file for cube name : {1} was updated.".format(clientName, filename))

			
# === Replacing default currency value in cube definition by proper client one ===
#
# All Cubes in their name have a default : "CUTP" to be replaced when place on remote clients
#
# ex.:  <Cube name="Sales Cube #CUTP#" visible="true" cache="true" enabled="true" defaultMeasure="Fare">
# The "#CUTP#" will be replaced by the proper client currency taken from "clients.py"		
#
def replaceDefaultCurrencyInLocalCube(cubeLocalPath, filename, cubeCurrency):
	fileInString = readFileAsString(os.path.join(cubeLocalPath, filename))
    
	print("\nCube name : {0} was updated.".format(filename))
	return fileInString.replace("#CUTP#", cubeCurrency)
	

# === Writing the remote cube to its destination ===		
#def writingCubeOnRemote(remotePathOfCube, cubeName, cubeAsString, connection):
#	
#	# example : echo -e 'text' > 'Users/Name/Desktop/TheAccount.txt'
#	# -e to keep the newlines
#	# single quotes to keep special characters in string
#	writingCommand = "echo -e '" + cubeAsString + "' > " + remotePathOfCube + cubeName
#	#print(writingCommand)
#	try:
#		runOnlyCommandOnRemote(connection, writingCommand)
#	except Exception as err:
#		print(err)		
#
		
# === Moving existing cubes from 'Cube' folder to 'Cube/CubesBackup' folder ===	
def moveExistingRemoteCubesForBackup(connection, pathOfTomcat):
	createBackupCubeFolderOnRemote(connection, pathOfTomcat)

	# -n moves only if file does not exist
	mvCommand = "mv -n " + pathOfTomcat + cubeRemoteRelativePath + "*Cube*.xml " + pathOfTomcat + cubeRemoteRelativePath + "CubesBackup"
	#print(mvCommand)
	runOnlyCommandOnRemote(connection, mvCommand)


# === Creating 'Cube/CubesBackup' folder ===	
def createBackupCubeFolderOnRemote(connection, pathOfTomcat):

	try:			
		# Only creating CubesBackup folder if folder does not exist
		mkDirCommand = 'mkdir -p ' + pathOfTomcat + cubeRemoteRelativePath + 'CubesBackup'
		#print(mkDirCommand)
		runOnlyCommandOnRemote(connection, mkDirCommand)

	except Exception as err:
		print(err)			
		
		
# === Creating data source file to be written on remote destination for each cube found ===		
def replaceDefaultValuesInDataSource(tomcatPath, clientToBeUpdated, cubeXmlFileName, dataSourceFileName):
	
	# Loop in all databases array to get the info from client database
	for db in databases:
		if db['name'] == clientToBeUpdated:
			print("\nFound database of client :" + db['name'])

			# "saiku-datasource-template.txt" is found locally under : C:\Adev\Misc\Fin\90-Tags\Fin_Release_1.90patch\XML
			fileInString = readFileAsString(os.path.join(cubeLocalPath, "saiku-datasource-template.txt"))
			
			fileInString = fileInString.replace("#CubeName#", "{0}".format(dataSourceFileName))
			
			# Connection to DB
			fileInString = fileInString.replace("#DbIP:Port:Sid#", "{0}:{1}:{2}".format(db['host'], db['port'], db['sid']))	
			
			# Path for link with cube  
			remotePathOfCube = tomcatPath + cubeRemoteRelativePath
			fileInString = fileInString.replace("#CubePathAndFileName#", "{0}{1}".format(remotePathOfCube, cubeXmlFileName))		
			
			fileInString = fileInString.replace("#DbUserName#", "{0}".format(db['username']))			
			fileInString = fileInString.replace("#DbPassword#", "{0}".format(db['password']))

			return fileInString
			
			
# === Writing string as file to the remote destination ===		
def writingDataOnRemote(remotePath, fileName, fileAsString, connection):
	
	# example : echo -e 'text' > 'Users/Name/Desktop/TheAccount.txt'
	# -e to keep the newlines
	# single quotes to keep special characters in string
	writingCommand = "echo -e '" + fileAsString + "' > " + remotePath + fileName
	#print(writingCommand)
	try:
		runOnlyCommandOnRemote(connection, writingCommand)
	except Exception as err:
		print(err)	
		
		
# === Read as string ===	
def readFileAsString(filePath):
	fileString = ''
	with open(filePath) as file:
		fileString = file.read()
	return fileString		