#-*- encoding: utf-8 -*-
import os

import redis
from copy import deepcopy

import time

import signal
from bson import ObjectId
from scrapy import cmdline
import pymongo
from geospider.spiders.news_spider import NewsSpider
from geospider.utils.mongodb_helper import connect_mongodb, TaskDao, ProcessDao
from geospider.utils.redis_helper import connect_redis, URLDao
from geospider.utils.time_util import compare_time


def init(taskid):
    mongodb = connect_mongodb()
    taskdao = TaskDao(mongodb)
    task = taskdao.find_by_id(taskid)

    temp = None
    if "news"==task['webtype']:
        temp = deepcopy(NewsSpider)
        temp.name = taskid
        temp.redis_key = taskid+":start_urls"

    redis = connect_redis()
    url_manager = URLDao(redis)
    allowed_domains = []
    for url in task['starturls']:
        url_manager.insert_url(taskid, url)
        allowed_domains.append(url.split('/')[2])
    temp.allowed_domains = allowed_domains


def run(taskid):
    cmdline.execute(("scrapy crawl "+taskid+" --nolog").split())

def wait(taskid):

    mongodb = connect_mongodb()
    taskdao = TaskDao(mongodb)
    task = taskdao.find_by_id(taskid)

    starttime = task['starttime']
    endtime = task['endtime']
    flag = False
    while(flag is False):
        flag = compare_time(time.strftime("%Y/%m/%d %H:%M"), starttime, endtime)
        time.sleep(60)
    if flag is True:
        task['status'] = 'running'
        taskdao.save(task)
        processdao = ProcessDao(mongodb)
        processdao.update_status_by_taskid(taskid, 'running')
        run(taskid)



def delete(taskid, is_changed):
    redis = connect_redis()
    url_manager = URLDao(redis)
    url_manager.delete_task(taskid)

    if is_changed:
        mongodb = connect_mongodb()
        taskdao = TaskDao(mongodb)
        task = taskdao.find_by_id(taskid)

        endtime = time.strftime("%Y/%m/%d %H:%M")
        task['endtime']=endtime
        taskdao.save(task)


def scaner():
    mongodb = connect_mongodb()
    taskdao = TaskDao(mongodb)
    processdao = ProcessDao(mongodb)
    while(True):
        task_list = taskdao.find_by_status('running')
        for t in task_list:
            starttime = t['starttime']
            endtime = t['endtime']
            if endtime != '':
                if compare_time(time.strftime("%Y/%m/%d %H:%M"), starttime, endtime) is False:
                    taskid = str(t['_id'])
                    process_list = processdao.find_by_taskid(taskid)
                    test = processdao.find_by_taskid('')
                    for p in process_list:
                        if p['taskid'] == taskid and p['status']!='stopping':
                            print("杀死进程%s" % (taskid))
                            # p.terminate()
                            os.kill(p['pid'], signal.SIGKILL)
                            delete(taskid, False)
                            t['status']='stopping'
                            taskdao.save(t)
                    processdao.delete_by_taskid(taskid)
        time.sleep(60)
