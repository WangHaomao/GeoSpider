#coding:utf-8

import re
# class URLUtils:
    # def __init__(self):
    #     pass

#通过上下文信息，拼接一些非法的url,例如//xxx.com等等
# "xxxx"
def url_sifter(parent_url, url):
    # print parent_url
    # print url
    if url is None or len(url) == 0:
        return None

    cu_url = str(url)
    cuURL_len = len(cu_url)
    pa_url = str(parent_url)
    paURL_len = len(pa_url)
    #  去除双引号
    cu_url   = cu_url.replace('"',"")
    #  去掉开头的／或//
    if (cu_url.startswith("/")):
        if (cu_url.startswith("//")):
            index = 2
            for ind in range(2, cuURL_len):
                if (cu_url[ind] is not '/'):
                    index = ind
                    break

            cu_url = cu_url[index:cuURL_len]
        else:
            cu_url = cu_url[1:cuURL_len]

    pa_part = pa_url.split('.')
    part_len = len(pa_part)
    domain = ""
    if part_len == 2:
        domain = pa_part[0]
    elif part_len == 3:
        domain = pa_part[1]

    if domain not in cu_url:
        cu_url = pa_url + ('' if pa_url[paURL_len - 1] == '/' else '/') + cu_url

    if "https://" not in cu_url and "http://" not in cu_url:
        http_str_header = pa_url.split("//")
        cu_url = http_str_header[0] + "//" + cu_url

    return cu_url

def get_url_domain(url):
    res_url = re.search("\.[0-9a-zA-Z]{2,14}\.(com.cn|com|cn|net|org|wang|cc)",url).group()
    return res_url[1:]
# 截取前一段url
def get_partial_url(url):
    res_url = re.search(".+\.(com.cn|com|cn|net|org|wang|cc)", url).group()
    return res_url

if __name__ == '__main__':
    print (url_sifter("https://www.taobao.com/","//www.taobao.com/tbhome/page/market-list"))
    print (get_partial_url("https://news.qq.com/"))
    str = "https://news.qq.com"
    print(str.split('/')[2])