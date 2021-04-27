import sys
from CV import CV
import urllib.request
import userConsole as uc
import ml
import mrOutput

if __name__ == '__main__':
    args = sys.argv[1:]		# extracting arguments from the command line
    options = {"-h", "--help", "-u", "--url", "-i", "--headline", "-f", "--filter", "-o", "--output"}
    last_option = ''
    was_option = False
    headlines = []
    output = ''
    filterTerms = []
    
    for i in range(len(args)):
        was_option = False
        # check if the argument is an option
        if args[i].lower() in options:
            last_option = args[i].lower()
            was_option = True
        # if last option is help
        if last_option == "-help" or last_option == "-h":
            print("\n\t Welcome to the Parody Headline/URL Checker!"
                  "\n"
                  "\n\t List of Options:"
                  "\n\t --help or -h"
                  "\n\t --url or -u"
                  "\n\t --headline or -i"
                  "\n\t --filter or -f"
                  "\n\t --output or -o"
                  "\n"
                  "\n\t You are expected to enter these options in the correct order followed"
                  "\n\t by the URLs or Headlines that you wish to test !"
                  "\n"
                  "\t Input arguments needed:\n"
                  "\n\t\t [--url/--headline] =  Input a URL to extract a headline from or input headline directly\n"
                  "\t\t [URL or TITLE) = Input the URLs and/or headlines enclosed in single '' or double \"\" quotes. \n"
                  "\t\t [--filter] = Specifies that you would like to filter your search.\n"
                  "\t\t [Filter(s)] = Input the terms you want the headline or URL to be filtered by. \n"
                  "\t\t [-output] = Specifies that you would like your output saved to a specific path.\n"
                  "\t\t [Path] = Enter the file path where you would like your output to be stored.\n"
                  "\n\t Example Input:\n"
                  "\n\t --headline 'David Jimson is a good bloke, apparently !' --filter Europe Person Sport\n"
                  "\t [cont.] --output C:\Program Files\example.json"
                  "\n\t The following terms are valid filters:")
            for k, v in CV.items():
                print('\t\t {key}: {values}'.format(key=k, values=', '.join('{}'.format(', '.join(x.split())) for x in v)))
            break
        if was_option:
            continue
        elif last_option == "--url" or last_option == "-u":
            url = args[i]
            import urllib.request
            with urllib.request.urlopen('http://python.org/') as response:
                html = response.read()
        elif last_option == "--headline" or last_option == "-i":
            headlines.append(args[i])
        elif last_option == "--filter" or last_option == "-f":
            CV_vals = CV.values()
            CV_single = []
            for sublist in CV_vals:
                for item in sublist:
                    CV_single.append(item)
            CV_single_lower = [x.lower() for x in CV_single]
            if args[i].lower() in CV_single_lower:
                filterTerms.append(args[i])
        elif last_option == "--output" or last_option == "-o":
            output = args[i]
    
    if not headlines:
        uc.run_guide()
    else:
        while not output:
            output = uc.GetOutputDir()
        results = ml.demo(headlines, filterTerms)
        for result in results:
            # Send to machine readable output
            mrOutput.exportchoice(output, result)
