userInput = int(input("Hello, this is the parody headline checker!S \n To begin choose between:" \
                  "\n 1.Input a URL" \
                  "\n 2. Input a headline" \
                  "\n Choose 1 or 2 \n ")) 

if userInput == 1:
    print("You've picked to input a URL")
elif userInput == 2:
    print("You've picked to input a headline")
else:
    print("Choose either 1 2 or 3")

