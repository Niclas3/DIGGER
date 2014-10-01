# -*- coding:utf8 -*-
import os
import re
import urllib
from bs4 import BeautifulSoup


class Spider (object):

    def __init__(self):
        self.urlIndex = urllib.urlopen('http://www.yinwang.org/')
        self.context = self.urlIndex.read()
        self.soup = BeautifulSoup(self.context)
        self.articles = self.soup.find_all('li', class_='list-group-item title')
        self.downloadTable = []  # downloadTable = { } # store the K:V with href and title
        self.filedImageurl = []  # collect pictrue when my REGEX can not match it.
        self.fullDownloadTable()  # prepery Table to download

    def fullDownloadTable(self):
        for i in range(len(self.articles)):
            articleAtag = self.articles[i].a
            href = articleAtag['href']
            title = articleAtag.text
            self.downloadTable.append((href, title))
        self.createList()
        return self.downloadTable

    def createList(self):
        with open('./list.txt', 'a+') as fb:  # appand list to the new list
            for url, title in self.downloadTable:
                fb.write('%s %s\n' % (url.encode('utf8'), title.encode('utf8')))

    def downloadPage(self, articurl):
        artic = urllib.urlopen(articurl)
        pageContext = BeautifulSoup(artic.read())
        self.saveImg(pageContext)
        self.saveArtical(articurl, pageContext)

    def saveImg(self, pageContext):
        title = ''
        if not os.path.exists('./img'):  # Just working at the first time.
            os.mkdir('./img')
        for imgid, imgTag in enumerate(pageContext.find_all('img')):
            '''
               if you can not understand the code, let it go......
            '''
            rawimgName = re.search(r'\b[a-z]*.\b[a-z]*\b"', str(imgTag))
            if not rawimgName:  # fix regex bug.
                self.filedImageurl.append(str(imgTag))
                print "pic donwloads failed.", title
            else:
                if rawimgName.group()[:-1][0] == '.':
                    print 'Find A point.'
                    imgName = str(imgid)+title+rawimgName.group()[:-1]
                else:
                    imgName = rawimgName.group()[:-1]
                with open('./img/'+imgName, 'a') as img:
                    img.write(urllib.urlopen(imgTag['src']).read())

    def saveArtical(self, articurl, pageContext):
        title = ''
        if not os.path.exists('./artical'):
            os.mkdir('./artical')
        publishTime = re.search(r'\d{4}\/\d{1,2}\/\d{1,2}', articurl)
        if not publishTime:
            title = 'IDNT'+title
        else:
            title = publishTime.group().replace('/', '-')+title
        with open('./artical/'+title+'html', 'w') as fbaitic:
            fbaitic.write(str(pageContext))
        return "Do you want read next article %s. %d" % (title, id)

if __name__ == '__main__':
    smallSpider = Spider()
    table = smallSpider.downloadTable
    for id, articalPair in enumerate(table):
        smallSpider.downloadPage(articalPair[0])
        print str(id)+" "+articalPair[1]
