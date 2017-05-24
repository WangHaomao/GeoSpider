# -*- encoding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

res = requests.get('http://news.ifeng.com/a/20170423/50983942_0.shtml')
#res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'lxml')


plist = soup.find_all('p')
for p in plist:
    print p

