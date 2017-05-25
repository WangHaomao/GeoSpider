# -*- coding:utf-8 _*-
import re
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from e_commerce_site_crawler.\
    ecommerce.spiderUtils.\
    parser_util \
    import  get_soup_by_request_without_script,\
    get_soup_by_selenium_without_script,\
    get_xpath_doc_by_request_by_html_source,\
    get_soup_by_html_source



# 判断是否是商品列表的条件
"""
1、是否有足够的图片CONSEQUENT_SIMILAR_TAG_NUMBER个<img>标签
2、数量是否够多，在当前的wrapper中筛选符合条件1的 html数量最长的

后期可以添加筛选条件
"""
def check_is_goods_list(old_html_len,current_tag):
    CONSEQUENT_SIMILAR_TAG_NUMBER = 10
    tag_source = str(current_tag)
    img_len = len(get_soup_by_html_source(tag_source).find_all("img"))
    source_len = len(tag_source)
    if(img_len >= CONSEQUENT_SIMILAR_TAG_NUMBER and old_html_len < source_len):
        return source_len
    return  -1

def get_goods_list_tag_from_url(url):
    soup = get_soup_by_selenium_without_script(url)
    return get_goods_list_tag_from_soup(soup)

def get_goods_list_tag_from_soup(soup):
    # 按块查找，找到相似度较高且连续数高于某个值的外围后停止 ，每次选择当前区域内的最复杂区域（此处缩略为字符长最长的）
    # soup = soup = get_soup_by_request_without_script(url)

    has_find_goods_list = False
    max_len_tag = soup.find("body") #初始最大的外围
    goods_tag = max_len_tag
    deep = 0                        #查找深度
    SEARCH_DEEP_LIMIT = 20
    CONSEQUENT_SIMILAR_TAG_NUMBER = 10
    ATTRIBUTES_NUM_LIMIT = 3    #可允许商品中出现的不同class的个数，除了苏宁，一般都是2个以下（taobao 2个，其他（不包含未知） 1个）


    while(has_find_goods_list is False and deep < SEARCH_DEEP_LIMIT):

        max_len = 0
        tmp_max_len_tag = max_len_tag

        for child_tag in max_len_tag.children:
            # 排除不是tag的东西，比如\n，纯字符等等
            if(child_tag.name != None):
                # child_tag_len = len(str(child_tag))
                # if (child_tag_len > max_len):
                current_len =  check_is_goods_list(max_len,child_tag)
                if (current_len!=-1):
                    max_len = current_len
                    tmp_max_len_tag = child_tag

        max_len_tag = tmp_max_len_tag
        # 用来判断是否有多余的属性，初次属性设置为全都一样才算list
        """ 筛选条件：（筛选的缩放宽度）
            版本1：所有的 attributes 都一样
            版本2：允许出现两种以下的attributes
            版本3：将当前已有的 attributes 放入attrs_set内，检测set的长度（有几个attrs_set）
            将所有 attributes 组成一个字符串，比较即可
        """
        #保存当前有几种attributes了
        attrs_set = set()

        """ --------------新增上述一个对象-------------"""
        number_of_effective_children = 0
        tag_list_name = ""

        is_goods_list = True
        # 测试是否符合要求
        for child_tag in max_len_tag.children:

            if(child_tag.name != None):
                # print child_tag.attrs
                tag_attrs = child_tag.attrs
                # 第一次出现的attribute
                current_attrs_str = "".join(tag_attrs.keys())

                if(current_attrs_str not in attrs_set):
                    if(len(attrs_set) >= ATTRIBUTES_NUM_LIMIT):
                        is_goods_list = False
                        break
                    else:
                        attrs_set.add(current_attrs_str)
                    if(is_goods_list is False): break

                number_of_effective_children+=1

        # 同一个中某个标签大于10且服务条件
        if(number_of_effective_children>CONSEQUENT_SIMILAR_TAG_NUMBER and is_goods_list):
            has_find_goods_list = True
            goods_tag = max_len_tag

        deep+=1
    return max_len_tag

def get_goods_url_from_tag(wrapper_tag):
    goods_url_list = []
    for tag in wrapper_tag:
        if(tag.name != None):
            doc = etree.HTML(str(tag))
            a_list = doc.xpath("//a[@href]/@href")
            # print  a_list[0]
            print a_list


"""
解析翻页需要渲染js，交给selenium批量处理
selenium 批量处理将减少大量时间，提高效率
"""
def get_next_page_url(url_list):
    pass


if __name__ == '__main__':

    # url = "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&suggest=1.his.0.0&wq=&pvid=9e4453eb3e86474c9f0d8ce8719b03aa"
    url = "https://s.taobao.com/search?initiative_id=tbindexz_20170509&ie=utf8&spm=a21bo.50862.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E6%89%8B%E6%9C%BA&suggest=0_1&_input_charset=utf-8&wq=shouji&suggest_query=shouji&source=suggest"
    # url = "http://list.mogujie.com/s?q=%E6%89%8B%E6%9C%BA%E5%A3%B3%E8%8B%B9%E6%9E%9C6&from=querytip0&ptp=1._mf1_1239_15261.0.0.5u1T9Y"
    # url = "http://search.dangdang.com/?key=%CA%E9&act=input"
    # url = "http://search.suning.com/%E6%89%8B%E6%9C%BA/"

    # url = "http://search.yhd.com/c0-0/k%25E9%259B%25B6%25E9%25A3%259F/?tp=1.1.12.0.3.Ljm`JdW-10-4v5ud"
    # url = "http://www.meilishuo.com/search/goods/?page=1&searchKey=%E8%A3%99%E5%AD%90%E5%A4%8F&acm=3.mce.1_4_.17721.33742-33692.3Va85qjefPdEZ.mid_17721-lc_201"
    # url = "http://search.gome.com.cn/search?question=%E6%89%8B%E6%9C%BA"
    # url = "http://search.jumei.com/?referer=yiqifa_cps__ODg5MjEzfDAwczliN2JmZGVjN2EzOWQ2M2I5"
    # url = "https://www.vmall.com/search?keyword=%E6%89%8B%E6%9C%BA"

    soup = get_soup_by_selenium_without_script(url)
    # soup = get_soup_by_request_without_script(url)
    # 已经获得
    goods_list_tag = get_goods_list_tag_from_soup(soup)


    '''
        暂时不考虑没attribute的标签
    '''
    # print goods_list_tag
    # print goods_list_tag.name
    # print goods_list_tag.attrs
    #
    tag_name = goods_list_tag.name
    attrs_dic =  goods_list_tag.attrs


    # print soup.find_all(tag_name,attrs=attrs_dic)


    get_goods_url_from_tag(goods_list_tag)
