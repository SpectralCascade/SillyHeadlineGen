import json
import xml.etree.ElementTree as ET 
import ml
import soupScraping as s
#Reference: https://docs.python.org/3/library/xml.etree.elementtree.html
#Accessed 21/04/2021 at 14:45



class mrOutput:
    #inputDict = {} <---- will be populated from elsewhere in the program
    #takes input from the main program and posts it in a JSON file as a dictionary
    def createJSON(inputDict):
        #open a new file and dump the dictionary to it
        with open('outputData.json', 'w') as outputFile:
            json.dump(inputDict, outputFile, indent=4)

    def createXML(completedict):
        title = ET.Element(completedict.get("output"))
        identifier1 = ET.SubElement(title, "inputHeadline") 
        identifier1.text = str(completedict.get("inputHeadline"))
        identifier2 = ET.SubElement(title, "predictionModel")
        identifier2.text = str(completedict.get("predictionModel"))
        identifier3 = ET.SubElement(title, "outcomeProbabilities") 
        identifier3.text = str(completedict.get("outcomeProbabilities"))
        identifier4 = ET.SubElement(title, "result")
        identifier4.text = str(completedict.get("result"))
        identifier5 = ET.SubElement(title, "scrapedExampleHeadlines")
        identifier5.text = str(completedict.get("scrapedExampleHeadlines"))
        identifierS = ET.SubElement(title, "schema")
        identifierS.text = str(completedict.get("schema"))

        finalTree = ET.ElementTree(title)
        with open('outputData.xml', 'w') as outputFile:
            finalTree.write(outputFile, encoding='unicode')
        

    if  __name__ == "__main__":
        #run the createJSON and createXML method
        headline = "swag gamers looking sus in the Mordor"
        results = ml.demo(headline)
        guardianResults = s.guardianScrape(2)
        mashResults = s.dailymashScrape(2)
        completedict= {
        "output" : "Output",
        "inputHeadline" : results.get("Input Headline"),
        "predictionModel" : results.get("Prediction Model"),
        "outcomeProbabilities" : results.get("Outcome Probabilities"),
		"result" : results.get("Result"),
		"scrapedExampleHeadlines" : {"Guardian" : guardianResults.get("headlines"), "DailyMash" : mashResults.get("headlines")},
		"schema" : guardianResults.get("schema") + mashResults.get("schema")
        }


        createXML(completedict)
        createJSON(completedict)
