# -*- encoding: utf-8 -*-
import os

import mongoengine
import redis
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from scrapy import cmdline

from bigcrawler.main import run

import logging

from crawlermanage.models import Task

logger = logging.getLogger('crawlermanage.views')
mongoengine.register_connection('default', 'p')

# Create your views here.

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

def login(request):
    if request.method == 'POST':
        uf = LoginForm(request.POST)
        if uf.is_valid():  
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # user = User.objects.filter(username__exact = username,password__exact = password)  
            # if user:  
            #     request.session['username'] = username  
            #     return HttpResponseRedirect('/blog/index')  
            # else:  
            #     err = 'incorrect username or pwd,please input again.'  
            #     return render_to_response('login.html',{'err':err})  
            if username=='admin' and password=='a':
                #request.session['username'] = username
                return HttpResponseRedirect('/crawlermanage/index')
            else:
                return render_to_response('crawlermanage/login.html', {'error': '用户名或密码错误'})

    else:
        return render_to_response('crawlermanage/login.html')

def index(request):
    main = os.path.dirname(__file__) + "/../../bigcrawler/main.py"
    logger.info(main)
    os.system("python " + main)
    return render(request, 'crawlermanage/index.html')

def tasks(request):
    tasklist = Task.objects.all()
    return render(request, 'crawlermanage/tasks.html', {'tasklist':tasklist})

def ecommercedata(request):
    return render(request, 'crawlermanage/ecommercedata.html')

def newsdata(request):
    return render(request, 'crawlermanage/newsdata.html')

def layout(request):
    # taskname=ads&starturls=fsd&webtype=option1&optionsRadios=option1
    if request.method == 'POST':
        taskname = request.POST.get('taskname', '')
        starturls = request.POST.get('starturls', '')
        webtype = request.POST.get('webtype', '')
        runmodel = request.POST.get('runmodel', '')

        if taskname=='' or starturls=='':
            error1 = None
            error2 = None
            if taskname=='':
                error1 = u'任务名不能为空'
            if starturls=='':
                error2= u'起始URL不能为空'
            return render_to_response('crawlermanage/layout.html', {'taskname':taskname, 'starturls':starturls, 'error1': error1, 'error2': error2})
        else:
            status = 'running'
            list_url = starturls.strip().split('\n')
            task = Task.objects.create(taskname=taskname, starturls=list_url, status=status, webtype=webtype, runmodel=runmodel)

            main = os.path.dirname(__file__) + "/../../bigcrawler/main.py"
            logger.info(main)
            os.system("python " + main)

            return HttpResponseRedirect('/crawlermanage/tasks')
    else:
        return render_to_response('crawlermanage/layout.html')

