import datetime

import mongoengine
from django.db import models
from mongoengine import Document, StringField, DateTimeField, connect, ListField

# Create your models here.

class Task(Document):
    taskname = StringField(max_length=30, required=True)
    starturls = ListField(required=True)
    starttime = StringField(max_length=20, required=True, editable=False)
    endtime = StringField(max_length=20)
    webtype = StringField(max_length=20)
    describe = StringField(max_length=100)
    slave = ListField(required=True)
    status = StringField(max_length=10)

class News(Document):
    title = StringField(max_length=30, required=True)
    url = StringField(max_length=200, required=True)
    acticle = StringField(max_length=2000)
    time = StringField(max_length=20)
    keywords = StringField(max_length=30)
    taskid = StringField(max_length=30, required=True)
