import sys

from CV import CV

# TEST INPUTS:
# commandLine.py hello url www.hello.com Sport, Person
# commandLine.py hello headline poop person 'yolo' poo

def URLChecker(args):
    # check website is valid
    ref_list = ['www.','https']
    URLInput = [s for s in stringArgs if any(xs in s for xs in ref_list)]
    
    #Verfiy status of website (see userConsole.py)
    
    # removes URL from input args
    for element in URLInput:
        if element in args:
            args.remove(element)

    #removes special chars from args
    removetable = str.maketrans('', '', '@#%,')
    args = [s.translate(removetable) for s in args]
    
    # checks if args contains filter categories
    CV_vals = CV.values()
    CV_single = []
    for sublist in CV_vals:
        for item in sublist:
            CV_single.append(item)
    CV_single_lower = [x.lower() for x in CV_single]
    # filterTerms is a list of terms the user wants to filter by
    filterTerms = list(set(CV_single_lower).intersection(args))

    # pass on these variables to machine learning
    print("URL: %s" % str(URLInput))
    print("Filter Terms: %s" % str(filterTerms))
    
def HeadlineChecker(InputStr):
    #retrieve headline title from input
    HeadlineTitle = InputStr.split("'")[1::2]

    # remove headline from args
    HeadlineString = " ".join(str(x) for x in HeadlineTitle)
    InputStr = InputStr.split(HeadlineString)
    InputStr = " ".join(InputStr).split()
    
    # extract filter terms from input
    CV_vals = CV.values()
    CV_single = []
    for sublist in CV_vals:
        for item in sublist:
            CV_single.append(item)
    CV_single_lower = [x.lower() for x in CV_single]
    filterTerms = list(set(CV_single_lower).intersection(InputStr))

    # pass on these variables to machine learning
    print("Headline Title: %s" % str(HeadlineTitle))
    print("Filter Categories: %s" % str(filterTerms))
    
def main():
    args = sys.argv[1:]
    args = [each_string.lower() for each_string in args]
    if "url" in args:
        # user has picked to check a URL
        args.remove("url")
        URLChecker(args)
        
    elif "headline" in args:
        # user has picked a headline
        args.remove("headline")
        inputString = ' '.join(args)
        HeadlineChecker(inputString)

        
if __name__ == '__main__':
    stringArgs = sys.argv
    if "--help" in stringArgs or len(stringArgs) == 1:
        print("\n\t Welcome to the Parody Headline/URL Checker!  \n\n" \
              "\t Example Input: URL www.google.com/john-smith person sport or Headline 'who is Mr Smith' person sport \n\n" \
              "\t Input arguments needed:\n" \
              "\t\t [URL/HEADLINE] =  Input whether you are checking a URL or a Headline \n" \
              "\t\t ['Title' or 'URL') = Input the Headline or the URL \n" \
              "\t\t [Filter(s)] = Input the terms you want the headline or URL to be filtered by. \n\n" \
              "\t Choose to filter from these Terms:" )
        for k, v in CV.items():
            print('\t\t {key}: {values}'.format(key=k, values=', '.join('{}'.format(', '.join(x.split())) for x in v)))
    else:
        main()
        
