#-*-coding:utf-8 -*-
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from gevent import monkey; monkey.patch_socket()
import gevent
from time import ctime
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree
from e_commerce_site_crawler.ecommerce.spiderUtils.parser_util import get_soup_by_html_source
import re
import time
import logging

"""
1、商品列表页面
"""

# 不需要了，直接replace url中的关键字即可
def get_keyword_methond(url,keyword):
    pass


def get_next_url_by_number123(driver):

    element_1_list = driver.find_elements_by_xpath("//*[text()='1']" )
    elsment_2 =  ""
    for elem in element_1_list:
        print elem.tag_name


def get_next_page_element(driver):
    next_str = u"下一页"
    # element = driver.find_element_by_xpath("//*[text()='%s']"%next_str)
    # contains
    element = driver.find_element_by_xpath("//*[contains(text(),'%s')]" % next_str)
    # element = driver.find_element_by_partial_link_text(next_str)
    element_tag_name =  element.tag_name

    if(element_tag_name!="button" and element_tag_name!="a"):
        # 暂时只找一层父节点
        element = element.find_element_by_xpath("..")

    # print element.text
    element.click()
    return driver.current_url

    # return element

page_url_dic = {}

#[domain.com,domain.cn,domain.net....]
def get_url_domain(url):
    # res_url = re.findall("\..+\.com|\..+\.cn",url)
    res_url = re.findall("\.[0-9a-zA-Z]{2,14}\.com|\.[0-9a-zA-Z]{2,14}\.cn",url)
    return res_url[0]

"""
xpath 获取的数据，由于attributes不能获得名字，换用beautifulsoup
# doc = etree.HTML(driver.page_source)
        # is_find_page3_url = False
        # #当前是第一页，寻找分页中的第二页，通过第二页找到第三页的URL
        # element_2_list = doc.xpath("//a[text()='2']")
        # number_to_url_dic = {}
        # for elem in element_2_list:
        #     find_parent_times = 0
        #     xpath_path_string = ""
        #     while(find_parent_times < 4):
        #         if(find_parent_times == 0):
        #             xpath_path_string = "../a"
        #         elif(find_parent_times == 1):
        #             xpath_path_string = "..//a"
        #         else:
        #             xpath_path_string = "../" + xpath_path_string
        # 
        #         if (len(elem.xpath(xpath_path_string)) >= 3):
        #             for tmp_elem in elem.xpath(xpath_path_string):
        #                 if (tmp_elem.text == "3"):
        #                     # print tmp_elem.xpath("./@href")
        #                     number_to_url_dic['2'] = elem.xpath("./@href")[0]
        #                     number_to_url_dic['3'] = tmp_elem.xpath("./@href")[0]
        #                     print elem.xpath("./attribute::node()")
        #                     print tmp_elem.xpath("./attribute::node()")
        #                     is_find_page3_url = True
        #                     break
        # 
        #         find_parent_times += 1
        # 
        #     if is_find_page3_url :
        #         break
        # 
        # print url
"""


def get_url_by_attrs_dic(driver,attrs_dic):

    find_element_key_list = ['a']
    for key, value in attrs_dic.items():
        if isinstance(value, list):
            continue
        else:
            find_element_key_list.append("[%s='%s']" % (key, value))

    # print "------1------" + ''.join(find_element_key_list)
    elem = driver.find_element_by_css_selector(''.join(find_element_key_list))
    elem.click()
    time.sleep(5)
    return driver.current_url


