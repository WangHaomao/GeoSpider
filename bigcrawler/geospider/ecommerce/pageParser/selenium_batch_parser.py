#-*-coding:utf-8 -*-
from selenium import webdriver
import sys

# from gevent import monkey; monkey.patch_socket()
# import gevent
from time import ctime
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree
from geospider.ecommerce.spiderUtils.parser_util import get_soup_by_html_source,get_webdriver
from geospider.ecommerce.spiderUtils.url_utils import url_sifter,get_partial_url
import re
import time
import logging
reload(sys)
sys.setdefaultencoding('utf-8')
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
        print (elem.tag_name)


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

# page_url_dic = {}
#[domain.com,domain.cn,domain.net....]
def get_url_domain(url):
    res_url = re.search("\.[0-9a-zA-Z]{2,14}\.(com.cn|com|cn|net|org|wang|cc)",url).group()
    return res_url[1:]
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


def get_all_page_number(url):
    print "getallpage_number:" + url
    driver = get_webdriver()

    attemps = 0
    ATTEMPS_TIMES = 3  # 失败尝试3次
    all_page_numer = -1

    # driver.get(url)
    #
    # driver.find_element_by_xpath()
    while (attemps < ATTEMPS_TIMES and all_page_numer==-1):
        driver.get(url)
        # print driver.page_source
        soup = get_soup_by_html_source(driver.page_source)


        is_find_number = False
        # 当前是第一页，寻找分页中的第二页，通过第二页找到第三页的URL
        element_2_list = soup.find_all("a", text="2")
        for elem in element_2_list:
            find_parent_times = 0
            while (find_parent_times < 4 and is_find_number is False):
                # descendants_list = []
                if (find_parent_times == 0):
                    elem_parent = elem.parent
                    descendants_list = elem_parent.contents
                elif (find_parent_times == 1):
                    elem_parent = elem.parent
                    descendants_list = elem_parent.descendants
                else:
                    elem_ancestor = elem
                    for up_times in range(0, find_parent_times):
                        elem_ancestor = elem_ancestor.parent

                    descendants_list = elem_ancestor.descendants

                for descendant in descendants_list:
                    if (descendant.name != None and descendant.name == 'a'):
                        if descendant.text == '3':
                            is_find_number = True
                        if (is_find_number and descendant.text.isdigit()):
                            # print descendant.text
                            all_page_numer = max(int(descendant.text),all_page_numer)
                    if (is_find_number and descendant.name != None):
                        allpage_text =  descendant.parent.parent.parent.text
                        try:
                            tmp_number = int(re.search("\d+",re.search(u"\d+\s*页",allpage_text).group()).group())
                            all_page_numer = max(tmp_number,all_page_numer)

                            # print (tmp_number)

                        except:
                            pass
                        # print tmp_number
                find_parent_times += 1

            if is_find_number and all_page_numer!=-1:
                break

        if(is_find_number and all_page_numer!=-1):
            break
        else:
            attemps+=1

    driver.close()
    # print (all_page_numer)
    return all_page_numer

