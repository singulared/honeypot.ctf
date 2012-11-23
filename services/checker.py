#!/usr/bin/python3
# -*- coding: utf-8 -*-

import config
import itertools
import logging
import queue


class Checker:
    def __init__(self, services):
        self.logger = logging.getLoger('honeypot.services.Checker')
        self.logger.info('Init Checker')
        self.services = services
        self.queue = queue.Queue()

    def get_task_generator(self):
        for service, ports in config.services.items():
            print(service, ports)
            ips = itertools.product(*config.ip + [ports])
            for ip in ips:
                yield {'srv': service, 'ip': ('{}.{}.{}.{}'.format(*ip[:4]), ip[4])}

    def fill_queue(self):
        self.logger.info('Start fill queue')
        task_generator = self.get_task_generator()
        for task in task_generator:
            self.queue.put(task)
        self.logger.info('End fill queue')


services = []
c = Checker(services)
tasks = c.get_tasks()
for task in tasks:
    print(task)
