#!/usr/bin/python

import psutil, pwd, sys

# Get the users from /etc/passwd

def printResult(*args):
    if (len(args) == 3):
        print('{0:<8}{1:<20}{2}'.format(args[0], args[1], args[2]).strip())
    elif (len(args) == 4):
        print('{0:<12}{1:<12}{2:<42}-{3}'.format(args[0], args[1], args[2], args[3]))

def getAllUsers():
    print('{0:<8}{1:<20}{2}'.format('UID', 'USER', 'SHELL'))
    users = pwd.getpwall()
    for user in sorted(users, key=lambda x: x[2]):
        printResult(user.pw_uid, user.pw_name, user.pw_shell)

def filterUser(arg):
    print('{0:<8}{1:<20}{2}'.format('UID', 'USER', 'SHELL'))
    users = pwd.getpwall()
    for user in sorted(users, key=lambda x: x[2]):
        if arg in user.pw_name:
            printResult(user.pw_uid, user.pw_name, user.pw_shell)
        elif arg in str(user.pw_uid):
            printResult(user.pw_uid, user.pw_name, user.pw_shell)

# Get and print processes from psutil

def listAllProc():
    print('{0:<12}{1:<12}{2:42}{3}'.format('PID', 'USER', 'PROC', 'CMDLINE'))
    for proc in psutil.process_iter():
        try:
            pname = proc.name
            ppid = proc.pid
            puser = proc.username
            info = proc.as_dict(attrs=["cmdline"])
            pcmdline = ' '.join(info["cmdline"])[:255]
        except psutil.Error:
            pass
        printResult(ppid, puser, pname, pcmdline)

def filterProc(arg):
    print('{0:<12}{1:<12}{2:42}{3}'.format('PID', 'USER', 'PROC', 'CMDLINE'))
    for proc in psutil.process_iter():
        try:
            pname = proc.name
            ppid = proc.pid
            puser = proc.username
            info = proc.as_dict(attrs=["cmdline"])
            pcmdline = ' '.join(info["cmdline"])[:255]
        except psutil.Error:
            pass
        if arg in proc.name:
            printResult(ppid, puser, pname, pcmdline)

if __name__=='__main__':
    if len(sys.argv) < 2:
        print("""Usage:
        {0} user                (Lists all users)
        {0} user john   (Search for "john" in users database)
        {0} proc                (Lists all process)
        {0} proc ssh    (Search for "ssh" in running process)
        """.format(sys.argv[0]))
    elif (len(sys.argv) == 2) and (sys.argv[1] == "proc"):
        listAllProc()
    elif (len(sys.argv) == 3) and (sys.argv[1] == "proc"):
        filterProc(sys.argv[2])
    elif (len(sys.argv) == 2) and (sys.argv[1] == "user"):
        getAllUsers()
    elif (len(sys.argv) == 3) and (sys.argv[1] == "user"):
        filterUser(sys.argv[2])
    else:
        print('ERROR: Unknown arguments provided...')
