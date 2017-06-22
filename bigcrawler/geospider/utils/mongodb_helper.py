# -*- encoding: utf-8 -*-
from bson import ObjectId
from pymongo import MongoClient


def connect_mongodb():
    client = MongoClient('localhost:27017')
    db = client.news  # 'examples' here is the database name.it will be created if it does not exist.
    # 如果 examples不存在，那么就会新建它
    return db


class TaskDao(object):
    def __init__(self, db):
        self.db = db

    def find_by_id(self, taskid):
        return self.db.task.find_one({'_id': ObjectId(taskid)})

    def find_by_status(self, status):
        cursor = self.db.task.find({'status': status})
        task_list = []
        for i in cursor:
            task_list.append(i)
        return task_list

    def save(self, task):
        self.db.task.save(task)


class ProcessDao(object):
    def __init__(self, db):
        self.db = db

    def find_all(self):
        cursor = self.db.process.find()
        process_list = []
        for i in cursor:
            process_list.append(i)
        return process_list

    def find_by_status(self, status):
        cursor = self.db.process.find({'status': status})
        process_list = []
        for i in cursor:
            process_list.append(i)
        return process_list

    def find_by_taskid(self, taskid):
        cursor = self.db.process.find({'taskid': taskid})
        process_list = []
        for i in cursor:
            process_list.append(i)
        return process_list

    def insert_process(self, pid, taskid, status):
        self.db.process.insert_one({'pid': pid, 'taskid': taskid, 'status': status})

    def delete_by_taskid(self, taskid):
        self.db.process.remove({"taskid": taskid})

    def update_status_by_taskid(self, taskid, status):
        task_list = self.find_by_taskid(taskid)
        for task in task_list:
            task['status'] = status
            self.db.process.save(task)
        # task['status']=status

        # self.db.process.save(task)


if __name__ == '__main__':
    db = connect_mongodb()
    pro = ProcessDao(db)
    dict = pro.find_by_status("scanner")
    #print(len(dict))
    # processDao.insert_process('a','d','runnnig')
    # processDao.delete_by_taskid('594b94219c1da9212141ef75')
    #processDao.update_status_by_taskid('594b94219c1da9212141ef75','waittinig')
    taskid='594bdd359c1da93dba43a3d3'
    process_list = pro.find_by_taskid(taskid)
    # pro.insert_process('a','a','a')
    print(process_list)