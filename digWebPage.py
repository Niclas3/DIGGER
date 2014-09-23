# -*- encoding:utf8 -*-
__author__ = 'Niclas'

'''
 some thing i want
 1.I need article's publish time 
 2.I need pure text
 3.I need HTML vision

# 2014年 9月22日 星期一 23时16分27秒 CST

'''

import urllib
from bs4 import BeautifulSoup

urlIndex= urllib.urlopen('http://www.yinwang.org/')
context = urlIndex.read()
soup = BeautifulSoup(context)
downloadTable = [] # downloadTable = { } # store the K:V with href and title

articles = soup.find_all('li',class_='list-group-item title')

for i in range(len(articles)):
    articleAtag = articles[i].a
    href = articleAtag['href']
    title = articleAtag.text

    downloadTable.append((href, title))

#print downloadTable

fb = open('./list.txt','a') # appand list to the new list 
for url, title in downloadTable:
    fb.write('%s %s\n' % (url.encode('utf8'), title.encode('utf8')))
fb.close()

for articPair in downloadTable: # To read each article's
    artic = urllib.urlopen(articPair[0])
    print "Do you want read next article %s.(Y/N)" % (articPair[1])
    chrack = raw_input()
    if(chrack == 'N'):
        continue
    else:
        print BeautifulSoup(artic.read())# BeautifulSoup(artic.read()).body