"""
通过商品列表的第一个url获取接下来的第二页、第三页
返回值：list[url,urlpage2,urlpag3]
"""
def get_next_urlList_by_firstpage_url(url):
    driver = webdriver.PhantomJS('/usr/local/bin/phantomjs')
    print(url)
    attemps = 0
    ATTEMPS_TIMES = 3 #失败尝试3次
    FAILUED_STRING = "FAILUED_STRING"
    page_url_list = []
    while(attemps < ATTEMPS_TIMES):
        driver.get(url)
        time.sleep(3)
        # print(driver.page_source)
        soup = get_soup_by_html_source(driver.page_source)
        is_find_page3_url = False
        #当前是第一页，寻找分页中的第二页，通过第二页找到第三页的URL
        element_2_list = soup.find_all("a",text="2")
        number_to_url_dic = {}
        for elem in element_2_list:
            find_parent_times = 0
            while(find_parent_times < 4 and is_find_page3_url is False):
                # descendants_list = []
                if(find_parent_times == 0):
                    elem_parent = elem.parent
                    descendants_list = elem_parent.contents
                elif(find_parent_times == 1):
                    elem_parent = elem.parent
                    descendants_list = elem_parent.descendants
                else:
                    elem_ancestor = elem
                    for up_times in range(0,find_parent_times):
                        elem_ancestor = elem_ancestor.parent

                    descendants_list = elem_ancestor.descendants

                for descendant in descendants_list:
                    if (descendant.name != None and descendant.name == 'a'):
                        if descendant.text == '3':
                            number_to_url_dic['2'] = elem.get("href")
                            number_to_url_dic['3'] = descendant.get("href")
                            number_to_url_dic['attrs_dic2'] = elem.attrs
                            number_to_url_dic['attrs_dic3'] = descendant.attrs
                            is_find_page3_url = True
                            # print (elem.get("href"))
                            # print ("-----------------------------")

                find_parent_times += 1

            if is_find_page3_url :
                break
        next_url_is_fake = False
        # try:
        url_2 =  number_to_url_dic['2']
        url_3 =  number_to_url_dic['3']
        """
        处理假URL的情况，比如有些URL是#,javascript;这里需要用driver动态跳转，获取current_url
        """
        if(url_2.lower() == url_3.lower()):
            url_2 = get_url_by_attrs_dic(driver, number_to_url_dic["attrs_dic2"])
            url_3 = get_url_by_attrs_dic(driver, number_to_url_dic["attrs_dic3"])
            # 出现解析问题，这个url可以跳过
            if (url_2.lower() == url_3.lower()):
                return None

            page_url_list = [url, url_2, url_3]
            break
        else:
            page_url_list = [url, url_2, url_3]
            break
            # break

        # attemps = 1 + attemps
        # except:
        #     # print "Failed..."
        #     attemps += 1
        #     if(attemps >= ATTEMPS_TIMES):
        #         page_url_list = [url, FAILUED_STRING, FAILUED_STRING]
        #
        #         logging.warning(url+"分页解析失败！！")
        #
        #     # print number_to_url_dic['2']
        #     # print number_to_url_dic['3']

    driver.close()

    return page_url_list


"""
通过list[url,urlpage2,urlpag3](上一个函数的返回值),获取翻页的信息和关键字信息
返回值：
1、翻页信息,两种情况：
page_name = pagenum (只是一个数字)
page_name = pagemessage (例如0-11-2)
{page_name:[pagenum(第二页的num),dx(差值)]}
{page_name:[pagemessage,{index(第几个数相加（一般是最后一个）):dx}]}


返回值类型：dict

2、查询关键字信息
search_name = keyword
返回值类型:string

例如：
http://search.jumei.com/?filter=0-11-1&search=%E9%9D%A2%E8%86%9C
返回{'filter': ['0-11-2', {2: 1}]},'search'
               value[0]  value[1]
       key          value
"""

# def get_pageKeyDic_and_searchKeywordKey(page_urls,searchKeyword):
def get_pageKeyDic(page_urls):
    url_2 = page_urls[1]
    url_3 = page_urls[2]
    # 获取倒数第二个元素
    url_2_pieces = str(url_2).split("?")[-1].split("&")
    url_3_pieces = str(url_3).split("?")[-1].split("&")
    pieces_2_len = len(url_2_pieces)
    pieces_3_len = len(url_3_pieces)

    """-------------------------返回值-----------------------------"""
    pageKeyDic = {}
    # try:
    #     re_str = "\?\w+=%s|&\w+=%s|/\w+=%s"%(searchKeyword,searchKeyword,searchKeyword)
    #     print (re_str)
    #     print (url_2)
    #     searchKeywordKey = re.findall(re_str,url_2)[0].split("=")[0][1:]
    #
    # except:
    #     searchKeywordKey = "SEARCHKEYERROR"

    """-----------------------------------------------------------"""

    if pieces_2_len != pieces_3_len:
        raise Exception("解析分页URL碎片时，第二页和第一页URL参数不相等")

    for pieces_index in range(0,pieces_3_len):
        pieces_2_splited = url_2_pieces[pieces_index].split("=")
        pieces_3_splited = url_3_pieces[pieces_index].split("=")

        """
            将page=1这类字符串分割为[page,1],判断第二个值的差，拼接url
            -1是取倒数第一个，当出现只有值不是=分割时，用这种方式比较方便
            存储方式:
            domain.com:{
                            name1:[1(原值，即第二页的值),1(dx,差值)],
                            name2:[0-11-2(原值，即第二页的值),{2:1(dx,差值)}]
                        }
                        
            name2比较特殊，在拥有特殊字符的串中，将0-11-2分割，第2个数字有差值(从0开始)
            
        """
        if(len(pieces_2_splited) == 2 and pieces_2_splited[-1]!=pieces_3_splited[-1]):
            value2 = pieces_2_splited[-1]
            value3 = pieces_3_splited[-1]
            if(value2.isdigit()):
                dx =  int(value3) - int(value2)
                pageKeyDic[pieces_2_splited[0]] = [pieces_2_splited[1],dx]


            else:
                value_str_len = min(len(value2),len(value3))
                value2_list = list(value2)
                value3_list = list(value3)
                for ch_index in range(0,value_str_len):
                    if(value2[ch_index].isdigit() is False):
                        value2_list[ch_index] = " "
                    if (value3[ch_index].isdigit() is False):
                        value3_list[ch_index] = " "
                value2 = "".join(value2_list).split(" ")
                value3 = "".join(value3_list).split(" ")


                num_len = len(value2)
                page_index_to_dx = {}
                for num_index in range(0,num_len):
                    if(value2[num_index] != value3[num_index]):
                        page_index_to_dx[num_index] =  int(value3[num_index]) - int(value2[num_index])

                pageKeyDic[pieces_2_splited[0]] = [pieces_2_splited[-1],page_index_to_dx]


    # return pageKeyDic,searchKeywordKey
    return pageKeyDic

