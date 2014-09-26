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


def typess(fn):
    '''
        This function to handle out question that
        I want to know fn()'s return type
    '''
    def _warp():
        return type(fn())
    return _warp

urlIndex = urllib.urlopen('http://www.yinwang.org/')
context = urlIndex.read()
soup = BeautifulSoup(context)
downloadTable = []  # downloadTable = { } # store the K:V with href and title

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

for articPair in downloadTable:  # To read each article's
    artic = urllib.urlopen(articPair[0])
    title = articPair[1]
    print "Do you want read next article %s.(Y/N)" % title
    chrack = raw_input()
    if(chrack == 'N'):
        continue
    else:
        context = BeautifulSoup(artic.read())
        ''' It is BeautifulSoup type not String
            Ones page has img tag and I need download it
        '''
        if context.find_all('img'):
            imgName = '2'
            for imgTag in context.find_all('img'):
                with open('./'+imgName+'.jpeg', 'a') as img:
                    img.write(urllib.urlopen(imgTag['src']).read())
        else:
            pass
        # with open('./'+title, 'w') as fbaitic:
        #     fbaitic.write(str(context))
