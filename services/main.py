#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import threading

from checker import Checker
from server import ServiceServer, ServiceRequestHandler


if __name__ == '__main__':
    # Console log handler
    logger = logging.getLogger('honeypot')
    ch = logging.StreamHandler()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    services = {'apache': [('127.0.0.1', 80), ('172.0.0.1', 88), ('192.168.0.155', 80)],
                'foo': [('8.8.8.8', 22)]}

    server = ServiceServer(('0.0.0.0', 5529), ServiceRequestHandler, services)

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

    # Start checker thread
    checker = Checker(services)
    checker_thread = threading.Thread(target=checker.worker)
    checker_thread.daemon = True
    checker_thread.start()

    server_thread.join()
