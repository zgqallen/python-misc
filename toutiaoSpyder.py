'''
Created on Nov 17, 2017

@author: I310269
'''

#!/usr/bin/env python 
# -*- coding: UTF-8 -*-

import requests
import json

focusurl = 'http://www.toutiao.com/api/pc/focus/'
realtimeurl = 'https://www.toutiao.com/api/pc/realtime_news/'
hotwordsurl = 'https://www.toutiao.com/hot_words/'
hotnewurl='https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao'

def catch_focus(url):
    wbdata = requests.get(url).text
    data = json.loads(wbdata)
    news = data['data']['pc_feed_focus']
    
    for n in news:    
        title = n['title']    
        img_url = n['image_url']    
        url = n['media_url']  
        print url + "| " + title + "| " + img_url
        
def catch_realtime(url):
    wbdata = requests.get(url).text
    data = json.loads(wbdata)
    news = data['data']
    
    for n in news:    
        title = n['title']    
        img_url = n['image_url']    
        url = n['open_url']  
        print url + "| " + title + "| " + img_url
        
def catch_hotword(url):
    wbdata = requests.get(url).text
    data = json.loads(wbdata)
    for n in data:
        print n
        
def catch_hotnews(url):
    wbdata = requests.get(url).text
    data = json.loads(wbdata)
    news = data['data']
    
    for n in news: 
        abstract = n['abstract']
        
        if len(abstract) <= 0:
            continue
                     
        title = n['title']
        tag = n['chinese_tag']
 #       img_url = n['image_url']    
 #       middle_image = n['middle_image']  
        print tag + "| " + title + "| " + abstract 
            
  
if __name__ == '__main__':
    print "Focus:"
    catch_focus(focusurl)
    
    print "RealTimes:"
    catch_realtime(realtimeurl)
    
    print "Hotwords:"
    catch_hotword(hotwordsurl)
    
    print "Hot news:"
    catch_hotnews(hotnewurl)
    
    pass