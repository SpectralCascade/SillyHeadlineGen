import json

#takes input from the main program and posts it in a JSON file as a dictionary

class mrOutput:
	#inputDict = {} <---- will be populated from elsewhere in the program
	exampleDict = {
		"Title":"Lunch",
		"Tasty": "78%",
		"Fruity":"0%"
	}

	def createJSON(inputDict):
		#open a new file and dump the dictionary to it
		with open('outputData.json', 'w') as outputFile:
			json.dump(inputDict, outputFile, indent=4)

	if  __name__ == "__main__":
		#run the createJSON method
		createJSON(exampleDict)