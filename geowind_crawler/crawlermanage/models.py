import datetime
from django.db import models
from mongoengine import Document, StringField, DateTimeField, connect, ListField

# Create your models here.
from geowind_crawler.settings import MONGODB_DATABASES

connect(MONGODB_DATABASES)
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