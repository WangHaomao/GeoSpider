# -*- encoding: utf-8 -*-
import json
import logging
import time

from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response

from crawlermanage.models import Task, News
from crawlermanage.utils.acticle_parser import extract
from crawlermanage.utils.message import Message
from crawlermanage.utils.page import paging
from crawlermanage.utils.settings_helper import get_attr

logger = logging.getLogger('crawlermanage.views')
# mongoengine.register_connection('default', 'p')

# Create your views here.
redis_host = get_attr('REDIS_HOST')
sub = get_attr('SUBSCRIBE')
messager = Message(redis_host)
messager.subscribe(sub)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


'''
    登录
'''


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
            if username == 'admin' and password == 'a':
                # request.session['username'] = username
                return HttpResponseRedirect('/crawlermanage/index')
            else:
                return render_to_response('crawlermanage/login.html', {'error': '用户名或密码错误'})

    else:
        return render_to_response('crawlermanage/login.html')


def index(request):
    return render(request, 'crawlermanage/index.html')


'''
    爬虫任务列表
    p:正在进行、等待运行、出现故障的任务
    p2:结束的任务
'''


def tasks(request):
    page = request.GET.get('page')
    page2 = request.GET.get('page2')
    if page == None:
        page = 1
    if page2 == None:
        page2 = 1

    list = Task.objects.filter(status__in=['running', 'waitting', 'error', 'pausing'])
    list2 = Task.objects.filter(status='stopping')
    p = paging(list, page, 10)
    p2 = paging(list2, page2, 10)
    return render(request, 'crawlermanage/tasks.html', {'p': p, 'p2': p2})


'''
    编辑爬虫状态：暂停/唤醒/结束
'''


def edittask(request):
    if request.method == 'POST':
        op = request.POST.get('op')
        taskid = request.POST.get('taskid')
        task = Task.objects.filter(id=taskid)
        logger.info(task)
        if op == 'running':
            task.update(status='running')
            msg = 'op=resumetask&taskid=' + taskid
            messager.publish('crawler', msg)
            ret = {'status': 'success', 'taskstatus': 'running'}
            return HttpResponse(json.dumps(ret))
        elif op == 'pausing':
            task.update(status='pausing')
            msg = 'op=suspendtask&taskid=' + taskid
            messager.publish('crawler', msg)
            ret = {'status': 'success', 'taskstatus': 'pausing'}
            return HttpResponse(json.dumps(ret))
        elif op == 'stopping':
            task.update(status='stopping')
            msg = 'op=terminatetask&taskid=' + taskid
            messager.publish('crawler', msg)
            ret = {'status': 'success', 'taskstatus': 'stopping'}
            return HttpResponse(json.dumps(ret))


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

'''
    新闻列表
'''


def newsdata(request):
    taskid = request.GET.get('taskid')
    list = []
    if taskid != None:
        list = News.objects.filter(taskid=taskid)
    page = request.GET.get('page')
    if page == None:
        page = 1
    p = paging(list, page, 10)
    return render(request, 'crawlermanage/newsdata.html', locals())


'''
    新闻详细内容
'''


def newsdetail(request):
    id = request.GET.get('id')
    if id == None:
        return
    news = News.objects.get(id=id)
    if news == None:
        return
    return render(request, 'crawlermanage/newsdetail.html', {'news': news})


'''
    布置爬虫任务
'''


def layout(request):
    # taskname:taskname,
    # starturls:starturls,
    # describe:describe,
    # webtype:webtype,
    # reservationtime:reservationtime,
    # slave:slave
    if request.method == 'POST':
        taskname = request.POST.get('taskname', '')
        starturls = request.POST.get('starturls', '')
        describe = request.POST.get('describe', '')
        webtype = request.POST.get('webtype', '')
        reservationtime = request.POST.get('reservationtime', '')
        slave = request.POST.get('slave', '')
        # logger.info(taskname+" "+starturls+" "+describe+" "+webtype+" "+reservationtime+" "+slave)
        list_url = starturls.split(',')
        # status = ''
        starttime = ''
        endtime = ''
        if reservationtime == '':
            starttime = time.strftime("%Y/%m/%d %H:%M")
            status = 'running'
        else:
            temp = reservationtime.split('-')
            starttime = temp[0].strip()
            endtime = temp[1].strip()
            # logger.info(starttime)
            # logger.info(endtime)
            status = 'waitting'
        slave_list = []
        if slave == '':
            slave = '127.0.0.1'
        slave_list = slave.split(',')
        logger.info(starttime)
        task = Task.objects.create(taskname=taskname, starturls=list_url, starttime=starttime, endtime=endtime,
                                   webtype=webtype, describe=describe, slave=slave_list, status=status)
        taskid = str(task['id'])
        logger.info(status)
        msg = 'op=starttask&taskid=' + taskid + "&status=" + status
        messager.publish('crawler', msg)
        # logger.info(taskid)
        ret = {'status': 'success'}
        return HttpResponse(json.dumps(ret))
    else:
        return render_to_response('crawlermanage/layout.html')


'''
    爬虫任务详情
'''


def taskdetail(request):
    taskid = request.GET.get('taskid')
    logger.info(taskid)

    task = Task.objects.get(id=taskid)
    logger.info(task.status)
    return render_to_response('crawlermanage/taskdetail.html', {'task': task})


'''
    测试正文
'''


def extractarticle(request):
    if request.method == 'POST':
        original_folder = request.POST.get('original_folder', '')
        goal_folder = request.POST.get('goal_folder', '')
        extract(original_folder, goal_folder)
        ret = {'isFinished': 'yes'}
        return HttpResponse(json.dumps(ret))
    else:
        return render_to_response('crawlermanage/extract_article.html')


def testarticles(request):
    if request.method == 'POST':
        original_folder = request.POST.get('original_folder', '')
        goal_folder = request.POST.get('goal_folder', '')
        # test(original_folder, goal_folder)
        ret = {'isFinished': 'yes'}
        return HttpResponse(json.dumps(ret))
    else:
        return render_to_response('crawlermanage/test_articles.html')


'''
    测试结果
'''


def testlist(request):
    return render_to_response('crawlermanage/test_list.html')