# 必须是第二页之后,返回下一页的url
def get_next_page_by_pageKeyDic_pageUrls_currentPageUrl(pageKeyDic,page_urls,current_page_url):
    # for domain, page_urls in page_url_dic.items():
    url_0 = page_urls[0]
    print (url_0)
    url = page_urls[1]
    url_pageKeyDic = pageKeyDic
    # print url
    previous_attrs_value_dict = {}
    next_url = current_page_url
    for key, value in url_pageKeyDic.items():
        re_str = "%s=(\w-*)+" % key
        page_key_value = re.search(re_str, current_page_url).group()
        if (isinstance(value[1], dict)):
            page_value = page_key_value.split("=")[-1]
            value0_list = list(page_value)
            value0_list_len = len(value0_list)
            ch = " "
            for ch_index in range(0, value0_list_len):
                if (value0_list[ch_index].isdigit() is False):
                    ch = value0_list[ch_index]
                    value0_list[ch_index] = " "

            value0_list_splited = "".join(value0_list).split(" ")
            value0_list_len = len(value0_list_splited)
            for index in range(0, value0_list_len):
                if (value[1].has_key(index)):
                    value0_list_splited[index] = str(int(value0_list_splited[index]) + int(value[1][index]))
            new_page_value = ch.join(value0_list_splited)

        else:
            new_page_value = int(page_key_value.split("=")[-1]) + value[1]

            # print page_key_value, new_page_key_value

        new_page_key_value = "%s=%s"%(page_key_value.split("=")[0],str(new_page_value))
        next_url = next_url.replace(page_key_value, new_page_key_value)

    print ("next = "+next_url)
    return next_url

def get_all_page_urls(pageKeyDic,page_urls,all_page_number):
    url_0 = page_urls[0]
    url = page_urls[1]
    url_pageKeyDic = pageKeyDic
    # print url
    previous_attrs_value_dict = {}
    all_url_list = []
    for i in range(0, all_page_number+1):
        current_url = url
        for key, value in url_pageKeyDic.items():
            if isinstance(value[1], dict) is True:
                value0_list = list(value[0])
                value0_list_len  = len(value0_list)
                ch = " "
                for ch_index in range(0,value0_list_len):
                    if(value0_list[ch_index].isdigit() is False):
                        ch = value0_list[ch_index]
                        value0_list[ch_index] = " "


                value0_list_splited = "".join(value0_list).split(" ")
                value0_list_len = len(value0_list_splited)
                for index in range(0,value0_list_len):
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
                current_url=current_url.replace(("%s=%s")%(key,value[0]),("%s=%s")%(key,int(value[1])+ previous_attrs_value_dict[key]))
                previous_attrs_value_dict[key] = int(value[1])+ previous_attrs_value_dict[key]

        if(get_url_domain(url) not in current_url):
            # if(current_url.startswith("?")):
            #     # print url_0.split("?")[0]
            #     current_url = url_0.split("?")[0] + current_url
            #     # print current_url
            # elif(current_url.startswith("/")):
            #     current_url = re.findall(".*\.com",url_0)[0]+current_url
            url_sifter(get_partial_url(url_0),current_url)

        all_url_list.append(current_url)
    return all_url_list

