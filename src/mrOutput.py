import json
import xml.etree.ElementTree as ET 
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
		title = ET.Element(inputDict.get("Title"))
		identifier1 = ET.SubElement(title, "Tasty : " + inputDict.get("Tasty"))
		break1 = ET.SubElement(title, "\n")
		identifier2 = ET.SubElement(title, "Fruity : " + inputDict.get("Fruity"))
		break2 = ET.SubElement(title, "\n")
		finalTree = ET.ElementTree(title)
		with open('outputData.xml', 'w') as outputFile:
			finalTree.write(outputFile, encoding='unicode')


	def createXMLInStyle(inputDict):
		for x in inputDict:
			title = ET.Element.get(inputDict.get())

	if  __name__ == "__main__":
		#run the createJSON and createXML method
		createJSON(exampleDict)
		createXML(exampleDict)