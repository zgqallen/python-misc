#-*-coding=utf-8-*-

import urllib2
import urllib
import cookielib

from bs4 import BeautifulSoup
import sys
import re

class moonsonSpyder(object):
    root_url='https://monsoon.mo.sap.corp/'
    base_url = 'https://monsoon.mo.sap.corp/organizations/project'
    login_url = 'https://monsoon.mo.sap.corp/auth/authority/callback'
    req_header = {'User-Agent':'Mozilla/5.0(Windows;U;Windows NT 6.1;en-US; rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'}
    
    def __init__(self, inPro, userName, passWord, resultFile):
        self.inPro = inPro
        self.userName = userName
        self.passWord = passWord
        self.resultFile = resultFile
        self.base_url = self.base_url.replace('project', self.inPro)
        
        # Enable cookie support for urllib2
        cookiejar = cookielib.CookieJar()
        self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    
    def __login(self):
        authinfo = {"uid":self.userName, "password":self.passWord}
        data = urllib.urlencode(authinfo)
        
        req = urllib2.Request(self.login_url, data, self.req_header)
        res = self.urlOpener.open(req)
        htmlPage = res.read()
    
    def __parseSubPage(self, inUrl, owner):
        res = self.urlOpener.open(inUrl)
        htmlPage = res.read()
        htmlBS = BeautifulSoup(htmlPage.decode('utf-8', 'ignore'), "html.parser")
         
        Contents = htmlBS.body.contents[1].contents[5].contents[1].contents[7]
        for link in Contents.find_all('a'):
            url = self.root_url+link.get('href')
            link['href'] = url
        
        #print Contents
        with open(self.resultFile, mode='a') as r_file:
           r_file.write(str(Contents))
        
        # 
        pagiNation = htmlBS.body.find("div", {"class":"pagination"})
        if(pagiNation != None):
            nextp = pagiNation.find(rel="next")
            if(nextp != None):
                nexturl = self.root_url+nextp.get('href')
                #print nexturl
                self.__parseSubPage(nexturl, owner)

    def __setResultHtml(self):
        #print "<style>\n table {\nborder-collapse: collapse;\n}\ntable, td, th {\nborder: 1px solid black;\n}\n</style>"
        with open(self.resultFile, mode='a') as r_file:
            r_file.write("<style>\n table {\nborder-collapse: collapse;\n}\ntable, td, th {\nborder: 1px solid black;\n}\n</style>")
        
    def __getMainPage(self, inUrl):
        res = self.urlOpener.open(self.base_url)
        htmlPage = res.read()
        htmlBS = BeautifulSoup(htmlPage.decode('utf-8', 'ignore'), "html.parser")
        #body -> class wrap 1 -> class content 5 -> class container 1 -> class row 9 -> class listing listing-fancy projects 1
        Contents = htmlBS.body.contents[1].contents[5].contents[1].contents[9].contents[1]
                  
        #print Contents
        for link in Contents.find_all('a'):
            suburl = self.root_url+link.get('href')
            #print "<b><p>----------------  Owner:[" + link.string + "], URL:[<a href='" + suburl + "'>" + suburl + "</a>]-----------</p></b>"
            with open(self.resultFile, mode='a') as r_file:
                r_file.write("<b><p>----------------  Owner:[" + link.string + "], URL:[<a href='" + suburl + "'>" + suburl + "</a>]-----------</p></b>")
            self.__parseSubPage(suburl,link.string)
        
    def Parse(self):
        self.__login()
        self.__setResultHtml()
        self.__getMainPage(self.base_url)   

if __name__ == '__main__':
    Instance = moonsonSpyder('customhadr','I310269','zgq@22365201986','customhadr.html')
    Instance.Parse()