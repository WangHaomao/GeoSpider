# -*- encoding: utf-8 -*-
import os
import re
from collections import Counter

from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
authorset = {'责任编辑', '作者'}

'''
    过滤无用的标签
    html_str:网页源代码
    flag:是否过滤标签
'''
def filter_tags(html_str, flag):
    html_str = re.sub('(?is)<!DOCTYPE.*?>', '', html_str)
    html_str = re.sub('(?is)<!--.*?-->', '', html_str)  # remove html comment
    html_str = re.sub('(?is)<script.*?>.*?</script>', '', html_str)  # remove javascript
    html_str = re.sub('(?is)<style.*?>.*?</style>', '', html_str)  # remove css
    html_str = re.sub('(?is)<a[\t|\n|\r|\f].*?>.*?</a>', '', html_str)  # remove a
    html_str = re.sub('(?is)<li[^nk].*?>.*?</li>', '', html_str)  # remove li
    # html_str = re.sub('(?is)<span .*?>.*?</span>', '', html_str)  # remove li
    html_str = re.sub('&.{2,5};|&#.{2,5};', '', html_str)  # remove special char
    if flag:
        html_str = re.sub('(?is)<.*?>', '', html_str)  # remove tag
    return html_str

'''
    根据文本块密度获取正文
    html_str:网页源代码
    return：正文文本
'''
def extract_content_by_block(html_str):
    html = filter_tags(html_str, True)
    lines = html.split('\n')
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
    for i in range(0, len(indexDistribution) - blockwidth):
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
            for index in range(startindex, endindex + 1):
                line = lines[index]
                if len(line.strip()) < 5:
                    continue
                tmp.append(line.strip() + '\n')
            tmp_str = ''.join(tmp)
            if u"Copyright" in tmp_str or u"版权所有" in tmp_str:
                continue
            arcticle_content.append(tmp_str)
            boolstart = False
            boolend = False
    return ''.join(arcticle_content)

'''
    全网页查找根据文本块密度获取的正文，获取文本父级标签获取正文
    html:网页html
    article:根据文本块密度获取的正文
    return:正文文本
'''
def extract_content_by_tag(html, article):
    lines = filter_tags(html, False)
    soup = BeautifulSoup(lines, 'lxml')
    p_list = soup.find_all('p')
    p_in_article = []
    for p in p_list:
        if p.text.strip() in article:
            p_in_article.append(p.parent)
    tuple = Counter(p_in_article).most_common(1)[0]
    article_soup = BeautifulSoup(str(tuple[0]), 'xml')
    return article_soup.text

'''
    获取节点中的文本
    node:节点
    return:节点文本
'''
def get_tag_text(node):
    text = re.sub("\\s+", '', node.text)
    return text

'''
    读取文件内容
    filepath:要读的文件路径
    return:文件内容
'''
def readFile(filepath):
    with open(filepath, 'r') as fopen:
        content = fopen.read()
        fopen.close()
    return content

'''
    向文件中写指定内容
    filepath:要写的文件路径
    content:要写的内容
'''
def writeFile(filepath, content):
    # print(filepath)
    # is_exist = os.path.exists(filepath)
    # if is_exist is False:
    #     os.mknod(filepath)
    with open(filepath, 'w') as fopen:
        fopen.write(content)
        fopen.close()

'''
    将文件夹下所有网页的正文抽取写到另一个文件夹中
    input_path:要读的文件夹
    output_path:要写的文件夹
'''
def extract(input_path, output_path):
    root_dir = os.listdir(input_path)
    for file in root_dir:
        # print(file)
        path = os.path.join('%s/%s' % (input_path, file))
        if os.path.isfile(path):
            html = readFile(path)
            temp_article = extract_content_by_block(html)
            try:
                acticle = extract_content_by_tag(html, temp_article)
            except:
                acticle = temp_article
            output_filename = os.path.join('%s/%s' % (output_path, file))
            writeFile(output_filename, acticle)

if __name__ == '__main__':
    extract('/home/kui/下载/1_20170614100615_ldaon/正文抽取-源数据','/home/kui/下载/1_20170614100615_ldaon/abc')
    # html = readFile("/home/kui/下载/1_20170614100615_ldaon/正文抽取-源数据/blog_539c5bd20102vox7.html")
    # article = extract_content_by_block(html)
    # print(article)
    # print("============")
    # article2 = extract_content_by_tag(html, article)
    # print(article2)
