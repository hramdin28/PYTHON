"""
Home page, in [[updaterMain.py]]
"""
from fabric import Connection, Config, exceptions
from invoke import Responder
from params import sshKey ,passphrase
# === SSH functions script ===
"""
SSH functions:

1. Connection 
2. Read remote file
3. Write to remote file
4. Write command on remote
5. Upload File on remote
6. Get sudo password

"""

# === Connection ===
def connectSSH(tomcat):
	t = tomcat
	# Connect to tomcat
	if(t['hasGatewayServer'] is 'true'):
		if(t['gatewaySShPass'] is 'key'):

			con = Connection(t['internalSShUrl'], port=22, user=t['internalSShUser'], connect_kwargs={"key_filename": [sshKey], 'passphrase': passphrase}
							,gateway=Connection(t['gatewaySShUrl'], port=22, user=t['gatewaySShUser'], connect_kwargs={"key_filename": [sshKey], 'passphrase': passphrase})
							)
		else:
			con = Connection(t['internalSShUrl'], port=22, user=t['internalSShUser'], connect_kwargs={'password': t['internalSShPass']},
							gateway=Connection(t['gatewaySShUrl'], port=22, user=t['gatewaySShUser'], connect_kwargs={'password': t['gatewaySShPass']}))	
	else:
		con = Connection(t['sshUrl'], port=22, user=t['sshUser'], connect_kwargs={'password': t['sshPass'], "key_filename": [sshKey], 'passphrase': passphrase})
	return con

# === Read and adding "[dummy]" for properties purpose ===	
def readRemoteFileAddingDummyForProperty(connection, filePath, tomcat):	
	# Read using tail command
	result = connection.run('tail -10000 ' + filePath , hide=True, pty=True, watchers=[getSudoPassword(tomcat)])
	msg = "\n{0.stdout}"
	fileStr = '[dummy] \n' + msg.format(result)
	return fileStr
	
# === Read ===	
def readRemoteFile(connection, filePath, tomcat):	
	# Read using tail command
	result = connection.run('tail -10000 ' + filePath , hide=True, pty=True, watchers=[getSudoPassword(tomcat)])
	msg = "{0.stdout}"
	fileStr = msg.format(result)
	return fileStr	

# === Write ===
def writeToRemoteFile(connection, string, filePath, tomcat):
	# Write using echo and sudo tee -a command
	command = "echo '{fString}' >> {path}".format(fString=string, path = filePath)
	commandSudo = "echo '{fString}' | sudo tee -a {path}".format(fString=string, path = filePath)
	try: 
		connection.run(command, pty=True, watchers=[getSudoPassword(tomcat)])
	except Exception as err:
		connection.run(commandSudo, pty=True, watchers=[getSudoPassword(tomcat)])		

# === Run ===	
def runCommandOnRemote(command, tomcat):
	try:	
		# Connect to tomcat
		connection = connectSSH(tomcat)
		# Run command
		connection.run(command, pty=True, watchers=[getSudoPassword(tomcat)])	
	except Exception as e:
		print (e)

# === Run ===	
def runOnlyCommandOnRemote(connection, command):
	try:	
		# Run command
		connection.run(command)	
	except Exception as e:
		print (e)		
		
# === Upload ===	
def uploadFile(connection, fileToUpload, remotePath):
	# Upload file
	connection.put(fileToUpload, remote = remotePath)	
	
# === Sudo password ===	
def getSudoPassword(tomcat):
	# Add watcher for sudo password
	pwd = "{password}\n".format(password = tomcat['sshPass'])
	sudopass = Responder(pattern=r'\[sudo\] password for .*:',response= pwd)
	return sudopass	

	

# === Migrate ===	
def runMigrateCommandOnRemote(command, oldTomcat, newTomcat):
	try:	
		pwd = "{password}\n".format(password = newTomcat['sshPass'])
		patternMigrate = r"{user}@{host}'s password:".format(user=newTomcat['sshUser'], host=newTomcat['sshUrl'])
		sudopass = Responder(pattern=patternMigrate,response= pwd)
		# Connect to tomcat
		connection = connectSSH(oldTomcat)
		# Run command
		connection.run(command, pty=True, watchers=[sudopass])	
	except Exception as e:
		print (e)

	