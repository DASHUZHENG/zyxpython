# -*- coding: utf-8 -*-
import logging
import os
import datetime
import time


from zdownloader import ZDownload
from zfilter import ZFilter
from zcrawler import ZCrawler
from zanalyser import ZAnalyser
from zcache2 import ZCache
from zdatabase import ZDownData

url='http://www.yszygou.com/forum-42-1.html'


#Downloader Start

cache=ZCache(category=2,parameters={"doc":{"category": "URL", "folder":"ha","surfix":""}})

downloader=ZDownload(cache=cache)


#Filter Start
filter1=ZFilter(method="BS4",parameters={"base_url":"http://www.yszygou.com/","re_filter":"http://www.yszygou.com/.*html","2nd_filter":None})


#Analyser Start

db=ZDownData("scrapy.db")
db.create_table(table="dbtest",primekey="field1",cat="TEXT")
db.add_column_not_exist(table="dbtest",newkey="field2",cat="TEXT")
db.add_column_not_exist(table="dbtest",newkey="field3",cat="TEXT")  


parameters={"doc":{"category": None, "folder":"abc","surfix":".txt"},"db":{"db":db,"info":{"table":"dbtest","key":"field1","att":["field2","field3"]}}} 
Z1=ZCache(7,parameters)



analyser1=ZAnalyser(method="GEN",parameters={"re_filter":[b"(pan.baidu.com.*)\" target.*\xc3\xdc\xc2\xeb:\s+(\w{4}|<)"],"bs4_filter":["title"]},cache=Z1)
#analyser1=ZAnalyser(method="RE",parameters={"re_filter":[b"(pan.baidu.com.*)\" target.*(\xc3\xdc\xc2\xeb:\s+.*)<?"],"bs4_filter":["title"]})    
#def __init__(self,method="RE",parameters={"re_filter":["*"],"bs4_filter":["title"],"match_filter":["*"]},cache=None):



#Crawler Start    
crawler=ZCrawler(downloader,filter1,analyser1)

#def __init__(self,downloader,link_filter=None,link_analyser=None):



#Start to crawl the net!

for a in range(1,6):
    
    baseurl="http://www.yszygou.com/forum-42-%s.html" % a

    print "crawler test", a

    crawler(baseurl,1,-1)


#<strong>链接: <a href="https://pan.baidu.com/s/1c1KySiW" target="_blank">https://pan.baidu.com/s/1c1KySiW</a> 密码: prbv</strong><br />
#链接: <a href="https://pan.baidu.com/s/1bpwosiz" target="_blank">https://pan.baidu.com/s/1bpwosiz</a> 密码: <div class="locked">





