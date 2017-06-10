# -*- encoding: utf-8 -*-
import redis

from geospider.control.message_analyze import Analyze
from geospider.control.process_controller import ProcessController


class MessageListener(object):

    channels = []

    def __init__(self, host):
        self.rc = redis.Redis(host=host)
        self.ps = self.rc.pubsub()

    def subscribe(self, channel):
        self.channels.append(channel)
        self.ps.subscribe(channel)

    def listen(self):
        for item in self.ps.listen():
            if item['type'] == 'message':
                return item['data']


if __name__ == '__main__':
    listener = MessageListener('127.0.0.1')
    listener.subscribe('crawler')
    p = ProcessController()
    while(True):
        msg = listener.listen()
        params = Analyze(msg)
        op = params.get('op')
        print(op)
        if op=='starttask':
            taskid = params.get('taskid')
            p.start(taskid)
        elif op=='suspendtask':
            taskid = params.get('taskid')
            p.suspend(taskid)
        elif op=='resumetask':
            taskid = params.get('taskid')
            p.resume(taskid)
        elif op=='terminatetask':
            taskid = params.get('taskid')
            p.terminate(taskid)


    # p = ProcessController()
    # p.start('592ceac49c1da96d222995d9')
    # p.sleep('592ceac49c1da96d222995d9', 10)
    # p.processes()
    # print('pause......')
    # #p.pause('592ceac49c1da96d222995d9')
    # p.processes()
    # p.suspend('592ceac49c1da96d222995d9')
    # p.sleep('592ceac49c1da96d222995d9', 10)
    # p.resume('592ceac49c1da96d222995d9')
    # print('restart...')
    # p.restart('592ceac49c1da96d222995d9')
    # p.processes()