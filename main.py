import re, os, sys, argparse
from distutils.util import strtobool
from scripts.single_mode import copy_single_mode, delete_single_mode
from scripts.all_mode import copy_all_mode, delete_all_mode
from scripts.daemon_mode import daemon_mode
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, "VS-Utils"))
from prints import errmsg, debugmsg, init_logging

def ask_user(question):
    answer = input(question)
    if not answer:
        answer = 'Y' if 'Y' in re.split(r'[\[\]|]', question)[1:3] else 'N'
    return strtobool(answer)

def main():

    ## Get arguments
    choices = ['copy-single', 'copy-all', 'delete-single', 'delete-all']
    parser = argparse.ArgumentParser(usage="sudo -u postgres python main.py -m <mode> -p <playlist-name>")
    parser.add_argument('--daemon',   help="Whether to run daemon mode", action="store_true")
    parser.add_argument("--playlist", help="Name of a playlist", metavar='')
    parser.add_argument("--user",     help="Username", metavar='')
    parser.add_argument("--mode",     help="Copy/Delete a playlist to/of a single or all user(s): {%(choices)s}",
                                      default='copy-single', nargs='?', choices=choices, metavar="")
    args = parser.parse_args()
    args.script_dir = cur_dir
    args.scope = "postgres"

    ## Initialize logging
    init_logging(args)

    ## Daemon execution
    if args.daemon:
        return daemon_mode(args)

    ## Copy single mode
    if (args.mode == 'copy-single' and args.user != None and args.playlist != None):
        question = "Are you sure to COPY the playlist '{playlist}' from " \
                   "admin to user '{user}'? [Y|n]: ".format(playlist=args.playlist, user=args.user)
        if (ask_user(question)):
            copy_single_mode(args)
        else: exit(-1)

    ## Delete single mode
    elif (args.mode == 'delete-single' and args.playlist != None and args.user != None):
        question = "Are you sure to DELETE the playlist '{playlist}' from " \
                   "user '{user}'? [y|N]: ".format(playlist=args.playlist, user=args.user)
        if (ask_user(question)):
            delete_single_mode(args)
        else: exit(-1)

    ## Copy all mode
    elif (args.mode == 'copy-all' and args.playlist != None):
        if (args.user != None):
            debugmsg("Your parameter for \"--user\" will be ignored, it is not necessary here")
        question = "Are you sure to COPY the playlist '{playlist}' from admin to ALL users? " \
                    "[Y|n]: ".format(playlist=args.playlist)
        if (ask_user(question)):
            copy_all_mode(args)
        else: exit(-1)

    ## Delete all mode
    elif (args.mode == 'delete-all' and args.playlist != None):
        if (args.user != None):
            debugmsg("Your argument for the \"--user\" will be ignored, it is not necessary here")
        question = "Are you sure to DELETE the playlist '{playlist}' from ALL users EXCEPT admin? " \
                    "[y|N]: ".format(playlist=args.playlist)
        if (ask_user(question)):
            delete_all_mode(args)
        else:
            exit(-1)

    else:
        errmsg("Invalid arguments, try the help section (-h)")
        exit(-1)

    debugmsg("Finish ...", args.mode)

if __name__== "__main__":
      main()
