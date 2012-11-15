# -*- coding: utf-8 -*-

import telnetlib


# Server host:port
# Port 0 means to select an arbitrary unused port
server = ('localhost', 5528)

# Organizator flagservice host and port
flag_service = ('localhost', 2324)

# Command identificator
cid = 'honeypot'


def check_test(flag):
    import random
    return random.randint(0, 1)


# Flag checking function
# must return true or false state for flag
def check(flag):
    print('Checking', flag)
    print('connect')
    tn = telnetlib.Telnet(flag_service[0], flag_service[1])
    print('read command')
    tn.read_until(b'command: ')
    print('write command')
    tn.write(cid.encode() + b'\n')
    print('read flag')
    tn.read_until(b'flag: ')
    print('write flag')
    tn.write(flag.encode() + b'\n\n')
    print('read state')
    state = tn.read_until(b'\n').decode().strip()
    print(state)
    if state == 'Correct flag!':
        status = True
    else:
        status = False
    print('write line')
    tn.write(b'\n')
    print('close')
    tn.close()
    return(status)

#print(check('1234'))
