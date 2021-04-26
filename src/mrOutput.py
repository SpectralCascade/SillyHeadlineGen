import json
import xml.etree.ElementTree as ET 
import ml
#Reference: https://docs.python.org/3/library/xml.etree.elementtree.html
#Accessed 21/04/2021 at 14:45



class mrOutput:
	#inputDict = {} <---- will be populated from elsewhere in the program
	exampleDict = {
		"Title":"Lunch",
		"Tasty": "78%",
		"Fruity":"0%"
	}
	#takes input from the main program and posts it in a JSON file as a dictionary
	def createJSON(inputDict):
		#open a new file and dump the dictionary to it
		with open('outputData.json', 'w') as outputFile:
			json.dump(inputDict, outputFile, indent=4)

	def createXML(inputDict):
		title = ET.Element(inputDict.get("Output from Execution"))
		identifier1 = ET.SubElement(title, "Input Headline") 
		identifier1.text = str(inputDict.get("Input Headline"))
		identifier2 = ET.SubElement(title, "Prediction Model")
		identifier2.text = str(inputDict.get("Prediction Model"))
		identifier3 = ET.SubElement(title, "Outcome Probabilities") 
		identifier3.text = str(inputDict.get("Outcome Probabilities"))
		identifier4 = ET.SubElement(title, "Result")
		identifier4.text = str(inputDict.get("Result"))
		finalTree = ET.ElementTree(title)
		with open('outputData.xml', 'w') as outputFile:
			finalTree.write(outputFile, encoding='unicode')


	def createXMLInStyle(inputDict):
		for x in inputDict:
			title = ET.Element.get(inputDict.get())
		

	if  __name__ == "__main__":
		#run the createJSON and createXML method
		results = ml.demo("poo")

		createXML(results)
		createJSON(results)
