#Refernce files:
# https://urllib3.readthedocs.io/en/latest/reference/urllib3.exceptions.html
# https://urllib3.readthedocs.io/en/latest/reference/urllib3.poolmanager.html#urllib3.PoolManager
# https://urllib3.readthedocs.io/en/latest/user-guide.html
# https://zetcode.com/python/urllib3/
# https://stackoverflow.com/questions/11971369/web2py-url-validator/11974942#11974942

import urllib3
import urllib3.request
import urllib3.exceptions
import re
import requests
import mrOutput

from CV import CV

import ml

filterTerms = []

def filterChoice(filterFile):
    filterTerms = []
    noOfFilters = int(input('Do you want to filter ' + filterFile +' by 1 or multiple terms? Choose \n 1. 1 term' \
        '\n 2. Multiple terms \n'))
    if noOfFilters == 1:
        print("What term to you want to filter by? Here are the categories:")
        for k, v in CV.items():
            print('{key}: {values}'.format(key=k, values=', '.join('{}'.format(', '.join(x.split())) for x in v)))            
        filterTerm = input("What term do you want to filter by? \n")
        if(any(filterTerm in value for value in CV.values())):
            print('Filter by ' + filterTerm)
        else:
            print("Please choose a category to filter by")
    elif noOfFilters == 2:
        print("What term to you want to filter by? Here are the categories:")
        for k, v in CV.items():
            print('{key}: {values}'.format(key=k, values=', '.join('{}'.format(', '.join(x.split())) for x in v)))            
        filterTerms = input("What terms do you want to filter by? (Split up the terms with a ', ' (comma)) \n")
        terms_list = re.split("[, ] ", filterTerms)
        #print(terms_list)
    else:
        print('Choose either options 1 or 2')

def HeadlineInput():
    print("You've picked to input a headline")
    return input("Please input in a headline:\n")

def GetOutputDir():
    return input("Please specify an output file path:\n")

def URLInputInStyle():
    validURL = False
    while validURL == False:
        URL = input("Please input in a valid URL:\n")
        if "http://" not in URL and "https://" not in URL:
            URL = "http://" + URL
        try:
            r = requests.get(URL)
            if r.status_code == 200:
                validURL = True
                print('URL is valid!')
                return True
            else:
                print("URL is not valid or the server couldn't fulfill the request.")
        except requests.exceptions.ConnectionError:
            print('Failed to reach the server.')

def run_guide():
    userInput = int(input("Hello, this is the parody headline checker!\nTo begin choose between:" \
                      "\n 1. Input a URL" \
                      "\n 2. Input a headline" \
                      "\n Choose (1) or (2):\n"))
    
    headline = ""
    if userInput == 1:
        headline = URLInputInStyle()
    elif userInput == 2:
        headline = HeadlineInput()
    else:
        print("Invalid option.")
        run_guide()
    
    if (headline):
        filterChoice(headline)
        output = GetOutputDir()
        results = ml.demo([headline], filterTerms)
        for result in results:
            # Send to machine readable output
            mrOutput.exportchoice(output, result)

