#!/usr/bin/python3
# -*- coding: utf-8 -*-

import concurrent.futures
import config
import itertools
import logging
import socket
import threading
import time
import queue


class Checker:
    def __init__(self, services):
        self.logger = logging.getLogger('honeypot.services.Checker')
        self.logger.info('Init Checker')
        self.services = services
        self.queue = queue.Queue()

    def get_task_generator(self):
        for service, ports in config.services.items():
            ips = itertools.product(*config.ip + [ports])
            for ip in ips:
                yield {'srv': service, 'ip': ('{}.{}.{}.{}'.format(*ip[:4]), ip[4])}

    def fill_queue(self):
        self.logger.info('Start fill queue')
        task_generator = self.get_task_generator()
        for task in task_generator:
            self.queue.put(task)
        self.logger.info('End fill queue')

    def check_task(self, task):
        thread = threading.current_thread()
        self.logger.info('Task {} started on {}'.format(task, thread.getName()))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(task['ip'])
            task['state'] = True
        except socket.error:
            task['state'] = False
        finally:
            sock.close()
        self.logger.info('Task {} ended on {}'.format(task, thread.getName()))
        return task

    def check_queue(self):
        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=config.max_workers) as executor:
            while self.queue.qsize():
                futures.append(executor.submit(self.check_task, self.queue.get()))
            for future in concurrent.futures.as_completed(futures):
                task = future.result()
                if task['state']:
                    try:
                        self.services[task['srv']].append(task['ip'])
                    except KeyError:
                        self.services[task['srv']] = [task['ip']]

    def worker(self):
        while True:
            self.services.clear()
            self.fill_queue()
            self.check_queue()
            time.sleep(config.check_timeout)
