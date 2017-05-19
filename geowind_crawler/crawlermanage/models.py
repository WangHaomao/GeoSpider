import datetime

import mongoengine
from django.db import models
from mongoengine import Document, StringField, DateTimeField, connect, ListField

# Create your models here.

class Task(Document):
    taskname = StringField(max_length=30, required=True)
    starturls = ListField(required=True)
    starttime = DateTimeField(
        default=datetime.datetime.now, required=True, editable=False,
    )
    status = StringField(max_length=10)
    webtype = StringField(max_length=20)
    runmodel = StringField(max_length=20)
    describe = StringField(max_length=100)

class News(Document):
    title = StringField(max_length=30, required=True)
    url = StringField(max_length=200, required=True)
    acticle = StringField(max_length=2000)
    time = StringField(max_length=20)
    keywords = StringField(max_length=30)
