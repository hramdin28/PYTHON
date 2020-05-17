# === All tomcats configs ===  
tomcats = [
	{'name': 'XX', 'managerUrl':'https://192.168.33.11:8080/manager', 'managerUser': 'admin-xx', 'managerPwd': 'pwd', 'location': '/home/tomcat-xx/apache-tomcat-8.5.11/', 'sshUrl': '192.168.33.11', 'sshUser': 'tomcat-xx', 'sshPass': 'pwd123', 'isBPO': 'true', 'hasGatewayServer': 'false', 'cubeCurrency': 'ALL'}
]


# === All databases configs ===  
databases = [
	{'name': 'XX', 'host': '192.168.80.11','port':'1521','username': 'USER', 'password': 'PWD', 'sid':'XX'}
]

cubeRemoteRelativePath = 'user/Saiku/Cube/'

cubeLocalPath = 'C:/XML/'

# === Which clients to run ===  
# An array used to select which clients to run.
# If array is empty, all clients will be run
clientsToRun = ['XX']