#支持同时给多个网站,url_list:多个网站的商品列表页url
def get_next_page_url_by_url_list(url_list):
    driver = webdriver.PhantomJS()
    url_number = len(url_list)
    index = 0
    attemps = 0
    ATTEMPS_TIMES = 3 #失败尝试3次
    FAILUED_STRING = "FAILUED_STRING"
    while(index < url_number):
        url = url_list[index]
        driver.get(url)
        soup = get_soup_by_html_source(driver.page_source)
        is_find_page3_url = False
        #当前是第一页，寻找分页中的第二页，通过第二页找到第三页的URL
        element_2_list = soup.find_all("a",text="2")
        number_to_url_dic = {}
        for elem in element_2_list:
            find_parent_times = 0
            while(find_parent_times < 4):
                # descendants_list = []
                if(find_parent_times == 0):
                    elem_parent = elem.parent
                    descendants_list = elem_parent.contents
                elif(find_parent_times == 1):
                    elem_parent = elem.parent
                    descendants_list = elem_parent.descendants
                else:
                    elem_ancestor = elem
                    for up_times in xrange(0,find_parent_times):
                        elem_ancestor = elem_ancestor.parent

                    descendants_list = elem_ancestor.descendants

                for descendant in descendants_list:
                    if (descendant.name != None and descendant.name == 'a'):
                        if descendant.text == '3':
                            number_to_url_dic['2'] = elem.get("href")
                            number_to_url_dic['3'] = descendant.get("href")
                            number_to_url_dic['attrs_dic2'] = elem.attrs
                            number_to_url_dic['attrs_dic3'] = descendant.attrs
                            # print elem.attrs
                            # print descendant.get("href")
                            is_find_page3_url = True
                            break

                find_parent_times += 1

            if is_find_page3_url :
                break
        next_url_is_fake = False
        try:
            url_2 =  number_to_url_dic['2']
            url_3 =  number_to_url_dic['3']
            index += 1
            attemps = 0

            page_url_dic[get_url_domain(url)] = [url,url_2,url_3]

            if(url_2.lower() == url_3.lower()):
                next_url_is_fake = True

        except:
            # print "Failed..."
            attemps += 1
            if(attemps >= ATTEMPS_TIMES):
                page_url_dic[get_url_domain(url)] = [url, FAILUED_STRING, FAILUED_STRING]
                index += 1
                attemps = 0
                logging.warning(url+"分页解析失败！！")

        """
            处理假URL的情况，比如有些URL是#,javascript;这里需要用driver动态跳转，获取current_url
        """
        if(attemps == 0 and next_url_is_fake):

            url_2 = get_url_by_attrs_dic(driver, number_to_url_dic["attrs_dic2"])
            url_3 = get_url_by_attrs_dic(driver, number_to_url_dic["attrs_dic3"])

            page_url_dic[get_url_domain(url)] = [url,url_2,url_3]
            # print number_to_url_dic['2']
            # print number_to_url_dic['3']

    driver.close()

