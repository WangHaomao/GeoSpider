# -*- encoding: utf-8 -*-
import os
import re
import threading
from collections import Counter

from bs4 import BeautifulSoup
import requests
import sys

from crawlermanage.utils.article_parser_util import get_html, get_title, get_time_by_html, get_keywords
from crawlermanage.utils.settings_helper import get_attr

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
    html_str = re.sub('(?is)<head.*?>.*?</head>', '', html_str)  # remove html head
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
    return remove_space(article_soup.text)


'''
    获取节点中的文本
    node:节点
    return:节点文本
'''


def remove_space(text):
    # text = re.sub('&.{2,5};|&#.{2,5};', '', text)  # remove special char
    # text = re.sub("\\s+", '', text)
    # text=text.replace('　','')
    return text


'''
    读取文件内容
    filepath:要读的文件路径
    return:文件内容
'''


def readFile(filepath):
    with open(filepath, 'r') as fopen:
        content = fopen.read().decode('utf-8')
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
        fopen.write(content.encode('utf-8'))
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


def test(standard_path, result_path):
    print(standard_path)
    print(result_path)
    base_dir = get_attr('BASE_DIR')
    jar = base_dir + "/crawlermanage/static/main-conent-extract-score.jar"
    print(jar)
    # text = os.popen('java -jar ' + jar + ' ' + standard_path + ' ' + result_path).read()
    # print('java -jar ' + jar + ' ' + standard_path + ' ' + result_path)
    os.system('java -jar ' + jar + ' ' + standard_path + ' ' + result_path)
    # print(text)
    # arr = text.split('最终准确率：')
    # return arr[0], arr[1]


def extract_content(html_str):
    article_temp = extract_content_by_block(html_str)
    try:
        article = extract_content_by_tag(html_str, article_temp)
    except:
        article = article_temp
    return (article).encode('utf-8')

def get_article_data(url):
    html = get_html(url)
    title = get_title(html)
    atime = get_time_by_html(html)
    keywords = get_keywords(html)
    content = extract_content(html)
    return str(title), str(atime), str(keywords), str(content)

if __name__ == '__main__':
    extract('/home/kui/下载/1_20170614100615_ldaon/ccc', '/home/kui/下载/1_20170614100615_ldaon/bbb')
    # print(get_attr('BASE_DIR'))
    # print(test('/home/kui/下载/1_20170614100615_ldon/aaa', '/home/kui/下载/1_20170614100615_ldaon/bbb'))
    # test('/home/kui/下载/1_20170614100615_ldon/right', '/home/kui/下载/1_20170614100615_ldaon/compare3')
#     html = readFile('/home/kui/下载/1_20170614100615_ldaon/正文抽取-源数据/blog_a3d444e30102wss6.html')
#     text = extract_content(html)
#     print(text)
#
#     xxx = """数天培训收费动辄过万，资深面试培训老师日工资可达五六千元，保过班、专家班、豪华套餐比比皆是，广告一年砸个几千万、吹嘘夸大，培训人员资质不合格……随着2017年国考面试进入尾声，各省联考、省考开始拉开序幕，公考培训进入忙碌期，而一直备受人们质疑的“公考培训乱象”亦随之而现。&nbsp;　　眼下，公考培 训市场已经成为奢侈型、非理性消费的新领地：寡头垄断之下，呈现典型的卖方市场特色，大培训机构是刀俎，来培训的是鱼肉，加之“知识无价”的幌子，定价权自然是“我的地盘听我的”。同时吹嘘夸大的培训效果，速成的培训，往往导致最后的人财两空。至于学员心理，大抵就两种：一是只买贵的不买对的。就像不敢输在起跑线的家长们一样，明知信息不对称，仍坚信重金能砸出“性价比”。二是胆小不经吓。看到别人都去参加培训了、又兼被培训机构的曼妙广告洗脑，总觉得粗放的自主学习不如参团的高价培训。花钱买个心安，好像能以肉疼的价格倒逼自己快马加鞭。　　虽说是“周瑜打黄盖”，但如果长期背离价值红线，就必有病态症状兴风作浪。面对中国公考培训市场的“疯狂与激情”，青年更需理性对待理性选择。　　首先，公考岗位固然“狼多肉少”，但如果人人都去参加培训，这和人人不参加培训的考中概率并无二致。其次，眼下的公考培训班，已然供求关系失衡，价格已经不可能“公道”。这个时候，非要砸钱进去，纯粹从成功率上说，算过“投资回报率”吗？再者，今日、乃至今后之中国公职人员，更侧重的是公务精神与业务素养，公务员履职，靠的是平常的积累，磨的是真切的功夫，花拳绣腿就想PK掉现实中的问题，不过是培训机构的痴人说梦罢了。青年应该在提升内力上下功夫，把精力放在提高实际工作解决能力以及人际关系矛盾的应变能力上，才能满足公务员职业的要求。指望“纸上得来终觉浅”的突击培训就能在面试中击楫中流，未免低估了考官的水平。　　当然，面对“天价公考培训”，仅有考生的理性自觉与自治显然是不够的。对于市场监管来说，恐怕还得“该出手时就出手”。比如所谓天价的“包过班”，是否涉嫌虚假宣传？又比如动辄天价的培训价格，消费者权益得以完美保障吗？天价培训市场，从来就不少“挂羊头卖狗肉”的伎俩，对于行业监督来说：一方面是打破信息壁垒、整饬市场业态，让有序竞争拉低“天价”的胆气；另一方面，也得让《广告法》等“长牙齿”“秀肌肉”，重拳整治公考培训市场的一切波诡云谲。
# 　　这些年，公考热渐趋理性，培训市场 上的种种乱象，也当来碗“清心汤”了吧！（中国青年网特约评论员 邓海建）
#     """
#     print  remove_space(xxx)