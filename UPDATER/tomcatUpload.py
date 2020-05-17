"""
Home page, in [[updaterMain.py]]
"""
from clients import tomcats, clientsToRun
from params import warPath, warFileName, deployedPath, timeToWait
import sshFunctions
import tomcatmanager as tm
import requests
from patchwork.files import exists
import time
# === Tomcat functions script ===
"""
Script containing functions to interact with tomcats 
"""

# === Connection ===
def connectTomcat(url, username, password):
	print ("Connecting to tomcat...")
	tomcatManager = tm.TomcatManager()
	conn = tomcatManager.connect(url= url, user= username, password= password)
	tomcatObj = {'manager': tomcatManager, 'connection': conn}
	return tomcatObj
	
# === Deploy ===	
def deploy():
	print ('')
	# Loop in all tomcats
	for t in tomcats:
		if (t['name'] in clientsToRun) or (len(clientsToRun) == 0):
			print ('Deploying on Tomcat ' + t['name'])
			try:
				# Connect to tomcat
				tomcatObj = connectTomcat(t['managerUrl'], t['managerUser'], t['managerPwd'])
				tomcatObj['connection'].raise_for_status()
				# Deploy to tomcat
				deployWar(tomcatObj, t)
			except Exception as err:
				print(err)
			
# === Monitor Tomcat ===
def monitorTomcatStatus():	
	print ('')
	print ("Monitoring tomcats status...")
	# Loop in all tomcats
	for t in tomcats:
		if (t['name'] in clientsToRun) or (len(clientsToRun) == 0):
			try:	
				print ('Checking Tomcat ' + t['name'])
				# Connect to tomcat
				tomcatObj = connectTomcat(t['managerUrl'], t['managerUser'], t['managerPwd'])
				# Get Tomcat status
				getTomcatStatusCode(tomcatObj)
				print ('')
			except Exception as err:
				print(err)	

# === Reload all apps ===
def reloadAllApps():	
	print ('')
	print ("Reloading tomcats apps...")
	# Loop in all tomcats
	for t in tomcats:
		if (t['name'] in clientsToRun) or (len(clientsToRun) == 0):
			print ('Reloading Tomcat ' + t['name'])
			try:
				# Connect to tomcat
				tomcatObj = connectTomcat(t['managerUrl'], t['managerUser'], t['managerPwd'])
				# Reload Application
				reloadApplication(tomcatObj)
				print ('')	
			except Exception as err:
				print(err)

# === Deploy war ===	
def deployWar(tomcatObj, tomcat):	
	remotePath = '/tmp/'
	fileToUpload = warPath + warFileName
	con = sshFunctions.connectSSH(tomcat)
	
	# Check if war is already pushed
	if not exists(con, remotePath + warFileName):	
		print ("Uploading war...")
		# Upload file
		sshFunctions.uploadFile(con, fileToUpload, remotePath)
		print ('Upload finished ...')
	
	print ("Deploying war...")
	# Deploy war
	tomcatObj['manager'].deploy_serverwar(warfile= remotePath + warFileName, path= deployedPath, update = True)
	print ('Deploy finished ...')

# === Undeploy Tomcat ===	
def unDeployWar(tomcatObj):
	print ("Undeploying war...")
	# Undeploy app
	t= tomcatObj['manager'].undeploy(path= deployedPath)
	print (t.status_message)

# === Reload App ===	
def reloadApplication(tomcatObj):
	print ("Reloading App...")
	# Reload app
	t= tomcatObj['manager'].reload(path= deployedPath)
	print (t.status_message)

# === Stop App ===	
def stopApplication(tomcatObj):
	print ("Stopping App...")
	# Reload app
	t= tomcatObj['manager'].stop(path= deployedPath)
	print (t.status_message)

# === Stop App ===	
def startApplication(tomcatObj):
	print ("Start App...")
	# Reload app
	t= tomcatObj['manager'].start(path= deployedPath)
	print (t.status_message)

# === Undeploy App ===	
def undeployApplication(tomcatObj):
	print ("Undeploy App...")
	# Reload app
	t= tomcatObj['manager'].undeploy(path= deployedPath)
	print (t.status_message)		

# === Tomcat status ===
def getTomcatStatusCode(tomcatObj):
	print (tomcatObj['connection'].status_code)
	
# === Undeploy Application on All Tomcats ===
def undeployAppOnTomcats():
	for t in tomcats:
		if (t['name'] in clientsToRun) or (len(clientsToRun) == 0):
			print ('Undeploying app: ' + t['name'])
			try:
				# Connect to tomcat
				tomcatObj = connectTomcat(t['managerUrl'], t['managerUser'], t['managerPwd'])
				# Undeploy Application
				undeployApplication(tomcatObj)
			except Exception as err:
				print(err)	

# === Stop Application on All Tomcats ===
def stopAppOnTomcats():
	for t in tomcats:
		if (t['name'] in clientsToRun) or (len(clientsToRun) == 0):
			print ('Stopping app: ' + t['name'])
			try:
				# Connect to tomcat
				tomcatObj = connectTomcat(t['managerUrl'], t['managerUser'], t['managerPwd'])
				# Stop Application
				stopApplication(tomcatObj)
			except Exception as err:
				print(err)

# === Start Application on All Tomcats ===
def startAppOnTomcats():
	for t in tomcats:
		if (t['name'] in clientsToRun) or (len(clientsToRun) == 0):
			print ('Starting app: ' + t['name'])
			try:
				# Connect to tomcat
				tomcatObj = connectTomcat(t['managerUrl'], t['managerUser'], t['managerPwd'])
				# Start Application
				startApplication(tomcatObj)
			except Exception as err:
				print(err)


# === Restart all Tomcat ===	
def restartTomcats():	
	# Loop in all tomcats
	for t in tomcats:
		if (t['name'] in clientsToRun) or (len(clientsToRun) == 0):
			print ('Restarting tomcat: ' + t['name'])
			try:
				# Kill Tomcat
				killCommand = "kill -9 $(ps ax |grep '" + t['location'] + "' | grep -v grep | awk {'print $1'})"
				sshFunctions.runCommandOnRemote(killCommand, t)
				# Start Tomcat
				startCommand = 'export JAVA_HOME=/usr/java/latest\n'
				startCommand += 'export PATHSAV=$PATH\n'
				startCommand += 'export PATH=$JAVA_HOME/bin:$PATHSAV\n'
				startCommand += 'set -m; {tomcatLocation}bin/startup.sh'.format(tomcatLocation = t['location'])
				# Run command
				sshFunctions.runCommandOnRemote(startCommand, t)
				time.sleep(timeToWait)
			except Exception as err:
				print(err)

# === Add required role to tomcat ===	
def addRoleToTomcats():
	# Loop in all tomcats
	for t in tomcats:
		if (t['name'] in clientsToRun) or (len(clientsToRun) == 0):
			print ('Adding role for: ' + t['name'])
			try:
				confFile = t['location'] + 'conf/tomcat-users.xml'
				command = "sed -i 's/admin,admin-gui,manager-gui/admin,admin-gui,manager-script,manager-gui/g' " + confFile + '\n'
				# Run command
				sshFunctions.runCommandOnRemote(command, t)
			except Exception as err:
				print(err)

		