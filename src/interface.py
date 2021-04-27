import sys
from CV import CV

if __name__ == '__main__':

	args = sys.argv[1:]		# extracting arguments from the command line
	count = 0;
	print()
	options = {"-h", "-help", "-u", "-url", "-h", "-headline", "-f", "-filter", "-o", "-output"}


	while (True):

		# if there are no more arguments
		if count >= len(args):
			print()
			print("****The list of arguments is finished !****")
			break

		# if arguments still exist	
		else:

			print (args[count])
			count = count + 1


