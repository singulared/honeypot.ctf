#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import socket
import time


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(bytes(message, 'ascii'))
        print('Sended at: {}'.format(datetime.datetime.now()))
        time.sleep(3)
        response = str(sock.recv(1024), 'ascii')
        print("Received: {} at: {}".format(response, datetime.datetime.now()))
    finally:
        sock.close()

data = input('>')
#client('localhost', 5528, data)
print('run {}'.format(data))
