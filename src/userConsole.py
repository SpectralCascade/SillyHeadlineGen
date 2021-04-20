#Refernce files:
# https://urllib3.readthedocs.io/en/latest/reference/urllib3.exceptions.html
# https://urllib3.readthedocs.io/en/latest/reference/urllib3.poolmanager.html#urllib3.PoolManager
# https://urllib3.readthedocs.io/en/latest/user-guide.html
# https://zetcode.com/python/urllib3/
# https://stackoverflow.com/questions/11971369/web2py-url-validator/11974942#11974942

import urllib3
import urllib3.request
import urllib3.exceptions

userInput = int(input("Hello, this is the parody headline checker!S \n To begin choose between:" \
                  "\n 1.Input a URL" \
                  "\n 2. Input a headline" \
                  "\n Choose 1 or 2 \n ")) 

if userInput == 1:
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
        print ("URL is good!")
        
elif userInput == 2:
    print("You've picked to input a headline")
    Headline = input("Please input in a headline:\n")
    
else:
    print("Choose either 1 or 2")
