#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import socketserver


class ServiceServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, host, handler, services):
        super(ServiceServer, self).__init__(host, handler)
        self.services = services
        self.logger = logging.getLogger('honeypot.services.ServiceServer')
        self.logger.info('Listen on {host}:{port}'.format(host=host[0], port=host[1]))


class ServiceRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.server.logger.info('Connect from: {}'.format(self.client_address))
        service = self.rfile.readline().decode().strip()
        self.server.logger.info('Request {}'.format(service))
        if service:
            self.wfile.write('\n'.join(['{}:{}'.format(ip, port) for ip, port in self.get_running(service)] + ['']).encode())

    def get_running(self, service):
        try:
            return self.server.services[service]
        except KeyError:
            return []
