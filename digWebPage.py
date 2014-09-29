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
import re
import os
from bs4 import BeautifulSoup


def typess(fn):
    '''
        This function to handle out question that
        I want to know fn()'s return type
    '''
    def _warp():
        return type(fn())
    return _warp

urlIndex = urllib.urlopen('http://www.yinwang.org/')
indexContext = urlIndex.read()
soup = BeautifulSoup(indexContext)
downloadTable = []  # downloadTable = { } # store the K:V with href and title
filedImageurl = []  # collect pictrue when my REGEX can not match it.

articles = soup.find_all('li', class_='list-group-item title')

for i in range(len(articles)):
    articleAtag = articles[i].a
    href = articleAtag['href']
    title = articleAtag.text

    downloadTable.append((href, title))

'''
    This list.txt file should append single line for each url visit,
    so I want to cheack out the last line of this file.
'''

with open('./list.txt', 'a') as fb:  # appand list to the new list
    for url, title in downloadTable:
        fb.write('%s %s\n' % (url.encode('utf8'), title.encode('utf8')))

for id, articPair in enumerate(downloadTable):  # To read each article's
    articurl = articPair[0]
    title = articPair[1]
    artic = urllib.urlopen(articurl)
    pageContext = BeautifulSoup(artic.read())

    ''' It is BeautifulSoup type not String
        Ones page has img tag and I need download it
    '''
    if pageContext.find_all('img'):
        if not os.path.exists('./img'):  # Just working at the first time.
            os.mkdir('./img')
        for imgid, imgTag in enumerate(pageContext.find_all('img')):
            '''
                if you can not understand the code, let it go......
            '''
            rawimgName = re.search(r'\b[a-z]*.\b[a-z]*\b"', str(imgTag))
            if not rawimgName:  # fix regex bug.
                filedImageurl.append(str(imgTag))
                print "pic donwloads failed.", title
            else:
                if rawimgName.group()[:-1][0] == '.':
                    print 'Find A point.'
                    imgName = str(imgid)+title+rawimgName.group()[:-1]
                else:
                    imgName = rawimgName.group()[:-1]
                with open('./img/'+imgName, 'a') as img:
                    img.write(urllib.urlopen(imgTag['src']).read())

    if not os.path.exists('./artical'):
        os.mkdir('./artical')
    publishTime = re.search(r'\d{4}\/\d{1,2}\/\d{1,2}', articurl)
    if not publishTime:
        title = 'IDNT'+title
    else:
        title = publishTime.group().replace('/', '-')+title
    with open('./artical/'+title+'html', 'w') as fbaitic:
        fbaitic.write(str(pageContext))
    print "Do you want read next article %s. %d" % (title, id)
