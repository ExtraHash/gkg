import sys
import requests
from pathlib import Path
from time import sleep


def main():
    args = get_cli_args()

    if not "username" in args.keys():
        args["username"] = input("Please enter your GitHub username: ")

    if args["loop"]:
        while True:
            write_keys(args)
            sleep(1000 * 60 * 5)
    else:
        write_keys(args)

    

def write_keys(args):
    print("Fetching public keys for " + args["username"])
    new_keys = request_keys(args["username"])
    print(str(len(new_keys)) + " keys downloaded from GitHub.")

    if args["write"]:
        print("Writing keys to authorized_keys file at " + args["path"])
        with open(args["path"], "w+") as authorized_keys_file:
            authorized_keys_file.writelines(key + "\n" for key in new_keys)
            authorized_keys_file.flush()
            authorized_keys_file.close()
            print('Keys written sucessfully to ' + args["path"])
    else:
        print()
        for key in new_keys:
            print(key)


def request_keys(username):
    res = requests.get(url="https://api.github.com/users/" + username + "/keys")
    keys = []
    for key_info in res.json():
        keys.append(key_info["key"])

    return keys

def print_help_menu():
    print('-u Username       Username      Takes one parameter, the username on GitHub for which to request the keys.')
    print('-p /path/to/file  Path          Takes one parameter, the path to output the authorized_keys file to. Has no effect if -w is not set.')
    print('-w                Write         Takes no parameters. If set, it will write the authorized_keys file to disk, otherwise it will simply print it to console and exit.')
    print('-h                Help          Displays this help menu. Can also be accessed at --help')


def get_cli_args():
    args = {
        'write': False,
        'path': str(Path.home()) + "/.ssh/authorized_keys",
        'loop': False
    }
    for arg in sys.argv:
        if arg == "-u":
            try:
                args["username"] = sys.argv[sys.argv.index("-u") + 1]
            except Exception:
                quit('Wrong syntax for -u username flag (-u Username)')
        if arg == "-p":
            try:
                args["path"] = sys.argv[sys.argv.index("-p") + 1]
            except Exception:
                quit('Wrong syntax for -p path flag (-p /path/to/authorized_keys)')
        if arg == "-w":
            args["write"] = True
        if arg == "-l":
            args["loop"] = True
        if arg == '-h':
            print_help_menu()
            quit()
        if arg == '--help':
            print_help_menu()
            quit()

    return args


main()
