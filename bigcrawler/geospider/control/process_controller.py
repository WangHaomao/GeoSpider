# -*- encoding: utf-8 -*-
from multiprocessing import Process

import time

from geospider.control.spider_controller import init, run, delete


class ProcessController(object):

    process_list = []

    def start(self, taskid, type):
        init(taskid, type)
        p = Process(name=taskid, target=run, args=(taskid,))
        p.start()
        self.process_list.append(p)

    def terminate(self, taskid):
        for p in self.process_list:
            if p.name == taskid and p.is_alive():
                p.terminate()
                delete(taskid)
                self.process_list.remove(p)
                break

    def sleep(self, taskid, t):
        for p in self.process_list:
            print 'aaaaaaaaaaaaaaddddddddddd'
            print p.name
            if p.name == taskid:
                print('aaaaaaaa')
                time.sleep(t)
                break

    def processes(self):
        for p in self.process_list:
            print p.name