def pages_analysis():
    page_url_dic = {
        "taobao.com":
            [
                "https://s.taobao.com/search?initiative_id=tbindexz_20170509&ie=utf8&spm=a21bo.50862.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E6%89%8B%E6%9C%BA&suggest=0_1&_input_charset=utf-8&wq=shouji&suggest_query=shouji&source=suggest",
                "https://s.taobao.com/search?initiative_id=tbindexz_20170509&ie=utf8&spm=a21bo.50862.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E6%89%8B%E6%9C%BA&suggest=0_1&_input_charset=utf-8&wq=shouji&suggest_query=shouji&source=suggest&p4ppushleft=5%2C48&s=48",
                "https://s.taobao.com/search?initiative_id=tbindexz_20170509&ie=utf8&spm=a21bo.50862.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E6%89%8B%E6%9C%BA&suggest=0_1&_input_charset=utf-8&wq=shouji&suggest_query=shouji&source=suggest&p4ppushleft=5%2C48&s=96"
            ],
        "dangdang.com":
            [
                "http://search.dangdang.com/?key=%CA%E9&act=input",
                "/?key=%CA%E9&act=input&page_index=2",
                "/?key=%CA%E9&act=input&page_index=3",
            ],
        "jd.com":
            [
                "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&suggest=1.his.0.0&wq=&pvid=9e4453eb3e86474c9f0d8ce8719b03aa",
                "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&offset=2&suggest=1.his.0.0&cid2=653&cid3=655&page=3&s=58&click=0",
                "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&offset=2&suggest=1.his.0.0&cid2=653&cid3=655&page=5&s=118&click=0",
            ],
        "jumei.com":
            [
                "http://search.jumei.com/?filter=0-11-1&search=%E9%9D%A2%E8%86%9C&from=search_toplist_%E9%9D%A2%E8%86%9C_word_pos_3&cat=",
                "http://search.jumei.com/?filter=0-11-2&search=%E9%9D%A2%E8%86%9C&bid=4",
                "http://search.jumei.com/?filter=0-11-3&search=%E9%9D%A2%E8%86%9C&bid=4",
            ],
        "tmall.com":
            [
                "https://list.tmall.com/search_product.htm?q=%D2%C1%DC%BD%C0%F6&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&xl=yifu_1&from=mallfp..pc_1_suggest",
                "?brand=115393&s=60&q=%D2%C1%DC%BD%C0%F6&sort=s&style=g&from=mallfp..pc_1_suggest&suggest=0_1&spm=875.7931836/B.a2227oh.d100&type=pc#J_Filter",
                "?brand=115393&s=120&q=%D2%C1%DC%BD%C0%F6&sort=s&style=g&from=mallfp..pc_1_suggest&suggest=0_1&spm=875.7931836/B.a2227oh.d100&type=pc#J_Filter",
            ],
        "meilishuo.com":
            [
                "http://www.meilishuo.com/search/goods/?page=1&searchKey=%E8%A3%99%E5%AD%90%E5%A4%8F&acm=3.mce.1_4_.17721.33742-33692.3Va85qjv0ALoa.mid_17721-lc_201",
                "?acm=3.mce.1_4_.17721.33742-33692.3Va85qjv0ALoa.mid_17721-lc_201&searchKey=%E8%A3%99%E5%AD%90%E5%A4%8F&page=2&cpc_offset=0",
                "?acm=3.mce.1_4_.17721.33742-33692.3Va85qjv0ALoa.mid_17721-lc_201&searchKey=%E8%A3%99%E5%AD%90%E5%A4%8F&page=3&cpc_offset=0",
            ],
        "suning.com":
            [
                "http://search.suning.com/%E6%89%8B%E6%9C%BA/",
                "/%E6%89%8B%E6%9C%BA/&iy=0&cp=1",
                "/%E6%89%8B%E6%9C%BA/&iy=0&cp=2",
            ],
        "mugujie.com":
            [
                "http://list.mogujie.com/s?q=%E8%A1%A3%E6%9C%8D&ptp=1._mf1_1239_15261.0.0.8RN3PL&f=baidusem_4uv5iimn1v",
                "/s?page=2&q=%E8%A1%A3%E6%9C%8D&sort=pop&ppath=#category_all",
                "/s?page=3&q=%E8%A1%A3%E6%9C%8D&sort=pop&ppath=#category_all",
            ],
    }

    domain_to_pageNextDic = {}

    for domain, page_urls  in page_url_dic.items():
        url_numbers = len(page_urls)
        url_2 = page_urls[1]
        url_3 = page_urls[2]
        # 获取倒数第二个元素
        url_2_pieces = str(url_2).split("?")[-1].split("&")
        url_3_pieces = str(url_3).split("?")[-1].split("&")
        pieces_2_len = len(url_2_pieces)
        pieces_3_len = len(url_3_pieces)

        NextDic = {}
        if pieces_2_len != pieces_3_len:
            raise Exception("解析分页URL碎片时，第二页和第一页URL参数不相等")

        for pieces_index in xrange(0,pieces_3_len):
            pieces_2_splited = url_2_pieces[pieces_index].split("=")
            pieces_3_splited = url_3_pieces[pieces_index].split("=")

            """将page=1这类字符串分割为[page,1],判断第二个值的差，拼接url
                -1是取倒数第一个，当出现只有值不是=分割时，用这种方式比较方便
                存储方式:
                domain.com:{
                                name1:[1(原值，即第二页的值),1(dx,差值)],
                                name2:[0-11-2(原值，即第二页的值),{2:1(dx,差值)}]
                            }
                            
                name2比较特殊，在拥有特殊字符的串中，将0-11-2分割，第2个数字有差值(从0开始)
                
            """

            if(len(pieces_2_splited) == 2 and pieces_2_splited[-1]!=pieces_3_splited[-1]):
                # for xx in pieces_3_splited[-1]:
                #     print xx
                value2 = pieces_2_splited[-1]
                value3 = pieces_3_splited[-1]
                # print "%s=%s" % (pieces_2_splited[0], pieces_2_splited[1])
                if(value2.isdigit()):
                    dx =  int(value3) - int(value2)
                    NextDic[pieces_2_splited[0]] = [pieces_2_splited[1],dx]


                else:
                    value_str_len = min(len(value2),len(value3))
                    value2_list = list(value2)
                    value3_list = list(value3)
                    for ch_index in xrange(0,value_str_len):
                        if(value2[ch_index].isdigit() is False):
                            value2_list[ch_index] = " "
                        if (value3[ch_index].isdigit() is False):
                            value3_list[ch_index] = " "
                    value2 = "".join(value2_list).split(" ")
                    value3 = "".join(value3_list).split(" ")


                    num_len = len(value2)
                    page_index_to_dx = {}
                    for num_index in xrange(0,num_len):
                        if(value2[num_index] != value3[num_index]):
                            page_index_to_dx[num_index] =  int(value3[num_index]) - int(value2[num_index])

                    NextDic[pieces_2_splited[0]] = [pieces_2_splited[-1],page_index_to_dx]

                # print "%s,%s"%(pieces_2_splited[-1],pieces_3_splited[-1])

        domain_to_pageNextDic[domain] = NextDic
        # print NextDic


    for domain, page_urls in page_url_dic.items():
        url_0 = page_urls[0]
        print url_0
        url = page_urls[1]
        url_nextDic = domain_to_pageNextDic[domain]
        # print url
        previous_attrs_value_dict = {}

        for i in xrange(0, 20):
            current_url = url
            for key, value in url_nextDic.items():
                if isinstance(value[1], dict) is True:
                    value0_list = list(value[0])
                    value0_list_len  = len(value0_list)
                    ch = " "
                    for ch_index in xrange(0,value0_list_len):
                        if(value0_list[ch_index].isdigit() is False):
                            ch = value0_list[ch_index]
                            value0_list[ch_index] = " "


                    value0_list_splited = "".join(value0_list).split(" ")
                    value0_list_len = len(value0_list_splited)
                    for index in xrange(0,value0_list_len):
                        if(value[1].has_key(index)):
                            # print "???"
                            if(i == 0):
                                previous_attrs_value_dict[index] = value0_list_splited[index]

                            value0_list_splited[index] = str(int(previous_attrs_value_dict[index]) + int(value[1][index]))

                            previous_attrs_value_dict[index] = value0_list_splited[index]
                            # print previous_attrs_value_dict[index]

                    res_value = ch.join(value0_list_splited)
                    current_url = current_url.replace(("%s=%s") % (key, value[0]),("%s=%s") % (key, res_value))


                else:
                    if(i ==0):
                        previous_attrs_value_dict[key] = int(value[0])
                    # url_attrs.append("%s=%s"%(key,int(value[1])+ previous_value))
                    # print "old:%s=%s"%(key,value[0])
                    # print "%s=%s"%(key, previous_attrs_value_dict[key] + int(value[1]))

                    current_url=current_url.replace(("%s=%s")%(key,value[0]),("%s=%s")%(key,int(value[1])+ previous_attrs_value_dict[key]))
                    # print current_url
                    previous_attrs_value_dict[key] = int(value[1])+ previous_attrs_value_dict[key]

                    # re.findall("%s=%s"%(key,value[0]),url)

            if(domain not in current_url):
                if(current_url.startswith("?")):
                    # print url_0.split("?")[0]
                    current_url = url_0.split("?")[0] + current_url
                    # print current_url
                elif(current_url.startswith("/")):
                    current_url = re.findall(".*\.com",url_0)[0]+current_url
            print current_url
    # return domain_to_pageNextDic

