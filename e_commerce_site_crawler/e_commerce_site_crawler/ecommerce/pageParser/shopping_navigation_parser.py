# -*- encoding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from e_commerce_site_crawler.ecommerce.spiderUtils import log_util


#淘宝
# url = 'https://www.taobao.com/'
# 当当
# url = "http://www.dangdang.com/"

#唯品会
# url = "http://www.vip.com/"
#凡客诚品
# url = "http://www.vancl.com/"
#一号店
# url = "http://club.yhd.com/"
# url = "http://www.yhd.com/"
#亚马逊
# url = "https://www.amazon.cn/"
#amazon USA
# url = 'https://www.amazon.com/'
# 美丽说
# url = "http://www.meilishuo.com/"


# res = requests.get(url)
# soup = BeautifulSoup(res.text, 'lxml')
# print res.text
# for x in  soup.find_all("a"):
#     print str(x)
# driver = webdriver.PhantomJS()
# driver.get(url)
# page = driver.page_source
# soup = BeautifulSoup(page, 'lxml')

# driver.close()
# step 1
# getAllCategoryFromKey(soup)
# step 2
# getNavFromUl(soup)
# setp 3
# getNavByClassNav(soup)

#计算得分
"""
给出一定的关键词，计算某个组建的关键词得分，得分高的作为navbar，存在一定失败率
"""
def get_nav_by_keyword_scoring(ulData,indexURL):
    featureDict = load_keyword_file('../../e-commerce.txt')

    scoreList = []
    hrefList = []
    index = 0
    fitting_index = 0
    fitting_score = -1

    # 避免url不完整的情况 step1
    # 这里还有问题，比如http://club.yhd.com/这恶果网站，以club开头
    url_domain = ''
    if 'https://www.' in indexURL:
        url_domain = indexURL.replace('https://www.','')
    elif "http://www." in indexURL:
        url_domain = indexURL.replace('http://www.', '')


    for ul in ulData:
        # print ul
        score = 0

        soup2 = BeautifulSoup(str(ul), 'lxml')
        # find out all <a> tag of one <ul>
        alist = soup2.find_all('a')
        if len(alist) != 0:
            for a in alist:
                soup3 = BeautifulSoup(str(a).strip(), 'lxml')
                content = soup3.a.text.strip().encode('utf8')

                href_list = soup3.find_all("a")
                # print href_list
                # if content != '' and content is not None and href !='' and href is not None:
                if content != '' and content is not None :
                    # and len(href_list) != 0 and str(href_list[0]) != ''
                    for key in featureDict.keys():
                        if content in key or key in content:
                            score += int(featureDict.get(key))
                            # print  content
                            break


                    # 避免url不完整的情况 step1
                    # for i in range(0,len(href_list)):
                    #     if (str(href_list[i]).startswith("//")):
                    #         if url_domain not in href_list[i]:
                    #             href_list[i] = indexURL + href_list[i]

        print "score=%d" %score
        scoreList.append(score)
        if fitting_score < score:

            fitting_index = index
            fitting_score = score

        index += 1
    # 符合
    print fitting_index
    if(len(scoreList)>0 and scoreList[fitting_index] >= 4):
        return ulData[fitting_index]
    else:return None


#加载特征数据
def load_keyword_file(fileName):
    fr = open(fileName, 'r')
    arrayLines = fr.readlines()
    featureDict = {}
    for line in arrayLines:
        line = line.strip()
        line = line.split(' ')
        featureDict[line[0]] = line[1]
        #print line[0]+" "+line[1]
    return featureDict


# strategy1 寻找所有分类（大分类页）
# strategy e-commerce get link from the keyword = "分类" or "商品分类"
# 返回一个url或空值，空即是没找到，执行下一步
def get_allCategory_from_Key(soup):
    keyword = [u"全部商品分类",u"商品分类",u"全部分类",u"分类",]
    for label_i in range(0, 4):
        a_key = soup.find_all(True, text=re.compile(keyword[label_i]))
        for a in a_key:
            # print  a
            if "</script>" in str(a):
                # print re.findall("{.+?}",str(a))
                for tmp in re.findall("{.+?}",str(a)):
                    if(keyword[label_i] in str(tmp)):
                        key_value = tmp.split(",")
                        for kv in key_value:
                            tmp_kv = kv.split(":")
                            key = tmp_kv[0]
                            value = tmp_kv[1]
                            #能否判断value是url,不能就用以下方法
                            if key =='"url"' :
                                return value
            else:
                deep = 1
                a_copy = a
                while(deep < 5):
                    soup_tmp = BeautifulSoup(str(a_copy), "lxml")
                    res_a= soup_tmp.find_all("a")
                    if len(res_a)!=0:
                        for a_list in res_a :
                            return a_list.get("href")
                        break

                    a_copy = a_copy.parent
                    # print  a_copy
                    deep += 1

    for label_i in range(0, 4):
        for sin_a in soup.find_all("a"):
             if keyword[label_i] in str(sin_a):
                  return sin_a.get("href")

    return None


# strategy2 class = nav
def get_nav_by_class_nav(soup):
    all_element = soup.find_all("ul",class_= re.compile("nav"))
    navUl = get_nav_by_keyword_scoring(all_element, url)
    if navUl is None:
        all_element = soup.find_all("div",class_= re.compile("nav"))
        print "isther::"
        for x in all_element:
            print str(x)
        navUl = get_nav_by_keyword_scoring(all_element, url)

    return navUl

# strategy3 all by select ul
def get_nav_by_tag_ul(soup):
    all_ul = soup.find_all('ul')
    print get_nav_by_keyword_scoring(all_ul, url)

# strategy4 还未完成，需要找子节点
def get_nav_by_tag_div(soup):
    all_div = soup.find_all('div')
    get_nav_by_keyword_scoring(all_div, url)

def debug(debug_info):
    print "debug:%s"%debug_info


from category_page_parser import category_page_parser
from e_commerce_site_crawler.ecommerce.spiderUtils.url_utils import url_sifter

def get_categoryList_method_in_index_url(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    allCategory_page_url = get_allCategory_from_Key(soup=soup)
    # method = 1
    if (allCategory_page_url != None):
        """
        这里实际上是进入下一页页面，一般写callback
        """
        allCategory_page_url = url_sifter(url, allCategory_page_url)
        print allCategory_page_url
        url_list = category_page_parser(allCategory_page_url)
        print len(url_list)

    else:
        pass


if __name__ == '__main__':

    # url = 'https://www.taobao.com/'
    # 当当
    # url = "http://www.dangdang.com/"
    # 唯品会
    # url = "http://www.vip.com/"
    # 凡客诚品
    url = "http://www.vancl.com/"
    # 一号店
    # url = "http://www.yhd.com/"
    # 亚马逊
    # url = "https://www.amazon.cn/"
    # amazon USA
    # url = 'https://www.amazon.com/'
    # 美丽说
    # url = "http://www.meilishuo.com/"


    resp = requests.get(url)

    soup = BeautifulSoup(resp.text,'lxml')

    allCategory_page_url =  get_allCategory_from_Key(soup=soup)
    if(allCategory_page_url != None):
        """
        这里实际上是进入下一页页面，一般写callback
        """
        log_util.info("大分类页面：" + allCategory_page_url)

        allCategory_page_url = url_sifter(url,allCategory_page_url)

        url_list = category_page_parser(allCategory_page_url)
        for u in url_list:
            print url_sifter(url,u)
        # print len(url_list)

    else:
        nav = get_nav_by_class_nav(soup)
        if nav == None:
            nav = get_nav_by_tag_ul(soup)
            print nav


        else:
            print "methon 2:"
            print nav