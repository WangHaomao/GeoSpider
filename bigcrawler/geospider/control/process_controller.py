# -*- encoding: utf-8 -*-
import ctypes
import os
from multiprocessing import Process
import time
import psutil
import signal

from geospider.control.spider_controller import init, run, delete, wait, scan


class ProcessController(object):

    process_list = []

    '''
        开始一个进程，开始任务
    '''
    def start(self, taskid):
        init(taskid)
        p = Process(name=taskid, target=run, args=(taskid,))
        p.start()
        print(p.pid)
        self.process_list.append(p)

    '''
        唤醒一个阻塞的进程，将暂停状态的任务重新启动
    '''
    def resume(self, taskid):
        for p in self.process_list:
            if p.name == taskid and p.is_alive():
                ps = psutil.Process(p.pid)
                ps.resume()
                break

    '''
        杀死一个进程，终止任务
    '''
    def terminate(self, taskid):
        for p in self.process_list:
            if p.name == taskid and p.is_alive():
                print("杀死进程%s"%(taskid))
                # p.terminate()
                os.kill(p.pid, signal.SIGKILL)
                delete(taskid)
                self.process_list.remove(p)
                break

    '''
        暂停进程，暂停任务
    '''
    def suspend(self, taskid):
        for p in self.process_list:
            if p.name == taskid and p.is_alive():
                ps = psutil.Process(p.pid)
                ps.suspend()
                break

    '''
        休眠
    '''
    def sleep(self, taskid, t):
        for p in self.process_list:
            print(p.name)
            if p.name == taskid:
                time.sleep(t)
                break

    '''
        查看所有的进程名
    '''
    def processes(self):
        for p in self.process_list:
            print(str(p.pid)+" "+p.name)

    '''
        开启一个进程，等待任务启动
    '''
    def wait(self, taskid):
        init(taskid)
        p = Process(name=taskid, target=wait, args=(taskid,))
        p.start()
        print(p.pid)
        self.process_list.append(p)

    '''
        扫描所有进程，将到时间的进程杀死
    '''
    def scan(self):
        p = Process(name='spider_scaner', target=scan)
        p.start()
        self.process_list.append(p)

if __name__ == '__main__':
    p = ProcessController()
    p.start('5948cbf59c1da929309ad2e0')
    p.sleep('5948cbf59c1da929309ad2e0', 5)
    p.terminate('5948cbf59c1da929309ad2e0')
