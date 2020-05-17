from clients import tomcats as tomcats
from clients import clientsToRun
from newClients import tomcats as tomcatsNew
import sshFunctions

newFileDirectory = 'edgarbi/'
filesToTransfer = ['Logo', 'Saiku', 'application.properties', 'datasources.yaml']	

def generateMigrateCopyCommand(old, new, file):
	command = 'scp -r -o StrictHostKeyChecking=no {tomcatLocation}edgarbi/{relativeFilePath} {sshNewUser}@{sshNewHost}:{tomcatNewLocation}{newLocation}'.format(
	tomcatLocation=old['location'], 
	relativeFilePath=file, 
	sshNewUser=new['sshUser'], 
	sshNewHost=new['sshUrl'], 
	tomcatNewLocation=new['location'], 
	newLocation=newFileDirectory
	)
	return command
	
def migrateFolders():
	for t in tomcatsNew:
		print ('Migrating ' + t['name'] + '...')
		try:
			newTomcat = t
			for oldTomcat in filter(lambda x : x['name'] == newTomcat['name'], tomcats):
				for file in filesToTransfer:
					command = generateMigrateCopyCommand(oldTomcat, newTomcat, file)
					sshFunctions.runMigrateCommandOnRemote(command, oldTomcat, newTomcat);
		except Exception as err:
				print(err)
		print('')

def replaceStringInFiles():
	for t in tomcatsNew:
		print ('Migrating ' + t['name'] + '...')
		try:
			newTomcat = t
			for oldTomcat in filter(lambda x : x['name'] == newTomcat['name'], tomcats):
				command1 = 'sed -i "s|spring.profiles.active=test|spring.profiles.active=prod|g" {path}edgarbi/application.properties*'.format(path=newTomcat['location'])
				sshFunctions.runCommandOnRemote(command1, newTomcat)
				
		
		except Exception as err:
				print(err)

def main():	
	migrateFolders()

	
if __name__ == '__main__':
	main()	