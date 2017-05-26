# -*-encoding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
from lxml import etree
from selenium import webdriver
from e_commerce_site_crawler.ecommerce.spiderUtils.parser_util import get_soup_by_request,get_soup_by_selenium
import sys
from lxml.html import fromstring
reload(sys)
sys.setdefaultencoding('utf8')


def _get_price_by_class(soup,class_name):
    res_price_list = []
    reg_without_keyword = u"(\d+\.*\d*-*)+"

    tag_symbol_list = soup.find_all(True, class_=re.compile(class_name))
    for tag in tag_symbol_list:
        tag_tmp = tag
        price_text_list = []
        attemps = 0
        while (len(price_text_list) == 0 and attemps < 2):
            price_text_list = re.findall(reg_without_keyword, tag_tmp.text)
            tag_tmp = tag_tmp.parent
            attemps += 1

        print res_price_list
        if (len(price_text_list) != 0):
            res_price_list = res_price_list + price_text_list

    return res_price_list

def _get_price_by_keyword(soup,keyword):
    res_price_list = []
    reg_with_keyword = u"%s(\s*\d+\.*\d*-*)+"%keyword
    reg_without_keyword = u"(\d+\.*\d*-*)+" #从带有关键字的字符串中提取价格（数字），例如促销价 100,则提取出100

    tag_symbol_list = soup.find_all(True, text=re.compile(keyword))
    for tag in tag_symbol_list:
        tag_tmp= tag
        price_text_list = []
        attemps = 0
        while(len(price_text_list) ==0 and attemps < 2):
            price_text_list = re.findall(reg_with_keyword,tag_tmp.text)
            tag_tmp = tag_tmp.parent
            attemps += 1

        print res_price_list
        if(len(price_text_list)!=0):
            res_price_list  = res_price_list + re.findall(reg_without_keyword,"".join(price_text_list))

    return res_price_list

def get_price(soup,url):
    res_price_list = _get_price_by_keyword(soup,u"¥")
    if(len(res_price_list) !=0 ):
        return res_price_list

    res_price_list = _get_price_by_class(soup,"price")
    if (len(res_price_list) != 0):
        return res_price_list

    res_price_list = _get_price_by_keyword(soup, u"促销价")
    if (len(res_price_list) != 0):
        return res_price_list

    res_price_list = _get_price_by_keyword(soup, u"价格")
    if (len(res_price_list) != 0):
        return res_price_list

    res_price_list = _get_price_by_keyword(soup, u"价")
    return res_price_list


# def _get_comments_by_keyword(soup,keyword):


def get_comments(url):
    driver = webdriver.PhantomJS()
    driver.get(url)


    # req = requests.get(url)
    # req.encoding = "utf-8"
    # doc = etree.HTML(driver.page_source)
    key = u"评论"
    # print  doc.xpath("//*[text()='%s']"%(key))

    driver = webdriver.PhantomJS()
    driver.get(url)

    tree = fromstring(driver.page_source)
    xxx = tree.xpath('//*[re:test(text(), "%s")]' % key, namespaces={'re': "http://exslt.org/regular-expressions"})
    print  xxx[0].text
    print  xxx[0].tag

    # print driver.page_source
    # xx = driver.findElement(By.xpath("/html/body/div/input[@value='查询']"))
    xx = driver.find_element_by_xpath('//*[re:test(text(), "%s")]' % key, namespaces={'re': "http://exslt.org/regular-expressions"})
    print len(xx)



    driver.close()



def shopping_item_parser(url):

    # soup = get_soup_by_request(url)
    soup = get_soup_by_selenium(url)
    # [script.extract() for script in soup.findAll('script')]
    # print soup.prettify()
    # 价格
    get_price(soup,url)



if __name__ == '__main__':
    # url = "https://detail.tmall.com/item.htm?spm=a230r.1.14.14.AT6RIa&id=544429684821&cm_id=140105335569ed55e27b&abbucket=20"
    # url = "https://item.taobao.com/item.htm?spm=a230r.1.14.97.oI9e6K&id=545728190154&ns=1&abbucket=20#detail"
    url = "https://item.jd.com/11225370508.html"
    # url = "http://item.meilishuo.com/detail/1kaosga?acm=3.ms.2_4_1kaosga.0.24476-25176.94mOaqibAUDJd.t_0-lc_3&ptp=1.9Hyayb.classsearch_mls_1kaosga_2017%E6%96%B0%E6%AC%BE%E6%AC%A2%E4%B9%90%E9%A2%82%E7%8E%8B%E5%AD%90%E6%96%87%E6%9B%B2%E7%AD%B1%E7%BB%A1%E5%90%8C%E6%AC%BE%E5%8C%85%E6%97%B6%E5%B0%9A%E5%B0%8F%E6%96%B9%E5%8C%85%E5%8D%95%E8%82%A9%E6%96%9C%E6%8C%8E%E5%B0%8F%E5%8C%85%E5%8C%85_10057053_pop.1.mNWwi"
    # shopping_item_parser(url)



    get_comments(url)