import sys
import tomcatUpload
import oracleScripts
import propertyReader
import olapFunctions
import requests as r
print('')
print("SSL certificate location: " + r.certs.where())
print('')
# === Python Updater App ===
"""
Python menu to run updater functions.
Script uses different python scripts for different tasks:

1. Tomcat tasks, defined in [[tomcatUpload.py]]
2. Oracle sql script tasks, defined in [[oracleScripts.py]]
3. SSH tasks, defined in [[sshFunctions.py]]
4. Properties file tasks, in [[propertyReader.py]]

"""
def menu():
	print("************MAIN MENU**************")
	print()

	choice = input("""
	0: Quit
	1: Monitor tomcats
	2: Deploy war to tomcats
	3: Deploy to and monitor tomcats
	4: Deploy Scripts
	5: Deploy Properties file
	6: Reload All Applications
	7: Deploy All
	8: Add Roles to tomcat
	9: Restart tomcats
	10: Compile invalid objects
	11: Stop Application
	12: Start Application
	13: Undeploy Application
	14: Get remote properties 
	15: Update Cube found under C:\Adev\Misc\Fin\90-Tags\Fin_Release_1.90patch\XML to remote location
	
	Please enter your choice: """)

	if choice == "0":
		sys.exit
	elif choice == "1":
		tomcatUpload.monitorTomcatStatus()
		
	elif choice == "2":
		tomcatUpload.deploy()
		
	elif choice=="3":
		tomcatUpload.deploy()
		tomcatUpload.monitorTomcatStatus()
		
	elif choice=="4":
		oracleScripts.deploy()
		
	elif choice=="5":
		propertyReader.deploy()

	elif choice=="6":
		tomcatUpload.reloadAllApps()
		
	elif choice=="7":
		propertyReader.deploy()
		oracleScripts.deploy()
		tomcatUpload.deploy()
		tomcatUpload.monitorTomcatStatus()

	elif choice=="8":
		tomcatUpload.addRoleToTomcats()	
	
	elif choice=="9":
		tomcatUpload.restartTomcats()	

	elif choice=="10":
		oracleScripts.compileAllClientsInvalidObjects()	

	elif choice=="11":
		tomcatUpload.stopAppOnTomcats()	

	elif choice=="12":
		tomcatUpload.startAppOnTomcats()

	elif choice=="13":
		tomcatUpload.undeployAppOnTomcats()
		
	elif choice=="14":
		propertyReader.writePropertyFileToLocalFile()		
	
	elif choice=="15":
		olapFunctions.updateCubesOnRemote()	
		
	else:
		print ('')
		print("You must only select either 0,1,2,3,4,5,6,7,8,9,10,11,13.")
		print("Please try again")
		menu()
	

def main():	
	menu()
	
if __name__ == '__main__':
    main()		