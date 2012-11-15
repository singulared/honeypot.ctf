#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import socketserver
import threading


class FlagServericeHandler(socketserver.BaseRequestHandler):
    command_list = ['honeypot']

    def handle(self):
        self.request.send(b'This is test flag service\nPlease enter you command: ')
        cid = self.request.recv(1024).decode().strip()
        if cid not in self.command_list:
            self.request.send(b'Wrong command\n')
            self.request.close()
            return
        while True:
            self.request.send(b'Enter flag: ')
            flag = self.request.recv(1024).decode().strip()
            if not flag:
                break
            if len(flag) < 4:
                self.request.send(b'Not a flag\n')
                continue
            status = random.randint(0, 1)
            if status:
                self.request.send(b'Correct flag!\n')
            else:
                self.request.send(b'Old flag! :(\n')
            print('{} [{}]: {} is {}!'.format(cid, self.client_address[0], flag, bool(status)))


class FlagService(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    print('listen on {}'.format(2324))
    server = FlagService(('0.0.0.0', 2324), FlagServericeHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    server_thread.join()
