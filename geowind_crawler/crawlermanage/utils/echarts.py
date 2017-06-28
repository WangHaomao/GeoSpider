# -*- encoding: utf-8 -*-
import mongoengine

from crawlermanage.models import Task
'''
    创建当前任务状态表，返回4个数组
    运行[新闻，博客，电商]
    暂停[...]
    等待[...]
    故障[...]
'''

# mongoengine.register_connection('default', 'geospider')

def create_chart1():
    run_news = Task.objects.filter(webtype='news', status='running').count()
    run_blog = Task.objects.filter(webtype='blog', status='running').count()
    run_ecommerce = Task.objects.filter(webtype='ecommerce', status='running').count()
    pause_new = Task.objects.filter(webtype='news', status='pausing').count()
    pause_blog = Task.objects.filter(webtype='blog', status='pausing').count()
    pause_ecommerce = Task.objects.filter(webtype='ecommerce', status='pausing').count()
    wait_news = Task.objects.filter(webtype='news', status='waitting').count()
    wait_blog = Task.objects.filter(webtype='blog', status='waitting').count()
    wait_ecommerce = Task.objects.filter(webtype='ecommerce', status='waitting').count()
    error_news = Task.objects.filter(webtype='news', status='error').count()
    error_blog = Task.objects.filter(webtype='blog', status='error').count()
    error_ecommerce = Task.objects.filter(webtype='ecommerce', status='error').count()
    run = [run_news, run_blog, run_ecommerce]
    pause = [pause_new, pause_blog, pause_ecommerce]
    wait = [wait_news, wait_blog, wait_ecommerce]
    error = [error_news, error_blog, error_ecommerce]
    return run, pause, wait, error

'''
    历史任务：各类型爬虫任务所占比例
    return：停止的电商任务个数，停止的新闻任务个数，停止的博客任务个数
'''
def create_chart2():
    ecommerce = Task.objects.filter(webtype='ecommerce', status='stopping').count()
    news = Task.objects.filter(webtype='news', status='stopping').count()
    blog = Task.objects.filter(webtype='blog', status='stopping').count()
    return ecommerce, news, blog