if __name__ == '__main__':

    print ctime()
    # url_list = [
    #     "http://search.jumei.com/?filter=0-11-1&search=%E9%9D%A2%E8%86%9C&from=search_toplist_%E9%9D%A2%E8%86%9C_word_pos_3&cat=",
    #     "http://search.dangdang.com/?key=%CA%E9&act=input",
    #     "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&suggest=1.his.0.0&wq=&pvid=9e4453eb3e86474c9f0d8ce8719b03aa",
    #     "https://s.taobao.com/search?initiative_id=tbindexz_20170509&ie=utf8&spm=a21bo.50862.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E6%89%8B%E6%9C%BA&suggest=0_1&_input_charset=utf-8&wq=shouji&suggest_query=shouji&source=suggest",
    #     "https://s.taobao.com/search?q=%E8%A1%A3%E6%9C%8D&imgfile=&ie=utf8",
    #     "https://list.tmall.com/search_product.htm?q=%D2%C1%DC%BD%C0%F6&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&xl=yifu_1&from=mallfp..pc_1_suggest",
    #     "http://list.mogujie.com/s?q=%E8%A1%A3%E6%9C%8D&ptp=1._mf1_1239_15261.0.0.8RN3PL&f=baidusem_4uv5iimn1v",
    #     "http://www.meilishuo.com/search/goods/?page=1&searchKey=%E8%A3%99%E5%AD%90%E5%A4%8F&acm=3.mce.1_4_.17721.33742-33692.3Va85qjv0ALoa.mid_17721-lc_201",
    #     "http://search.suning.com/%E6%89%8B%E6%9C%BA/",
    #
    #     # "www.xxxx.cn",
    # ]
    # list_len = len(url_list)
    # g1 = gevent.spawn(get_next_page_url_by_url_list,url_list[0:list_len/2])
    # g2 = gevent.spawn(get_next_page_url_by_url_list,url_list[list_len/2:list_len])
    # g1.join()
    # g2.join()

    pages_analysis()

        # url_2_splited = str(url_2).strip("?")[1].split("&")
        # print url_2_splited



    print ctime()
