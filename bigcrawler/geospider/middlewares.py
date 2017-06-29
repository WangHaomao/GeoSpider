#-*- coding:utf-8 -*-


import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware
from scrapy import log

class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        #print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))

import json
class ProxyMiddleWare(HttpProxyMiddleware):

    ip_pool = []
    def __init__(self,ip=''):
        self.ip = ip
        json_s = '{"ERRORCODE":"0","RESULT":[{"port":"44306","ip":"171.13.36.228"},{"port":"20975","ip":"117.94.204.25"},{"port":"33779","ip":"182.42.44.155"},{"port":"33902","ip":"113.101.137.102"},{"port":"39143","ip":"114.230.127.62"},{"port":"38965","ip":"114.239.3.155"},{"port":"46996","ip":"123.161.154.64"},{"port":"45700","ip":"120.33.247.82"},{"port":"43573","ip":"113.121.41.165"},{"port":"21527","ip":"122.242.92.6"},{"port":"46535","ip":"49.79.58.186"},{"port":"48241","ip":"113.121.47.91"},{"port":"48750","ip":"27.154.183.45"},{"port":"26306","ip":"182.34.20.19"},{"port":"35181","ip":"223.242.177.44"},{"port":"35052","ip":"114.225.84.235"},{"port":"33385","ip":"117.86.20.26"},{"port":"38541","ip":"49.84.70.182"},{"port":"21002","ip":"114.239.1.18"},{"port":"40891","ip":"117.94.207.140"}]}'
        json_parser = json.loads(json_s)
        for ip_dic in json_parser["RESULT"]:
            self.ip_pool.append(ip_dic["ip"] + ":" + ip_dic["port"])

    def process_request(self, request, spider):
        thisip = random.choice(self.ip_pool)

        try:
            request.meta["proxy"] = "http://%s" % thisip

            print "current_ip = %s" % request.meta["proxy"]
        except  Exception as e:
            pass

class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            # 显示当前使用的useragent
            # print ("********Current UserAgent:%s************" % ua)

            # 记录
            log.msg('Current UserAgent: ' + ua, level=log.INFO)
            request.headers.setdefault('User-Agent', ua)

            # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape

    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]