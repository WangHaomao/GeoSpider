# -*- encoding: utf-8 -*-
import re
from bs4 import BeautifulSoup, Comment
import requests
import sys
from selenium import webdriver
# reload(sys)
# sys.setdefaultencoding("utf-8")
authorset = {'责任编辑', '作者'}

def get_html(url):
    # driver = webdriver.PhantomJS()
    # driver.get(url)
    obj = requests.get(url)
    #code = requests.head(url).encoding
    code = get_codetype(obj.text)
    if code is not None and code != '':
        obj.encoding = code
    return obj.text

def get_html_after_selenium(url):
    browser = webdriver.PhantomJS()
    browser.get(url)
    html_source = browser.page_source
    browser.close()
    return html_source


def filter_tags(html_str, flag):
    # soup = BeautifulSoup(html_str, "lxml")
    # # 把html里script，style给清理掉
    # [script.extract() for script in soup.find_all('script')]
    # [style.extract() for style in soup.find_all('style')]
    # # [ul.extract() for ul in soup.find_all('ul')]
    # # 提取代码中的注释
    # comments = soup.find_all(text=lambda text: isinstance(text, Comment))
    # # 清除注释
    # [comment.extract() for comment in comments]
    # # 用正则表达式，把所有的HTML标签全部清理
    # reg1 = re.compile("<[^>]*>")
    # content = reg1.sub('', soup.prettify()).split('\n')
    # return content
    html_str = re.sub('(?is)<!DOCTYPE.*?>', '', html_str)
    html_str = re.sub('(?is)<!--.*?-->', '', html_str) #remove html comment
    html_str = re.sub('(?is)<script.*?>.*?</script>', '', html_str) #remove javascript
    html_str = re.sub('(?is)<style.*?>.*?</style>', '', html_str) #remove css
    html_str = re.sub('(?is)<a[\t|\n|\r|\f].*?>.*?</a>', '', html_str)  # remove a
    if flag is True:
        html_str = re.sub('(?is)<li[^nk].*?>.*?</li>', '', html_str)  # remove li
    html_str = re.sub('&.{2,5};|&#.{2,5};', '', html_str) #remove special char
    html_str = re.sub('(?is)<.*?>', '', html_str)

    lines = html_str.split('\n')
    return lines

#获取编码类型
def get_codetype(html_str):
    soup = BeautifulSoup(html_str, 'lxml')
    meta = soup.find_all('meta')
    codetype = ''
    for m in meta:
        name = m.get('http-equiv')
        if name is not None:
            if str(name).lower() == 'content-type':
                charset = str(m.get('content')).lower()
                if 'charset=gb2312' in charset:
                    codetype = 'gb2312'
                    break
                elif 'charset=utf-8' in charset:
                    codetype = 'utf-8'
                    break
                elif 'charset=gbk' in charset:
                    codetype = 'gbk'
                    break
    if codetype == '':
        for m in meta:
            charset = m.get('charset')
            if charset is not None:
                if 'gb2312'==charset:
                    codetype = 'gb2312'
                    break
                elif 'utf-8'==charset:
                    codetype = 'utf-8'
                    break
                elif 'gbk'==charset:
                    codetype = 'gbk'
                    break
    return codetype

#获取标题
def get_title(html_str):
    soup = BeautifulSoup(html_str, 'lxml')
    # title_node = soup.title
    # h1_node = soup.h1
    # if title_node != None and h1_node != None:
    #     #title = title_node.text.strip()
    #     title = re.sub("\\s+", '', title_node.text.strip())
    #     h1 = re.sub("\\s+", '', h1_node.text.strip())
    #     print(title)
    #     print(h1)
    #     #h1 = h1_node.text.strip()
    #     if h1 in title:
    #         return h1
    title = soup.title.text
    title = re.sub(r'(-|_)','#', title)
    title = title.split('#')[0]
    print(title)
    if(len(title.strip())>=8):
        return title
    return None

#获取关键词
def get_keywords(html_str):
    soup = BeautifulSoup(html_str, 'lxml')
    keywords = None
    meta = soup.find_all('meta')
    for m in meta:
        name = str(m.get('name')).lower()
        if name=='keywords':
            keywords = m.get('content')
            break
    return keywords


def get_img(html_str):
    pass

#获取时间
def get_time_by_html(html_str):
    time_str = re.search(r'\d{4}(-|\u5E74)(0{0,1}[1-9]|1[0-2])(-|\u6708)(0{0,1}[1-9]|[1-2][0-9]|3[0-1])\u65E5{0,1}', html_str)
    if time_str is not None:
        return time_str.group(0)
    return None

