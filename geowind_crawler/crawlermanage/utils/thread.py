# -*-encoding: utf-8 -*-

import threading
import time

import logging

from crawlermanage.utils.acticle_parser import extract
logger = logging.getLogger('crawlermanage.util.thread')

class ExtractArticle(threading.Thread): #The timer class is derived from the class threading.Thread
    def __init__(self, original_folder, goal_folder, request):
        threading.Thread.__init__(self)
        self.origin_folder = original_folder
        self.goal_folder = goal_folder
        self.request = request

    def run(self): #Overwrite run() method, put what you want the thread do here
        extract(self.origin_folder, self.goal_folder)
        session = self.request.session.get('info', None)
        if session:
            session.append('aaaaaaaaa')
            logger.info(self.request.session.get('info', None))
        else:
            info = []
            info.append('aaaaaaaaaaaaaaa')
            self.request.session['info'] = info
            logger.info(self.request.session.get('info', None))

