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
    # 插入操作
    def find_by_id(self, id):
        return self.db.task.find_one({'_id': ObjectId(id)})




if __name__ == '__main__':
    db=connect_mongodb()
    taskDao = TaskDao(db)
    a = taskDao.find_by_id('5948cbf59c1da929309ad2e0')
    print(a)