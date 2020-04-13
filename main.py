############################################################
####                 The main function                 #####
############################################################

import argparse
from distutils.util import strtobool

from scripts.single_mode import copy_single_mode, delete_single_mode
from scripts.all_mode import copy_all_mode, delete_all_mode

def main():

    ## Get arguments
    parser = argparse.ArgumentParser(usage="sudo -u postgres python main.py -m delete-all -p \"playlist-name\"")

    parser.add_argument("-m", '--mode', 	default='copy-single', nargs='?', 
											choices=['copy-single', 'copy-all', 'delete-single', 'delete-all'],
											required=True,
											help='Copy/Delete the playlist to/of a single user or to all users (default: %(default)s)')
    parser.add_argument("-p", "--playlist", help="Name of the playlist", action="store")
    parser.add_argument("-u", "--user", 	help="Username", action="store")    
    args = parser.parse_args()

    ## Copy single mode
    if(args.mode == 'copy-single' and args.user != None and args.playlist != None):
        answer = raw_input("Are you sure to COPY the playlist '" + args.playlist + "' from admin to user '" + args.user +"'? [Y|N]: ")
        if(strtobool(answer)):
            print("Execute copy single mode:")
            copy_single_mode(args)
        else: exit(-1)

    ## Delete single mode
    elif(args.mode == 'delete-single' and args.playlist != None and args.user != None):
        answer = raw_input("Are you sure to DELETE the playlist '" + args.playlist + "' from user '" + args.user +"'? [Y|N]: ")
        if(strtobool(answer)):
            print("Execute delete single mode:")
            delete_single_mode(args)
        else: exit(-1)

    ## Copy all mode
    elif(args.mode == 'copy-all' and args.playlist != None):
        if(args.user != None):
            print("Your argument for the user will be ignored, it is not necessary here")
        answer = raw_input("Are you sure to COPY the playlist '" + args.playlist + "' from admin to ALL users? [Y|N]: ")
        if(strtobool(answer)):
            print("Execute copy all mode:")
            copy_all_mode(args)
        else: exit(-1)

    ## Delete all mode    
    elif(args.mode == 'delete-all' and args.playlist != None):
    	if(args.user != None):
            print("Your argument for the user will be ignored, it is not necessary here")        
        answer = raw_input("Are you sure to DELETE the playlist '" + args.playlist + "' from ALL users EXCEPT admin? [Y|N]: ")
        if(strtobool(answer)):
            print("Execute delete all mode:")
            delete_all_mode(args)
        else: exit(-1)

    else:
        print("Invalid arguments, try the help section (-h)")
        exit(-1)

    print("Finish ...")

if __name__== "__main__":
      main()