def get_time_by_url(url):
    html = get_html(url)
    time_str = get_time_by_html(html)
    if time_str is None:
        html=get_html_after_selenium(url)
        time_str=get_time_by_html(html)
    return time_str

def get_all_url(html_str):
    soup = BeautifulSoup(html_str, 'lxml')
    alist = soup.find_all('a')
    href_list = []
    for a in alist:
        href = a.get('href')
        # print (a.text+" "+href)
        if href is not None and href !='':
            if href.startswith('javascript') or href.endswith('.jpg') or href.endswith('.png') or href.endswith('.jpeg') \
                    or href.endswith('gif') or href.endswith('.pdf'):
                continue
            else:
                href_list.append(href)

    return href_list



#获取正文父级标签
def get_parent_tag(html_str):
    soup = BeautifulSoup(html_str, 'lxml')
    parents = []
    content = filter_tags(html_str)
    for i, v in enumerate(content):
        if v.strip() != '' and v.strip is not None:
            pattern = re.compile(v.strip())
            element = soup.body.find(True, text=pattern)
            if element is not None and element.parent is not None:
                nidaye = element.parent
                parents.append(element.parent.name + str(element.parent.attrs))
                print(element.parent.name + str(element.parent.attrs))

#获取正文
def get_content(lines):
    # for a in lines:
    #     print(a)
    blockwidth = 3
    threshold = 86
    indexDistribution = []

    for i in range(0, len(lines) - blockwidth):
        wordnum = 0
        for j in range(i, i + blockwidth):
            line = re.sub("\\s+", '', lines[j])
            wordnum += len(line)
        indexDistribution.append(wordnum)

    startindex = -1
    endindex = -1
    boolstart = False
    boolend = False
    arcticle_content = []
    for i in range(0, len(lines) - blockwidth):
        if (indexDistribution[i] > threshold and boolstart is False):
            if indexDistribution[i + 1] != 0 or indexDistribution[i + 2] != 0 or indexDistribution[i + 3] != 0:
                boolstart = True
                startindex = i
                # print 'startindex=%d' %startindex
                continue
        if boolstart is True:
            if indexDistribution[i] == 0 or indexDistribution[i + 1] == 0:
                endindex = i
                # print 'endindex=%d' % endindex
                boolend = True
        tmp = []
        # print("%d %d"%(startindex,endindex))
        if boolend is True:
            for index in range(startindex,endindex+1):
                line = lines[index]
                if len(line.strip()) < 5:
                    continue
                tmp.append('<p>' + line.strip() + '</p>\n')
            tmp_str = ''.join(tmp)
            if u"Copyright" in tmp_str or u"版权所有" in tmp_str:
                continue
            arcticle_content.append(tmp_str)
            boolstart = False
            boolend = False
    return ''.join(arcticle_content)

def is_acricle_page_by_url_and_text(href, text):
    if href.endswith("index.html") or href.endswith("index.shtml") or href.endswith("index.htm"):
        #print("index结尾")
        return False
    if len(text.strip()) < 6:
        #print("标题文本太短")
        return False
    return True

def is_acricle_page_by_allinfo(html,title,time,keywords,content,url_num):
    if title is None:
        print("标题太短")
        return False
    if content is None or len(content.strip())<20:
        print("正文太短")
        return False
    if url_num > 300:
        print("url太多")
        return False
    if has_special_words(html):
        print("有特殊词")
        return False
    return True

def has_special_words(html):
    flag1 = re.findall('<a.*?>.*?下一页.*?</a>', html)
    flag2 = re.findall('<a.*?>.*?阅读全文.*?</a>', html)
    if len(flag1) > 0:
        return True
    if len(flag2) > 0:
        return True
    return False
    # flag2 = re.search('阅读全文', html)

if __name__ == "__main__":#http://news.sohu.com/s2014/nanshuibeidiao/
    #http://news.sohu.com/20061213/n247000032.shtml
    #http://news.sohu.com/s2017/xjpsf/
    url='http://star.news.sohu.com/s2014/chaoxian3/'
    ctthtml = get_html(url)

    print(len(get_all_url(ctthtml)))
    lines1 = filter_tags(ctthtml, True)
    content = get_content(lines1)
    print (get_title(ctthtml))
    time=get_time_by_url(url)
    print(time)

    print(content)

    #html = get_html_after_selenium(url)
    #print(get_content(filter_tags(html, True)))
    #print(find_words(ctthtml))
    # if content is None or content.strip()=='':
    #     html = get_html_after_selenium(url)
    #     print(html)
    #     print(get_content(filter_tags(html, True)))

# from selenium import webdriver
# driver = webdriver.PhantomJS()
# driver.get(url)
