# -*- encoding: utf-8 -*-
import re
from bs4 import BeautifulSoup, Comment
import requests
authorset = {'责任编辑', '作者'}

def getcontentfromweb(url):
    obj = requests.get(url)
    #code = requests.head(url).encoding
    code = getcodetype(obj.text)
    print code
    if code is not None and code != '':
        obj.encoding = code
    return obj.text


def filter_tags(html_str):
    soup = BeautifulSoup(html_str, "lxml")
    # 把html里script，style给清理掉
    [script.extract() for script in soup.find_all('script')]
    [style.extract() for style in soup.find_all('style')]
    # 提取代码中的注释
    comments = soup.find_all(text=lambda text: isinstance(text, Comment))
    # 清除注释
    [comment.extract() for comment in comments]
    # 用正则表达式，把所有的HTML标签全部清理
    # soup.prettify()
    return soup

def filter_ul_tags(soup):
    [ul.extract() for ul in soup.find_all('ul')]
    return soup

def get_origin_content(soup):
    reg1 = re.compile("<[^>]*>")
    # print soup.text
    content = reg1.sub('', soup.text).split('\n')
    # for i, v in enumerate(content):
    #     content[i] = v.strip()
    regex = re.compile("\\s+")
    # reg_a = re.compile("'http?://[^/]+?/'")
    for i, s in enumerate(content):
        content[i] = re.sub(regex, '', s)
        # content[i] = re.sub(reg_a, '', content[i])
        # print i,len(content[i]),content[i]
    return content

#获取编码类型
def getcodetype(html):
    soup = BeautifulSoup(html, 'lxml')
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
def gettitle(soup):
    return soup.title

#获取关键词
def getkeywords(soup):
    keywords = None
    meta = soup.find_all('meta')
    for m in meta:
        name = str(m.get('name')).lower()
        if name=='keywords':
            keywords = m.get('content')
            break
    return keywords


def getimg(src):
    soup = BeautifulSoup(src, "lxml")
    if src != '' and src is not None:
        print soup.find_all('img')

#获取时间
def gettime(soup):
    content = get_origin_content(soup)
    time = re.search(r'\d{4}[-\D?]\d{2}[-\D?]\d{2}\D?', ''.join(content))
    if time is not None:
        return time.group(0)

def get_all_url(soup):
    alist = soup.find_all('a')
    href_list = []
    for a in alist:
        href = a.get('href')
        if href is not None and href !='':
            if href.startswith('javascript') is False:
                href_list.append(href)
    return href_list



#获取正文父级标签
def getparent_by_most(html_str, content):
    soup = BeautifulSoup(html_str, "lxml")
    [script.extract() for script in soup.find_all('script')]
    [style.extract() for style in soup.find_all('style')]
    # 提取代码中的注释
    comments = soup.find_all(text=lambda text: isinstance(text, Comment))
    # 清除注释
    [comment.extract() for comment in comments]
    parents = []
    # s = '原标题：拒绝百万奖学金的女孩'
    # pattern = re.compile(s.decode('utf-8'))
    # element = soup.find(True, text=pattern)
    # print element.parent
    for i, v in enumerate(content):
        if v.strip() != '' and v.strip is not None:
            pattern = re.compile(v.strip())
            element = soup.body.find(True, text=pattern)
            if element is not None and element.parent is not None and len(v.strip()) > 30:
                nidaye = element.parent
                parents.append(element.parent.name + str(element.parent.attrs))
                print element.parent.name + str(element.parent.attrs)
                print "============="
                # for s in parents:
                #     print s
                #     print "==========="

#获取正文1
def getcontent1(lst):
    lstlen = [len(x) for x in lst]
    blockwidth = 3
    threshold = 80
    indexDistribution = []
    for i in range(0, len(lstlen) - blockwidth):
        wordnum = 0
        for j in range(i, i + blockwidth):
            wordnum += lstlen[j]
        # print i,len(lst[i]),wordnum,lst[i]
        indexDistribution.append(wordnum)
    startindex = -1
    endindex = -1
    boolstart = False
    boolend = False
    newcontent = ''
    for i in range(0, len(indexDistribution) - 1):
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
        if boolend is True:
            for x in lst[startindex:endindex + 1]:
                if len(x.strip()) < 5: continue
                tmp.append('<p>' + x.strip() + '</p>\n')
            str = ''.join(tmp)
            # for s in content:
            #     print s
            if u"Copyright" in str or u"版权所有" in str:
                continue
            newcontent = newcontent + str
            boolstart = False
            boolend = False
    return newcontent
    # for i,v in enumerate(lstlen[:maxindex-3]):
    #     if v> threshold and lstlen[i+1]>5 and lstlen[i+2]>5 and lstlen[i+3]>5:
    #         startindex = i
    #         break
    # for i,v in enumerate(lstlen[maxindex:]):
    #     if v< threshold and lstlen[maxindex+i+1]<10 and lstlen[maxindex+i+2]<10 and lstlen[maxindex+i+3]<10:
    #         endindex = i
    #         break
    # content =['<p>'+x.strip()+'</p>' for x in lst[startindex:endindex+maxindex] if len(x.strip())>0]
    # return content

#获取正文2
def getcontent2(lst):
    lstlen = [len(x) for x in lst]
    threshold = 50
    startindex = 0
    maxindex = lstlen.index(max(lstlen))
    endindex = 0
    for i, v in enumerate(lstlen[:maxindex - 3]):
        if v > threshold and lstlen[i + 1] > 5 and lstlen[i + 2] > 5 and lstlen[i + 3] > 5:
            startindex = i
            break
    for i, v in enumerate(lstlen[maxindex:]):
        if v < threshold and lstlen[maxindex + i + 1] < 10 and lstlen[maxindex + i + 2] < 10 and lstlen[
                            maxindex + i + 3] < 10:
            endindex = i
            break
    content = ['<p>' + x.strip() + '</p>\n' for x in lst[startindex:endindex + maxindex] if len(x.strip()) > 0]
    return ''.join(content)


def choose_stratigy():
    pass


def run(url):
    ctthtml = getcontentfromweb(url)
    soup = filter_tags(ctthtml)
    soup2 = filter_ul_tags(soup)
    title = gettitle(soup)
    print title
    print "==========="
    time = gettime(soup)
    print time
    print "==========="
    keywords = getkeywords(soup)
    print keywords
    print "============"
    origin_content = get_origin_content(soup2)
    content = getcontent1(origin_content)
    if len(content) < 30:
        origin_content = get_origin_content(soup)
        content = getcontent1(origin_content)
    print content
    print "==========="
    return title,time,keywords,content


if __name__ == "__main__":#http://news.sohu.com/s2014/nanshuibeidiao/
    ctthtml = getcontentfromweb('http://news.sohu.com/s2014/nanshuibeidiao/')
    soup = filter_tags(ctthtml)
    print get_all_url(soup)
    print len(get_all_url(soup))
    soup2 = filter_ul_tags(soup)
    title = gettitle(soup)
    print title
    print "==========="
    time = gettime(soup)
    print time
    print "==========="
    keywords = getkeywords(soup)
    print keywords
    print "============"
    origin_content = get_origin_content(soup2)
    content = getcontent1(origin_content)
    # if len(content)<30:
    #     origin_content = get_origin_content(soup)
    #     content = getcontent1(origin_content)
    print content
    print "==========="

