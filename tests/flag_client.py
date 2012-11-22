#!/usr/bin/env python3

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 5528))
s.send(b'foobar\ndeadbeef\n\n')
s.close()
