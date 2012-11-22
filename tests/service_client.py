#!/usr/bin/env python3

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 5529))
s.send(b'foobar\n\rdeadbeef\n\r\n\r')
s.close()
