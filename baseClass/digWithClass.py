# -*- coding:utf8 -*-
import os
import re
import urllib
from bs4 import BeautifulSoup

class Spider (object):

    def __init__(self, url, scope):
        """
            @param : urlIndex     # Whitch webSite you want to download.
                     articlesList # list of articles, In some scope.
        """
        self.urlIndex = urllib.urlopen(url)
        self.context = self.urlIndex.read()
        self.soup = BeautifulSoup(self.context)
        # self.articles = self.soup.find_all('li', class_='list-group-item title')
        self.articleslist = []
        self.genArticles(scope)
        self.gendetail('li')
        self.downloadTable = []  # downloadTable = { } # store the K:V with href and title
        self.filedImageurl = []  # collect pictrue when my REGEX can not match it.
        self.fullDownloadTable(True)  # prepery Table to download

    def genArticles(self, *args, **kargs):
        """
            self.genArticles({id='link2'})
        """
        self.articles = self.soup.find_all(args)

    def gendetail(self, *param):
        """
            This function gen a list called articleslist, to store list of url whitch I want 
            to download.
        """
        for item in self.articles:
            self.articleslist += item.find_all(param)

    def fullDownloadTable(self, needprefix):
        """ This function provides the downloadPage's url whitch user want to
            download. And save in instance perporty self.downloadTable.
            @peram: the scope of whitch context you want to featch, like <div> </div>
        """
        for i in range(len(self.articleslist)):
            articleAtag = self.articleslist[i].a
            if needprefix:
                if url[-1] == r'/':
                  raise "Please remove the last slash with your url."
                href = unicode(url) + articleAtag['href']
            else:
                href = articleAtag['href']
            title = articleAtag.text
            self.downloadTable.append((href, title))
        return self.downloadTable

    def createList(self):
        with open('./list.txt', 'a+') as fb:  # appand list to the new list
            for url, title in self.downloadTable:
                fb.write('%s %s\n' % (url.encode('utf8'), title.encode('utf8')))

    def downloadPage(self, articurl, title):
        artic = urllib.urlopen(articurl)
        pageContext = BeautifulSoup(artic.read())
        # self.saveImg(pageContext)
        self.saveArtical(articurl, pageContext, title)

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

    def saveArtical(self, articurl, pageContext, title):
        isyinwang = False
        if not os.path.exists('./artical'):
            os.mkdir('./artical')
        if isyinwang:
            publishTime = re.search(r'\d{4}\/\d{1,2}\/\d{1,2}', articurl)  # just for yinwang.org
            if not publishTime:
                title = 'IDNT'+title
            else:
                title = publishTime.group().replace('/', '-')+title
        with open('./artical/'+title+'.html', 'w') as fbaitic:
            fbaitic.write(str(pageContext))
        return "Do you want read next article %s. " % (title)

if __name__ == '__main__':
    url = r'http://learnvimscriptthehardway.stevelosh.com'
    smallSpider = Spider(url, 'ol')
    smallSpider.createList()
    for url,title in smallSpider.downloadTable:
        smallSpider.downloadPage(url, title)

    # table = smallSpider.downloadTable
    # for id, articalPair in enumerate(table):
    #     smallSpider.downloadPage(articalPair[0])
    #     print str(id)+" "+articalPair[1]
