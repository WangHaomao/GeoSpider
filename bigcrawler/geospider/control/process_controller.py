# -*- encoding: utf-8 -*-
import os
from multiprocessing import Process,Manager
import time
import psutil
import signal

from geospider.control.spider_controller import init, run, delete, wait, scaner
from geospider.utils.mongodb_helper import connect_mongodb, ProcessDao, TaskDao


class ProcessController(object):
    def __init__(self, localhost):
        mongodb = connect_mongodb()
        self.processdao = ProcessDao(mongodb)
        self.taskdao = TaskDao(mongodb)
        self.localhost = localhost
    '''
        开始一个进程，开始任务
    '''

    def start(self, taskid, is_restart):
        init(taskid, is_restart)
        p = Process(name=taskid, target=run, args=(taskid,))
        p.start()
        print(p.pid)
        self.processdao.insert_process(self.localhost, p.pid, taskid, 'running')
        # self.process_list.append(p)

    '''
        唤醒一个阻塞的进程，将暂停状态的任务重新启动
    '''

    def resume(self, taskid):
        process_list = self.processdao.find_by_localhost_and_taskid(self.localhost, taskid)
        for p in process_list:
            if p['taskid'] == taskid:
                try:
                    ps = psutil.Process(p['pid'])
                    ps.resume()
                except:
                    continue
        self.processdao.update_status_by_localhost_and_taskid(self.localhost, taskid, 'running')

    '''
        杀死一个进程，终止任务
    '''

    def terminate(self, taskid):
        process_list = self.processdao.find_by_localhost_and_taskid(self.localhost, taskid)
        for p in process_list:
            if p['taskid'] == taskid and p['status'] != 'stopping':
                try:
                    print("杀死进程%s" % (p['pid']))
                    # p.terminate()
                    os.kill(p['pid'], signal.SIGKILL)
                except:
                    continue
                delete(taskid, True)
        self.processdao.delete_by_localhost_and_taskid(self.localhost, taskid)

    '''
        暂停进程，暂停任务
    '''

    def suspend(self, taskid):
        process_list = self.processdao.find_by_localhost_and_taskid(self.localhost, taskid)
        for p in process_list:
            if p['taskid'] == taskid and p['status'] != 'stopping':
                try:
                    ps = psutil.Process(p['pid'])
                    ps.suspend()
                except:
                    continue
        self.processdao.update_status_by_localhost_and_taskid(self.localhost, taskid, 'pausing')

    '''
        休眠
    '''

    def sleep(self, taskid, t):
        process_list = self.processdao.find_all()
        for p in process_list:
            print(p['taskid'])
            if p['taskid'] == taskid:
                time.sleep(t)
                break

    '''
        查看所有的进程名
    '''

    def processes(self):
        process_list = self.processdao.find_all()
        for p in process_list:
            print(str(p['pid']) + " " + p['taskid'])

    '''
        开启一个进程，等待任务启动
    '''

    def wait(self, taskid, is_restart):
        init(taskid, is_restart)
        p = Process(name=taskid, target=wait, args=(taskid,))
        p.start()
        print(p.pid)
        self.processdao.insert_process(self.localhost, p.pid, taskid, 'waitting')

    '''
        扫描所有进程，将到时间的进程杀死
    '''

    def scan(self):
        # scanner = self.processdao.find_by_status('scanner')
        # if len(scanner) == 0:
        p = Process(name='spider_scaner', target=scaner)
        p.start()
        self.processdao.insert_process(self.localhost, p.pid, '', 'scanner')


if __name__ == '__main__':
    p = ProcessController('127.0.0.1')
    p.start('5948cbf59c1da929309ad2e0')
    p.sleep('5948cbf59c1da929309ad2e0', 5)
    p.terminate('5948cbf59c1da929309ad2e0')
