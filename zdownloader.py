# -*- coding: utf-8 -*-
import urllib2
import re
import bs4
import urlparse
import datetime
import time
import os

import threading
import multiprocessing

import logging
import logging.config

#logging.basicConfig(level="DEBUG")
#logging.config.fileConfig("logger.config")
#logger = logging.getLogger("example01")


class ZDownload(object):
    
    def __init__(self,delay=5,agent="bergy",proxy=None,num_retries=1,cache=None):
        
        self.throttle=Throttle(delay)

        self.agent=agent

        self.proxy=proxy

        self.num_retries=num_retries               

        self.cache=cache
        #ZCache类文件,或None

    def __call__(self,url):
        
        html=None
        
        if self.cache:
            
            try:
                html=self.cache[url]
                
                #print "Test HTML",url
                
                logging.debug("HTML LOAD")
            
            except KeyError as error:
                
                logging.info("There is no %s" % url)
               
                html=None
        
        
        if html==None: 
            
            #self.throttle.wait(url)
            
            headers={"User-agent":self.agent}
            
            html=self.download(url,headers,self.num_retries)
            
            if self.cache:
                
                self.cache[url]=html

        return html


    def download(self,url,agent="bergy",retry=2):
        
        print("Downloading Start:",url)
        
        headers={'User-agent':agent}
        
        request=urllib2.Request(url,headers=headers)

        

        try:

            html=urllib2.urlopen(request).read()
            
        except urllib2.URLError as error:
            
            logging.info("Download Error",error.reason)
            
            html=None
            
            if retry>0:

                #No URL error code
                html=self.download(url,agent,retry-1)
        
        return html
    

    def cacheRefresh(self):
        
        #更新数据库中的记录表单
        
        self.cache.refresh()
        
        
        
        
        


class Throttle():
    def __init__(self,delay):
        self.delay=delay
        self.domains={}

    def wait(self,url):
        domain=urlparse.urlparse(url).netloc
        last_accessed=self.domains.get(domain)
        if self.delay>0 and last_accessed is not None:
            timerecord=datetime.datetime.now()
            sleep_secs=self.delay-(timerecord-last_accessed).seconds
            if sleep_secs>0:
               time.sleep(sleep_secs)
        self.domains[domain]=timerecord




        
if __name__=="__main__":
    
    
    #ztest.zscrapy2_test_thread()
    ztest.zscrapy2_test_process()











