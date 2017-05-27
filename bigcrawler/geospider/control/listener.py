# -*- encoding: utf-8 -*-
import redis

from geospider.control.process_controller import ProcessController


class Listener(object):

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
                print item['data']


if __name__ == '__main__':
    # listener = Listener('127.0.0.1')
    # listener.subscribe('crawler')
    # listener.listen()
    p = ProcessController()
    p.start('591eb2df9c1da9154b001832', 'news')
    p.sleep('591eb2df9c1da9154b001832', 5)
    p.terminate('591eb2df9c1da9154b001832')
    # p.processes()