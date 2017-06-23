# -*- encoding: utf-8 -*-
import redis

from geospider.control.message_analyze import Analyze
from geospider.control.process_controller import ProcessController
from geospider.utils.mongodb_helper import connect_mongodb, TaskDao
from geospider.utils.settings_helper import get_attr


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
    redis_host = get_attr('REDIS_HOST')
    sub = get_attr('SUBSCRIBE')
    listener = MessageListener(redis_host)
    listener.subscribe(sub)
    db = connect_mongodb()
    taskdao = TaskDao(db)
    localhost = get_attr('LOCAL_HOST')
    p = ProcessController(localhost)
    p.scan()
    while (True):
        msg = listener.listen()
        params = Analyze(msg)
        op = params.get('op')
        taskid = params.get('taskid')
        task = taskdao.find_by_id(taskid)
        slave = task['slave']
        print(slave)
        if localhost in slave:
            print(op)
            if op == 'starttask':
                status = params.get('status')
                if status == 'running':
                    p.start(taskid)
                elif status == 'waitting':
                    p.wait(taskid)
            elif op == 'suspendtask':
                p.suspend(taskid)
            elif op == 'resumetask':
                p.resume(taskid)
            elif op == 'terminatetask':
                p.terminate(taskid)
