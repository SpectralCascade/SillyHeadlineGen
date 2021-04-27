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

from CV import CV

import ml

def filterChoice(filterFile):
    noOfFilters = int(input('Do you want to filter ' + filterFile +' by 1 or multiple terms? Choose \n 1. 1 term' \
        '\n 2. Multiple terms \n'))
    
    if noOfFilters == 1:
        print("What term to you want to filter by? Here are the categories:")
        for k, v in CV.items():
            print('{key}: {values}'.format(key=k, values=', '.join('{}'.format(', '.join(x.split())) for x in v)))            
        filterTerm = input("What term do you want to filter by? \n")
        if(any(filterTerm in value for value in CV.values())):
            print('Filter by ' + filterTerm)
            # MACHINE LEARNING
        else:
            print("Please choose a category to filter by")
            
    elif noOfFilters == 2:
        print("What term to you want to filter by? Here are the categories:")
        for k, v in CV.items():
            print('{key}: {values}'.format(key=k, values=', '.join('{}'.format(', '.join(x.split())) for x in v)))            
        filterTerms = input("What terms do you want to filter by? (Split up the terms with a ', ' (comma)) \n")
        terms_list = re.split("[, ] ", filterTerms)
        print(terms_list)
        # MACHINE LEARNING
    else:
        print('Choose either options 1 or 2')
        
def HeadlineInput():
    print("You've picked to input a headline")
    Headline = input("Please input in a headline:\n")
    filterChoice(Headline)
    # Do machine learning
    ml.demo(Headline)

def URLInput():
    # NEEDS TO BE LOOKED AT
    print("You've picked to input a URL")
    URL = input("Please input in a URL:\n")
    http = urllib3.PoolManager()
    try:
        response = http.request('GET', URL)
    except urllib3.exceptions.HTTPError:
        if hasattr(e, 'reason'):
            print ('We failed to reach a server.')
            print ('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print ('The server couldn\'t fulfill the request.')
            print ('Error code: ', e.code)
    else:
        print ("URL is valid!")
        filterChoice(URL)

def URLInputInStyle():
    print("You've picked to input a URL")
    validURL = False
    while validURL == False:
        URL = "http://" + input("Please input in a URL:\n")
        try:
            r = requests.get(URL)
            if r.status_code == 200:
                validURL = True
                print('URL is valid!')
                filterChoice(URL)
            else:
                print('URL is not valid or the server couldn\'t fufill the request') 
        except requests.exceptions.ConnectionError:
            print('We failed to reach the server you supplied.')

def run_guide ():

    userInput = int(input("Hello, this is the parody headline checker!S \n To begin choose between:" \
                      "\n 1.Input a URL" \
                      "\n 2. Input a headline" \
                      "\n Choose 1 or 2 \n "))
    if userInput == 1:
        URLInputInStyle()

    elif userInput == 2:
        HeadlineInput()

    else:
        print("Choose either 1 or 2")
