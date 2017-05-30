# -*- encoding: utf-8 -*-
from multiprocessing import Process
import time
import psutil
from geospider.control.spider_controller import init, run, delete


class ProcessController(object):

    process_list = []

    # 开始
    def start(self, taskid):
        init(taskid)
        p = Process(name=taskid, target=run, args=(taskid,))
        p.start()
        self.process_list.append(p)

    # 唤醒
    def resume(self, taskid):
        for p in self.process_list:
            if p.name == taskid and p.is_alive():
                ps = psutil.Process(p.pid)
                ps.resume()
                break

    # 停止
    def terminate(self, taskid):
        for p in self.process_list:
            if p.name == taskid and p.is_alive():
                p.terminate()
                delete(taskid)
                self.process_list.remove(p)
                break

    # 暂停
    def suspend(self, taskid):
        for p in self.process_list:
            if p.name == taskid and p.is_alive():
                ps = psutil.Process(p.pid)
                ps.suspend()
                break

    # 睡眠
    def sleep(self, taskid, t):
        for p in self.process_list:
            print p.name
            if p.name == taskid:
                time.sleep(t)
                break

    def processes(self):
        for p in self.process_list:
            print str(p.pid)+" "+p.name

if __name__ == '__main__':
    p = ProcessController()
    p.start('592ce4f79c1da96b04d28c30')
    p.start('592ce5539c1da96b04d28c31')
