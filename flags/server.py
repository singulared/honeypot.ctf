#!/usr/bin/python3
# -*- coding: utf-8 -*-

import config
import os
import signal
import socket
import socketserver
import sqlite3
import sys
import time
import threading


line_seps = [b'\n', b'\r\n', b'\r']
server = None


class FlagServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def set_config(self, cfg):
        self.cfg = cfg

    def set_queue(self, queue):
        self.queue = queue


class FlagRequestHandler(socketserver.BaseRequestHandler):
    client_linesep = os.linesep

    def handle(self):
        print('connect from: {}'.format(self.client_address))
        buf = None
        data = b''
        while buf not in line_seps:
            buf = self.request.recv(4096)
            data += buf
        else:
            self.client_linesep = buf.decode()
        tasks = self.parse_flags(data)
        self.server.queue += tasks
        print('Append:', [t['flag'] for t in tasks])

    def parse_flags(self, data):
        return [{'flag': flag, 'ip': self.client_address} for flag in data.decode().split(self.client_linesep) if flag]


class Checker:
    connect = None

    def __init__(self, cfg, queue):
        self.cfg = cfg
        self.queue = queue
        self.check_timeout = getattr(self.cfg, 'check_timeout', 3)

    def run(self):
        while True:
            if self.connect is None:
                try:
                    self.connect = self.cfg.connect()
                except socket.error:
                    time.sleep(self.check_timeout)
                    print('[Error]', 'Unable to connect with flagservice')
                    continue
            if self.queue:
                print('Queue:', [t['flag'] for t in self.queue])
            while self.queue:
                task = self.queue.pop(0)
                if self.check(task) < 0:
                    self.connect = None
                    break
            time.sleep(self.check_timeout)

    def check(self, task):
        conn = sqlite3.connect(self.cfg.db)
        db = conn.cursor()
        db.execute('select * from flags where flag = ?', (task['flag'],))
        if not db.fetchone():
            try:
                status = self.cfg.check(task['flag'], self.connect)
            except EOFError:
                status = -1
            print(task, status)
            db.execute('insert into flags values (?, ?, ?, ?, ?)', (
                task['flag'], task['ip'][0], int(time.time()), int(time.time()), status))
        conn.commit()
        return status


def stop_handler(signal, frame):
        print('\nStopping flag service.')
        if server:
            server.shutdown()
        sys.exit(0)


def init_db(cfg):
    conn = sqlite3.connect(cfg.db)
    c = conn.cursor()
    c.execute('select * from sqlite_master where tbl_name = "flags"')
    if not c.fetchone():
        c.executescript('''
        CREATE TABLE flags (
        flag TEXT PRIMARY KEY,
        ip TEXT NOT NULL,
        added INTEGER NOT NULL,
        checked INTEGER NOT NULL,
        status INTEGER NOT NULL
        );

        CREATE INDEX flags_idx
        ON flags (flag);''')
        conn.commit()
        conn.close()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop_handler)

    # init queue
    queue = []

    # Get cfg
    cfg = config.load()
    init_db(cfg)

    server = FlagServer(cfg.server, FlagRequestHandler)
    server.set_config(cfg)
    server.set_queue(queue)
    ip, port = server.server_address
    print('Started on {}:{}'.format(ip, port))

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

    # Start checker thread
    checker = Checker(cfg, queue)
    checker_thread = threading.Thread(target=checker.run)
    checker_thread.daemon = True
    checker_thread.start()
    server_thread.join()
