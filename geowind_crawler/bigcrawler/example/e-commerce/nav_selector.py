# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
'''
    author:Yangkui
'''
#加载特征数据
def loadFeature(fileName):
    fr = open(fileName, 'r')
    arrayLines = fr.readlines()
    featureDict = {}
    for line in arrayLines:
        line = line.strip()
        line = line.split(' ')
        featureDict[line[0]] = line[1]
        #print line[0]+" "+line[1]
    return featureDict

#计算得分
def scoring(ulData, featureDict):
    scoreList = []
    hrefList = []
    index = 0
    for ul in ulData:
        score = 0
        soup2 = BeautifulSoup(str(ul), 'lxml')
        alist = soup2.find_all('a')
        if len(alist) != 0:
            for a in alist:
                soup3 = BeautifulSoup(str(a).strip(), 'lxml')
                #print soup3.a.text.strip() +" "+soup3.a['href']
                content = soup3.a.text.strip().encode('utf8')
                href = soup3.a['href']
                #print href
                #print content
                if content != '' and content is not None and href !='' and href is not None:
                    #print content
                    if featureDict.has_key(content):
                        score += int(featureDict.get(content))
                    if (href.startswith("//")):
                        href = "http:" + href
                        #print href
            print "score=%d" %score
            scoreList.insert(index, score)
            index += 1


if __name__ == "__main__":
    dict = loadFeature('../../e-commerce.txt')
    print dict.items()
    print dict.get('数码')