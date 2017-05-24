# -*- encoding: utf-8 -*-
import os

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
import subprocess


import logging

from django.views.generic import ListView

from crawlermanage.models import Task, News
from crawlermanage.page import paging

logger = logging.getLogger('crawlermanage.views')
#mongoengine.register_connection('default', 'p')

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
    return render(request, 'crawlermanage/index.html')

def tasks(request):
    tasklist = Task.objects.all()
    return render(request, 'crawlermanage/tasks.html', {'tasklist':tasklist})

def ecommercedata(request):
    return render(request, 'crawlermanage/ecommercedata.html')

# def newsdata(request):
#     # newslist = News.objects.all()
#     # return render(request, 'crawlermanage/newsdata.html', {'newslist':newslist})
#     limit = 10  # 每页显示的记录数
#     allnews = News.objects.all()
#     logger.info("allnews:")
#     logger.info(len(allnews))
#     paginator = Paginator(allnews, limit)  # 实例化一个分页对象
#
#     page = request.GET.get('page')  # 获取页码
#     try:
#         newslist = paginator.page(page)  # 获取某页对应的记录
#     except PageNotAnInteger:  # 如果页码不是个整数
#         newslist = paginator.page(1)  # 取第一页的记录
#     except EmptyPage:  # 如果页码太大，没有相应的记录
#         newslist = paginator.page(paginator.num_pages)  # 取最后一页的记录
#     logger.info("newslist:")
#     logger.info(len(newslist))
#     return render(request, 'crawlermanage/newsdata.html', {'newslist': newslist})

def newsdata(request):
    id = request.GET.get('id')
    if id == None:
        id = 1
    p = paging(News,id,5)
    return render(request,'crawlermanage/newsdata.html',locals())

def newsdetail(request):
    id = request.GET.get('id')
    if id==None:
        return
    news = News.objects.get(id=id)
    if news == None:
        return
    return render(request, 'crawlermanage/newsdetail.html', {'news':news})

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
            list_url = starturls.split('\n')
            task = Task.objects.create(taskname=taskname, starturls=list_url, status=status, webtype=webtype, runmodel=runmodel)

            subprocess.Popen("python main.py", cwd=r"/home/kui/work/python/project/bigcrawler/", shell=True)

            return HttpResponseRedirect('/crawlermanage/tasks')
    else:
        return render_to_response('crawlermanage/layout.html')

