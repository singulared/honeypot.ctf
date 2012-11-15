#!/usr/bin/python3
# -*- coding: utf-8 -*-

import config
import os
import signal
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


class FlagRequestHandler(socketserver.BaseRequestHandler):
    client_linesep = os.linesep

    def handle(self):
        buf = None
        data = b''
        while buf not in line_seps:
            buf = self.request.recv(4096)
            data += buf
        else:
            self.client_linesep = buf.decode()
        flags = self.parse_flags(data)
        self.check_flags(flags)

    def parse_flags(self, data):
        return [flag for flag in data.decode().split(self.client_linesep) if flag]

    def check_flags(self, flags):
        conn = sqlite3.connect(self.server.cfg.db)
        db = conn.cursor()
        for flag in flags:
            db.execute('select * from flags where flag = ?', (flag,))
            print('check', flag)
            if not db.fetchone():
                # @TODO: add timeout exception check
                status = self.server.cfg.check(flag)
                print(flag, status)
                db.execute('insert into flags values (?, ?, ?, ?, ?)', (
                    flag, '192.169.0.155', int(time.time()), int(time.time()), status))
        conn.commit()


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

    # Get cfg
    cfg = config.load()
    init_db(cfg)

    server = FlagServer(cfg.server, FlagRequestHandler)
    server.set_config(cfg)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    server_thread.join()
