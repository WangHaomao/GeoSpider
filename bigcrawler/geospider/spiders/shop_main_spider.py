# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider

from geospider.ecommerce.spiderUtils.parser_util import get_html_with_request
from geospider.ecommerce.pageParser.shopping_itemsList_parser import analysis_method_selector, analysis_goods_list
from geospider.ecommerce.pageParser.shopping_navigation_parser import get_nav
from geospider.ecommerce.pageParser.selenium_batch_parser import \
    get_pageKeyDic, get_next_urlList_by_firstpage_url, get_all_page_number, get_all_page_urls
from geospider.ecommerce.pageParser.shopping_detail_parser import *
from urllib2 import quote, unquote
from geospider.items import Goods,Stores,Ecommerce

class ShopMainSpider(RedisSpider):
    name = "shopspider"
    # allowed_domains = ["https://www.baidu.com"]

    redis_key = 'ecommerce:start_urls'

    start_urls = [
        'https://www.taobao.com/',
        # "http://www.dangdang.com/",
        # "http://www.vip.com/",
        # "http://www.vancl.com/",
        # "http://www.yhd.com/",
        # "https://www.amazon.cn/",
        # "http://www.meilishuo.com/",
    ]

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        print("***********************************************************8")
        #self.allowed_domains = filter(None, domain.split(','))
        # db = connect_mongodb()
        # self.urldao = URLDao(db)
        # self.taskid = self.redis_key.split(':')[0]
        super(ShopMainSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        number, mylist = get_nav(response.url, 0)
        searchKeywordValue = None
        page_list = []
        pageKeyDic = {}

        # 第一遍遍历
        goal_url = ""
        goal_key = ""
        goal_url_len = -1
        all_meets_url_number = 0  # 统计有多少个关键字在url中
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

                all_meets_url_number += 1
        print goal_url

        res_url_list = []
        if (goal_url_len != -1):
            """
                对url进行一遍简化
            """
            goal_url_spilted = goal_url.split('&')
            key_index = 0
            simple_url = ""
            # print goal_url_spilted
            while key_index < len(goal_url_spilted):
                if (goal_key in goal_url_spilted[key_index]):
                    # [:]左闭右开
                    simple_url = ('&'.join(goal_url_spilted[:key_index + 1]))

                    key_index += 1
                    break
                key_index += 1
            # print goal_url
            original_html_len = len(get_html_with_request(goal_url))

            while (key_index < len(goal_url_spilted)):
                if (original_html_len <= len(get_html_with_request(simple_url))):
                    break
                simple_url = simple_url + "&" + goal_url_spilted[key_index]
                key_index += 1
            for tlist in mylist:
                if tlist[0] != None and tlist[0] != '':
                    searchKeywordValue = quote(tlist[0].encode('utf8'))
                    item_list_url = simple_url.replace(goal_key, searchKeywordValue)
                    # print item_list_url
                    res_url_list.append(item_list_url)
        else:
            # 假设所有url类型都相同，且默认为商品列表页面，进行解析
            for tlist in mylist:
                # print item_list_url
                if (tlist[1] != None and tlist[1] != '' and (
                            'list' in tlist[1] or 'search' in tlist[1] or 'category' in tlist[1])):
                    res_url_list.append(tlist[1])

        if (len(res_url_list) > 1):

            pageDict = None
            # test_url = res_url_list[0]
            demo_url = None
            for test_url in res_url_list:

                page_list = get_next_urlList_by_firstpage_url(test_url)

                if (page_list == None): continue

                pageDict = get_pageKeyDic(page_list)

                if (pageDict == None or len(pageDict) == 0): continue

                demo_url = test_url
                break

            if (pageDict == None or page_list == None):
                raise Exception("页面解析异常")

            print pageDict

            print page_list

            attached_1 = page_list[1].replace(demo_url, '')
            attached_2 = page_list[2].replace(demo_url, '')

            for goods_list_url in res_url_list:
                next_url1 = goods_list_url + attached_1
                next_url2 = goods_list_url + attached_2

                # print next_url2
                allnumber = get_all_page_number(goods_list_url)
                print allnumber
                # next_all_url_list = get_all_page_urls(pageKeyDic,page_list,allnumber)

                res = get_all_page_urls(pageDict, [goods_list_url, next_url1, next_url2],
                                        allnumber)
                """
                每一个商品列表的分页信息

                """
                for each_goods_list_url in res:
                    yield Request(callback=self.goods_list_parse, url=each_goods_list_url)


                    # print "----------$$$$$$$$$------------"


    def goods_list_parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        analysis_method = analysis_method_selector(soup)

        analysis_res = analysis_goods_list(analysis_method, response.url, soup)


        if(analysis_method == 'JSON'):
            for each_item in analysis_res:
                each_detail_url = each_item['detail_url']
                item = Goods()

                item['title'] = each_item['title']
                item['price'] = each_item['price']
                item['pic_url'] = each_item['pic_url']
                item['detail_url'] = each_item['detail_url']
                item['taskid'] = str(self.name)

                # yield item

                yield Request(callback=self.goods_detail_parse, url=each_detail_url, meta={'method': 'JSON','item':item},)

        else:
            try:
                for each_detail_url in analysis_res:
                    yield Request(callback=self.goods_detail_parse, url=each_detail_url, meta={'method': 'OTHER'})
            except:
                pass



    def goods_detail_parse(self, response):
        method =  response.meta['method']
        item = response.meta['item']
        print '------------------------------------------------------------------------------'
        soup = BeautifulSoup(response.url,'lxml')
        res_stroe_dic = get_store(soup, response.url)

        item['comment_degree'] = res_stroe_dic['comment_degree']

        if(method != 'JSON'):
            item['price'] = get_price(soup)
            item['detail_url'] = response.url

            # yield item

        store_item = Stores()
        store_item['name'] = res_stroe_dic['name']
        store_item['store_url'] = res_stroe_dic['store_url']
        store_item['comment_degree'] = res_stroe_dic['comment_degree']
        store_item['taskid'] = str(self.name)

        # yield store_item
        res_item = Ecommerce()
        res_item['goods'] = item
        res_item['stores'] = store_item


        yield res_item
        # soup = BeautifulSoup(response.text, 'lxml')
        # print  get_title(soup)
        # item = ECommerceSiteCrawlerItem()
        #
        # item['price'] = get_price(soup)
        # item['title'] = get_title(soup)
        # item['stroe_url'] = get_store(soup, response.url)
        # # item['pic_url'] =


    def stroe_detail_parse(self, respinse):
        pass