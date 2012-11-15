# -*- coding: utf-8 -*-

import telnetlib


# Server host:port
# Port 0 means to select an arbitrary unused port
server = ('localhost', 5528)

# Organizator flagservice host and port
flag_service = ('localhost', 2323)

# Command identificator
cid = 'honeypot'


def check_test(flag):
    import random
    return random.randint(0, 1)


# Flag checking function
# must return true or false state for flag
def check(flag):
    tn = telnetlib.Telnet(flag_service[0], flag_service[1])
    tn.read_until(b'command: ')
    tn.write(cid.encode() + b'\n')
    tn.read_until(b'flag: ')
    tn.write(flag.encode() + b'\n\n')
    state = tn.read_all().decode().strip()
    print(state)
    if state == 'Correct flag!':
        return True
    else:
        return False

print(check('1234'))
