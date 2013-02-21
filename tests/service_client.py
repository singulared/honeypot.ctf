#!/usr/bin/env python3

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 5529))
s.send(b'ssh\nfoobar\n\rdeadbeef\n\r\n\r')
print(s.recv(1024))
s.close()
