# -*- coding: utf-8 -*-

import telnetlib


# Server host:port
# Port 0 means to select an arbitrary unused port
server = ('0.0.0.0', 5528)

# Organizator flagservice host and port
flag_service = ('localhost', 2324)

# Command identificator
cid = 'honeypot'
timeout = 10


# Flag checking function
# must return true or false state for flag
def check(flag, tn):
    tn.read_until(b'flag: ', timeout)
    tn.write(flag.encode() + b'\n\n')
    state = tn.read_until(b'\n', timeout).decode().strip()
    if state == 'Correct flag!':
        status = 1
    elif state == 'Old flag! :(':
        status = 0
    elif state == 'Not a flag:':
        status = 2
    else:
        status = -1
    return(status)


def connect():
    tn = telnetlib.Telnet(flag_service[0], flag_service[1], timeout)
    tn.read_until(b'command: ', timeout)
    tn.write(cid.encode() + b'\n')
    return tn

#print(check('1234'))
