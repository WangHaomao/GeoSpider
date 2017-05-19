import logging
from proxy.proxy_util import get_ips

http, https = get_ips()

class ProxyMiddleware(object):
    http_n = 0
    https_n = 0

    def process_request(self, request, spider):
        if request.url.startswith("http://"):
            n = ProxyMiddleware.http_n
            n = n if n<len(http) else 0
            request.meta['proxy'] = "http://%s:%d" %(http[n].ip) %(int(http[n].port))
            logging.INFO('Squence - http:%s - %s' %(n, str(http[n])))
            ProxyMiddleware.http_n = n+1
        if request.url.startswith("https://"):
            n = ProxyMiddleware.http_n
            n = n if n<len(https) else 0
            request.meta['proxy'] = "https://%s:%d" %(http[n].ip) %(int(http[n].port))
            logging.INFO('Squence - https:%s - %s' %(n, str(http[n])))
            ProxyMiddleware.https_n = n+1


