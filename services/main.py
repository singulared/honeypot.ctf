#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import threading

from server import ServiceServer, ServiceRequestHandler


if __name__ == '__main__':
    # Console log handler
    logger = logging.getLogger('honeypot')
    ch = logging.StreamHandler()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    services = {'apache': ['127.0.0.1', '192.168.0.155'],
                'foo': ['8.8.8.8']}

    server = ServiceServer(('0.0.0.0', 5529), ServiceRequestHandler, services)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    server_thread.join()