def get_nextpage_info(url):

    page_urls = get_next_urlList_by_firstpage_url(url)
    pageKeyDic =  get_pageKeyDic(page_urls)
    # print get_next_page_by_pageKeyDic_currentPageUrl_pageKey_and_searchKey(pageKeyDic,page_urls,page_urls[-1])
    get_all_page_urls(pageKeyDic,page_urls,20)


if __name__ == '__main__':

    print (ctime())
    url_list = [

        "http://search.jumei.com/?filter=0-11-1&search=%E9%9D%A2%E8%86%9C&from=search_toplist_%E9%9D%A2%E8%86%9C_word_pos_3&cat=",
        "http://search.dangdang.com/?key=%CA%E9&act=input",
        "https://search.jd.com/Search?keyword=手机&enc=utf-8&suggest=1.his.0.0&wq=&pvid=9e4453eb3e86474c9f0d8ce8719b03aa",
        "https://s.taobao.com/search?initiative_id=tbindexz_20170509&ie=utf8&spm=a21bo.50862.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E6%89%8B%E6%9C%BA&suggest=0_1&_input_charset=utf-8&wq=shouji&suggest_query=shouji&source=suggest",
        "https://s.taobao.com/search?q=%E8%A1%A3%E6%9C%8D&imgfile=&ie=utf8",
        "https://list.tmall.com/search_product.htm?q=%D2%C1%DC%BD%C0%F6&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&xl=yifu_1&from=mallfp..pc_1_suggest",
        "http://list.mogujie.com/s?q=%E8%A1%A3%E6%9C%8D&ptp=1._mf1_1239_15261.0.0.8RN3PL&f=baidusem_4uv5iimn1v",
        "http://www.meilishuo.com/search/goods/?page=1&searchKey=%E8%A3%99%E5%AD%90%E5%A4%8F&acm=3.mce.1_4_.17721.33742-33692.3Va85qjv0ALoa.mid_17721-lc_201",
        "http://search.suning.com/%E6%89%8B%E6%9C%BA/",
    ]
    # url = "https://s.taobao.com/list?spm=a217f.7278017.1997728653.6.j5XpLB&q=轻薄款&style=grid&seller_type=taobao&cps=yes&cat=50099260"
    # for x in url_list:
    #
    #     get_all_page_number(x)
    # print get_next_urlList_by_firstpage_url(url)
    # get_nextpage_info(url_list[0],"%CA%E9")
    url = "https://s.taobao.com/list?q=%E7%BE%BD%E7%BB%92%E6%9C%8D"

    # page_list = get_next_urlList_by_firstpage_url(url)
    # print get_pageKeyDic(page_list)
    # print page_list
    # Dict_page = {'s': ['60', 60]}



    # res = get_all_page_urls({'s': ['60', 60]},[u'https://s.taobao.com/list?q=%E7%BE%BD%E7%BB%92%E6%9C%8D',
    #  u'https://s.taobao.com/list?q=%E7%BE%BD%E7%BB%92%E6%9C%8D&bcoffset=12&s=60',
    #  u'https://s.taobao.com/list?q=%E7%BE%BD%E7%BB%92%E6%9C%8D&bcoffset=12&s=120'],100)
    res = get_all_page_urls({'s': ['60', 60]}, [u'https://s.taobao.com/list?q=手机',
                                                u'https://s.taobao.com/list?q=手机&bcoffset=12&s=60',
                                                u'https://s.taobao.com/list?q=手机&bcoffset=12&s=120'],
                            100)
    for x in res:
        print str(x)



    # print get_all_page_number(url)
    # for x in url_list:
    #     print get_url_domain(x)

    # pages_analysis(['http://search.jumei.com/?filter=0-11-1&search=%E9%9D%A2%E8%86%9C&from=search_toplist_%E9%9D%A2%E8%86%9C_word_pos_3&cat=', 'http://search.jumei.com/?filter=0-11-2&search=%E9%9D%A2%E8%86%9C&bid=4', 'http://search.jumei.com/?filter=0-11-3&search=%E9%9D%A2%E8%86%9C&bid=4'])

        # url_2_splited = str(url_2).strip("?")[1].split("&")
        # print url_2_splited

    # print (get_next_urlList_by_firstpage_url(url_list[4]))
    print (ctime())
