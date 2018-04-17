#-*-coding=utf-8-*-

import urllib2
import urllib
import chardet
import thread
import threading

from bs4 import BeautifulSoup
import sys
import re

myLock = threading.RLock()

class baiduSpyder(object):
    pageCount = 1
    base_url = 'http://www.baidu.com/s?wd=keyword'
    req_header = {'User-Agent':'Mozilla/5.0(Windows;U;Windows NT 6.1;en-US; rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'}
    
    def __init__(self, inKey):
        self.inKey = inKey
        baiduSpyder.base_url = baiduSpyder.base_url.replace('keyword', self.inKey)

    #identify the coding of result page
    def __identifyCoding(self,inUrl):
        htmlPage = urllib.urlopen(inUrl).info()
        coding = htmlPage.getparam('charset')
        if coding is None:
            htmlPage = urllib.urlopen(inUrl).read()
            coding = chardet.detect(htmlPage)['encoding']
            if coding is None:
                coding = 'utf-8'
        
        coding = coding.lower()
        return coding
    
    #get the result page title
    def __getTitle(self,inUrl):
        coding = self.__identifyCoding(inUrl)
        try:
            titlereq = urllib2.Request(inUrl, None, self.req_header)
            titles = urllib2.urlopen(titlereq)
            htmlPage = titles.read()
            titleBS = BeautifulSoup(htmlPage.decode(coding, 'ignore'), "html.parser")
            title = titleBS.title.string
            return title
        except urllib2.HTTPError:
            return None
        except urllib2.URLError:
            return None
    
    #get info of result page
    def __getInfo(self,inUrl):
        #myLock.acquire()
        with open('result.txt', mode='a') as r_file:
            title = self.__getTitle(inUrl)
            if title:
                print title.encode('utf-8','ignore')
                r_file.write(title.encode('utf-8','ignore') + '\n')
                r_file.write(inUrl + '\n\n')
            else:
                print "No result for URL:" + inUrl
        #myLock.release()
    
    def __traverseUrl(self,inUrl):
        if self.pageCount > 5:
            return
        else:
            req =  urllib2.Request(inUrl, None, self.req_header)
            res = urllib2.urlopen(req)
            htmlPage = res.read()
            htmlBS = BeautifulSoup(htmlPage.decode('utf-8', 'ignore'), "html.parser")
            
            htmlList = htmlBS.find_all('h3')
            print 'Page ' + str(self.pageCount) + ' results:'
            for hh in htmlList:
                urlInPage = hh.a.get('href')
                try:
                    req = urllib2.Request(urlInPage, None, self.req_header)
                    readUrl = urllib2.urlopen(req).geturl()
                except urllib2.HTTPError:
                    readUrl = urlInPage
                
                print'url: ' + readUrl
                #thread.start_new_thread(self.__getInfo, (readUrl,))
                self.__getInfo(readUrl)
            
            self.pageCount += 1
            pNode = htmlBS.find_all('span', text=self.pageCount)
            #print pNode[1].parent.get('href')
            nextUrl = 'http://www.baidu.com' + pNode[1].parent.get('href')
            self.__traverseUrl(nextUrl)
            
    def ParseUrl(self):
        self.__traverseUrl(baiduSpyder.base_url)

if __name__ == '__main__':
    inKey = baiduSpyder("纸白银")
    inKey.ParseUrl()
                    
                
        