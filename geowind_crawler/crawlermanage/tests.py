# -*- encoding: utf-8 -*-
import csv

import mongoengine
from django.test import TestCase

# Create your tests here.
from crawlermanage.models import News, Process
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
mongoengine.register_connection('default', 'geospider')
def export_csvfile(output_path):
    list = News.objects.all()
    with open(output_path, 'wb') as f:
        writer = csv.writer(f)
        for i in list:
            print(i['url'], i['title'], i['time'], i['keywords'], i['article'])
            writer.writerows([i['url'], i['title'], i['time'], i['keywords'], i['article']])

def WriteTvsPlsttoCsv(csvFile):
    headList =['url', 'title', 'time', 'keywords','article']
    with open(csvFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(headList)
        # headList[0]='_id'
        list = News.objects.all()
        for u in list:
            vList = []
            for k in headList:
                vList.append(u[k].encode('utf8'))
            writer.writerow(vList)

if __name__ == '__main__':
    #export_csvfile(u'/home/kui/桌面/a.csv')
    WriteTvsPlsttoCsv(u'/home/kui/桌面/d.csv')