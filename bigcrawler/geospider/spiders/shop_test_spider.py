# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.http import request
from bs4 import BeautifulSoup
from geospider.items import ECommerceSiteCrawlerItem

from geospider.ecommerce.pageParser.shopping_navigation_parser import get_nav
from geospider.ecommerce.pageParser.selenium_batch_parser import \
    get_pageKeyDic,get_next_urlList_by_firstpage_url,get_all_page_number,get_all_page_urls
from geospider.ecommerce.spiderUtils.parser_util import get_html_with_request
from urllib2 import quote,unquote
import time

"""
1、获取网站首页的导航栏 关键字：url
2、判断是否存在 关键字 in url
如果 关键字 in url:
    那么解析出翻页
        

"""

if __name__ == '__main__':

    # url = 'https://www.taobao.com/'
    # url = 'https://www.tmall.com/'
    # 当当
    # url = "http://www.dangdang.com/"
    # 唯品会
    # url = "http://www.vip.com/"
    # 凡客诚品
    # url = "http://www.vancl.com/"
    # 一号店
    # url = "http://www.yhd.com/"
    # 亚马逊
    # url = "https://www.amazon.cn/"
    # 美丽说
    url = "http://www.meilishuo.com/"
    # url = 'http://www.mogujie.com'
    # url = "https://www.jd.com/"

    number, mylist = get_nav(url,0)
    searchKeywordValue = None
    page_list = []
    pageKeyDic = {}

    # 第一遍遍历
    goal_url = ""
    goal_key = ""
    goal_url_len = -1
    all_meets_url_number = 0 #统计有多少个关键字在url中
    for tlist in mylist:
        # pass
        o_url = tlist[1]
        o_key = tlist[0]
        if ((o_key != None and o_url != None and o_key in o_url)
            and ("search" in o_url or 'list' in o_url)):
            if goal_url_len == -1 or len(tlist[1]) < goal_url_len:
                goal_url = tlist[1]
                goal_key = tlist[0]
                goal_url_len = len(tlist[1])

            all_meets_url_number+=1
    print goal_url

    res_url_list = []
    if(goal_url_len != -1):
        print '----------------------------------方法一'
        """
            对url进行一遍简化
        """
        goal_url_spilted = goal_url.split('&')
        key_index = 0
        simple_url = ""
        print goal_url_spilted
        while key_index < len(goal_url_spilted):
            if(goal_key in goal_url_spilted[key_index]):
                # [:]左闭右开
                simple_url = ('&'.join(goal_url_spilted[:key_index+1]))

                key_index += 1
                break
            key_index+=1
        # print goal_url
        original_html_len = len(get_html_with_request(goal_url))

        while (key_index<len(goal_url_spilted)):
            if (original_html_len <= len(get_html_with_request(simple_url))):
                break
            simple_url = simple_url + "&" + goal_url_spilted[key_index]
            key_index+=1
        for tlist in mylist:
            if tlist[0] != None and tlist[0] != '':
                searchKeywordValue = quote(tlist[0].encode('utf8'))
                item_list_url = simple_url.replace(goal_key, searchKeywordValue)
                # print item_list_url
                res_url_list.append(item_list_url)
    else:
        # 假设所有url类型都相同，且默认为商品列表页面，进行解析
        print '----------------------------------方法二'
        for tlist in mylist:
            print tlist[1]
            if (tlist[1]!= None and tlist[1]!='' and ('list' in tlist[1] or 'search' in tlist[1] or 'category' in tlist[1])):
                res_url_list.append(tlist[1])
        print len(res_url_list)




    if(len(res_url_list)>1):
        print '#########################################'
        pageDict = None
        # test_url = res_url_list[0]
        demo_url = None

        for test_url in res_url_list:

            page_list = get_next_urlList_by_firstpage_url(test_url)
            # print 'url = %s' % test_url
            print page_list
            if(page_list == None):continue

            pageDict = get_pageKeyDic(page_list)

            if(pageDict == None or len(pageDict)==0):continue

            demo_url = test_url
            break

        if(pageDict == None or page_list == None):
            raise Exception("页面解析异常")

        print pageDict

        print page_list

        attached_1 = page_list[1].replace(demo_url, '')
        attached_2 = page_list[2].replace(demo_url, '')


        print attached_1

        for goods_list_url in res_url_list:
            next_url1 =  goods_list_url + attached_1
            next_url2 =  goods_list_url + attached_2

            print next_url2
            allnumber = get_all_page_number(goods_list_url)
            print allnumber
            # next_all_url_list = get_all_page_urls(pageKeyDic,page_list,allnumber)

            res = get_all_page_urls(pageDict, [goods_list_url,next_url1,next_url2],
                                    allnumber)
            for x in res:
                print str(x)
            print "----------$$$$$$$$$------------"
