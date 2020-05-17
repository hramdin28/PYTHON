import os

# === Doc Generator Script ===
"""
Run this script to generate python docs
"""

def main():	
	for subdir, dirs, files in os.walk('./'):
		for file in files:
			if file.endswith('.py') | file.endswith('.sql'):
				command = 'pycco ' + file
				os.system(command)
				
	
	
if __name__ == '__main__':
    main()	
	
	