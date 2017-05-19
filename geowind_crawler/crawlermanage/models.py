from django.db import models

# Create your models here.

class Task(models.Model):
    taskname = models.CharField(max_length=30)
    starturls = models.CharField(max_length=500)
    webtype = models.CharField(max_length=30)
    runmodel = models.CharField(max_length=30)
