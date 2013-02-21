# -*- coding: utf-8 -*-

import telnetlib
import flagstatus


# Server host:port
# Port 0 means to select an arbitrary unused port
server = ('0.0.0.0', 5528)

# Organizator flagservice host and port
flag_service = ('localhost', 2324)

# Command identificator
cid = 'honeypot'
timeout = 10


# Flag checking function
# Return status:
#   1  - Correct flag
#   0  - Old flag
#   2  - Not a flag
#   -1 - Server is down or another error
def check(flag, tn):
    tn.read_until(b'flag: ', timeout)
    tn.write(flag.encode() + b'\n\n')
    state = tn.read_until(b'\n', timeout).decode().strip()
    if state == 'Correct flag!':
        status = flagstatus.correct
    elif state == 'Old flag! :(':
        status = flagstatus.old
    elif state == 'Not a flag:':
        status = flagstatus.not_flag
    else:
        status = flagstatus.error
    return(status)


def connect():
    tn = telnetlib.Telnet(flag_service[0], flag_service[1], timeout)
    tn.read_until(b'command: ', timeout)
    tn.write(cid.encode() + b'\n')
    return tn
