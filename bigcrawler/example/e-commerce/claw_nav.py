# -*- encoding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from nav_selector import scoring
from nav_selector import loadFeature

res = requests.get('http://www.dangdang.com/')
soup = BeautifulSoup(res.text, 'lxml')

all_ul = soup.find_all('ul')

#print all_ul

scoring(all_ul, loadFeature('../../e-commerce.txt'))
#print all_ul[0]
#print "================"




#print all_ul[0]

#print "================================="

# soup2 = BeautifulSoup(all_ul[0], 'lxml')
# print soup2.a