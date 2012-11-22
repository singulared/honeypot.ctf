#!/usr/bin/python3
# -*- coding: utf-8 -*-

import config
import queue


class Checker:
    def __init__(self, services):
        self.services = services
        self.queue = queue.Queue()

    def init_queue(self):
        ips = {}
        #for service in config.services.keys()
        for octet, ip in enumerate(config.ip):
            if type(ip) in (range, tuple):
                pass
            #print(octet, ip)
            ips[octet] = str(ip)
        print('{}.{}.{}.{}'.format(**ips.values()))

services = []
c = Checker(services)
c.init_queue()
