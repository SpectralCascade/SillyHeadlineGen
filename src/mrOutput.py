import json
import xml.etree.ElementTree as ET 
import ml
import soupScraping as s
#Reference: https://docs.python.org/3/library/xml.etree.elementtree.html
#Accessed 21/04/2021 at 14:45
filecount = 0
#inputDict = {} <---- will be populated from elsewhere in the program
#takes input from the main program and posts it in a JSON file as a dictionary
def createJSON(directory, inputDict):
    global filecount
    #open a new file and dump the dictionary to it
    with open(directory + '/outputData' + str(filecount) + '.json', 'w') as outputFile:
        json.dump(inputDict, outputFile, indent=4)

def createXML(directory, completedict, schemaString):
    global filecount
    title = ET.Element(completedict.get("output"))
    identifier1 = ET.SubElement(title, "inputHeadline") 
    identifier1.text = str(completedict.get("inputHeadline"))
    #space1 = ET.SubElement(title, "\n")
    identifier2 = ET.SubElement(title, "predictionModel")
    identifier2.text = str(completedict.get("predictionModel"))
    #space2 = ET.SubElement(title, "\n")
    identifier3 = ET.SubElement(title, "outcomeProbabilities") 
    identifier3.text = str(completedict.get("outcomeProbabilities"))
    #space3 = ET.SubElement(title, "\n")
    identifier4 = ET.SubElement(title, "result")
    identifier4.text = str(completedict.get("result"))
    #space4 = ET.SubElement(title, "\n")
    identifier5 = ET.SubElement(title, "scrapedExampleHeadlines")
    identifier5.text = str(completedict.get("scrapedExampleHeadlines"))
    #space5 = ET.SubElement(title, "\n")

    identifierS = ET.SubElement(title, "schema")
    identifierS.text = str(completedict.get("schema"))

    finalTree = ET.ElementTree(title)
    xmlOutputString = ET.tostring(title, encoding ='utf-8', method ='xml')
    xmlOutputString = '<?xml version="1.0"?>' +"<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' xmlns:article='https://schema.org/NewsArticle'" + str(xmlOutputString) + schemaString + "</rdf:RDF>"
    with open(directory + '/outputData' + str(filecount) + '.xml', 'w') as outputFile: 
        outputFile.write(xmlOutputString)

def exportchoice(directory, results):
    global filecount
    completedictJSON = {
    "output" : "Output",
    "inputHeadline" : results.get("Input Headline"),
    "predictionModel" : results.get("Prediction Model"),
    "outcomeProbabilities" : results.get("Outcome Probabilities"),
	"result" : results.get("Result"),
	"schema" : results.get("Training Set")
    }

    totalSchemaString = ""

    
    for schema in results.get("Training Set"):
    	url = schema.get("aboutKey")
    	headline = schema.get("headline")
    	author = schema.get("author")
    	datePublished = schema.get("datePublished")
    	description = schema.get("description")
    	publisherDict = schema.get("publisher")
    	publisher = publisherDict.get("name")

    	schemaString = "<rdf:Description rdf:about=" + url +"><article:headline>" + headline + "</article:headline><article:author>" + author + "</article:author>" + "<article:datePublished>" + datePublished + "</article:datePublished><article:description>" + description + "</article:description>" + "<article:publisher>" + publisher + "</article:publisher></rdf:Description>"

    	totalSchemaString = totalSchemaString + schemaString


    completedictXML = {
    "output" : "Output",
    "inputHeadline" : results.get("Input Headline"),
    "predictionModel" : results.get("Prediction Model"),
    "outcomeProbabilities" : results.get("Outcome Probabilities"),
	"result" : results.get("Result")
	}


    filecount += 1
    createXML(directory, completedictXML, totalSchemaString)
    createJSON(directory, completedictJSON)
