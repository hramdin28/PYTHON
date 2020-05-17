"""
Home page, in [[updaterMain.py]]
"""
from clients import databases, clientsToRun
import cx_Oracle
import os
from params import scriptsLocation
# === Oracle scripts deploy script ===
"""
Script containing functions to deploy oracle scripts to databases
"""
# === Object to set a script priority ===	
deployPriority = {'create': [], 'alter': [], 'constraints':[], 'other': []}
# === Deploy ===	
def deploy():
	print ('')
	# Find and set scripts run priority
	populateScriptList()
	# Loop in all database clients
	for t in databases:	
		if (t['name'] in clientsToRun) or (len(clientsToRun) == 0):
			print ('Running script for: ' + t['name'])
			try:
				# deploy scripts
				deployScripts(t)
			except Exception as err:
				print(err)
	
# === Populate script in list ===	
# Use a custum list object to get an order of script execution
def populateScriptList():
	# loop in directorty to get all scripts
	for subdir, dirs, files in os.walk(scriptsLocation):
		for file in files:
			# Find create scripts
			if "create" in subdir.lower():
				deployPriority["create"].append(os.path.join(subdir, file))
			# Find alter scripts	
			elif "alter" in subdir.lower():
				deployPriority["alter"].append(os.path.join(subdir, file))
			# Find constraints scripts		
			elif "constraints" in subdir.lower():
				deployPriority["constraints"].append(os.path.join(subdir, file))
			# Find other scripts				
			else:
				deployPriority["other"].append(os.path.join(subdir, file))

# === Deploy scripts ===				
def deployScripts(db):	
	# loop in priority object to run scripts in correct order
	for key,val in deployPriority.items():
		print ('Deploying ' + key + ' scripts...')
		
		for scriptPath in val:
			with open(scriptPath, mode='r', newline='') as FILE:
				script ='begin ' + FILE.read() + ' end;';
				# connect to database
				dsn_tns = cx_Oracle.makedsn(db['host'], db['port'], db['sid'])
				with cx_Oracle.connect(user=db['username'], password=db['password'], dsn=dsn_tns) as connection:
					with connection.cursor() as cursor:
						try:
							# execute script
							cursor.execute(script);	
						except Exception as err:
							print(err)
		# compile invalid objects
		compileInvalidObjects(db)		
		print ('Scripts ' + key + ' deployed...')
		print ('')		

# === Compile invalid objects script ===	
def compileInvalidObjects(db):
	script = "begin dbms_utility.compile_schema(schema => 'EDGAR_FIN', compile_all => false); end;"
	dsn_tns = cx_Oracle.makedsn(db['host'], db['port'], db['sid'])
	with cx_Oracle.connect(user=db['username'], password=db['password'], dsn=dsn_tns) as connection:
		with connection.cursor() as cursor:
			# execute script
			cursor.execute(script);	
	
	
# === Compile All invalid objects script ===	
def compileAllClientsInvalidObjects():
	#Loop in all database clients
	for t in databases:	
		if (t['name'] in clientsToRun) or (len(clientsToRun) == 0):
			print ('Running script for: ' + t['name'])
			try:
				# deploy scripts
				compileInvalidObjects(t)
			except Exception as err:
				print(err)
	

			