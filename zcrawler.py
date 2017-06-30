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


from zcache2 import ZCache
from zdatabase import ZDownData
from zdownloader import ZDownload
from zfilter import ZFilter
from zanalyser import ZAnalyser


class ZCrawler():

    def __init__(self,downloader,link_filter=None,link_analyser=None):
        #v1.1
        #ZCrawler is constituted with 4 parts
        #1.ZDownloader;2.ZFilter;3.ZAnalyser;
        #4.ZDossier is not defined yet

        #v1.0
        #downloader is an example of ZDownload
        #Previous self.Downloader=ZDownload(delay,agent,proxy,num_retries,use_cache,cache)

        self.Downloader=downloader

        if link_filter:

            self.link_filter=link_filter

        else:           

            self.link_filter=ZFilter(method="Default")        

            #default_filter should not be a function, but a class
            # __init__(self,method="BS4",parameters={"base_url":None,"re_filter":".","2nd_filter":None}):

        if link_analyser:

            self.analyser=link_analyser

        else:
            
            self.analyser=None



        self.crawl_queue=[]
        
        self.seen_queue={}
        #crawl_queue must has a append method
        #seen_queue must has a set&get method
          
        
    def __call__(self,url,max_depth=-1,max_iteration=-1,processes=1,threads=1,cat="LINK"):
        
        self.crawl_queue.append(url)

        self.seen_queue[url]=0
        
        
        if cat=="LINK":
            
            print("Link Crawler Started")
            
            result=self.link_crawler(url,max_depth,max_iteration)
            
        elif cat=="THREAD":
            
            print("Thread Crawler Started")
            
            result=self.threaded_crawler(url,max_depth,max_iteration,threads)
        
        elif cat=="PROCESS":
            
            print("Process Crawler Started")
            
            result=self.process_crawler(url,max_depth,max_iteration,processes,threads)
            
        else:
            
            print("Crawler Not Started")
                   
        
        
    def map_crawler(self,url):
        sitemap=download(url)
        links=re.findall('<loc>(.*?)</loc>',sitemap)
        for link in links:
            print link
        pass

        
    def link_crawler(self,seed_url,max_depth=-1,max_iteration=-1):
                
        #原始网页,scrap网页历史记录,最大数量

        crawl_queue=self.crawl_queue

        seen_queue=self.seen_queue

        #扩展记录至超出普通list和lib方法
        
        #crawl_queue.append(seed_url)

        #seen_queue[seed_url]=0
        
        count=0
        
        #循环内容
        
        while crawl_queue:  
            #深度定义
            
            while count!=max_iteration:
                #while crawl_queue
                
                try:
                    
                    url=crawl_queue.pop()
                
                except Exception,error:
                    
                    print("Pop error %s Counter to %s" % (error,count))
                    break
                
                depth=seen_queue[url]    
                
                #logging.debug("link_crawler depth=%s" % depth) 
                
                html=self.Downloader(url)

                if  self.analyser:

                    self.analyser(url,html)

                #Whether or not it needs analysis?
                
                if html:
                    
                    url_list=self.link_filter(html)
                        
                    if depth!= max_depth:
                            
                        for new_url in url_list:
                             
                            if new_url not in seen_queue:
                                #更新URL列表
                                crawl_queue.append(new_url)

                                seen_queue[new_url]=depth+1
                    
                count=count+1
                
            print("Counter to %s" % count)

            break
            
        #!!Method Refresh Cache

        #self.Downloader.cacheRefresh()
        
        #!!Method Refresh Cache       
        
    
    

    
    
    def threaded_crawler(self,seed_url,max_depth=-1,max_iteration=-1,max_thread=1):
        
        crawl_queue=self.crawl_queue

        seen_queue=self.seen_queue

        #原始网页,scrap网页历史记录,最大数量
        
        crawl_queue.append(seed_url)

        seen_queue[seed_url]=0
        
        def thread_pop():
            
            print 'thread %s is running...' % threading.current_thread().name
            
            #time.sleep(5)
            
            #print 'thread %s start up after 5s...' % threading.current_thread().name
            
            count=0
            
            while crawl_queue:  
                #深度定义
                
                while count != max_iteration:
                    #while crawl_queue
                    
                    #time.sleep(0.5)
                    
                    try:
                        url=crawl_queue.pop()
                    
                    except Exception,error:
                        
                        print("Pop error %s Counter to %s" % (error,count))
                        break
                    
                    depth=seen_queue[url]    
                    
                    #logging.debug("link_crawler depth=%s" % depth) 
                    
                    html=self.Downloader(url)
                    
                    print 'thread %s is downloading...' % threading.current_thread().name
                    
                    if  self.analyser:

                        self.analyser(url,html)


                    if html:
                        
                        url_list=self.link_filter(html)
                            
                        if depth!= max_depth:
                                
                            for new_url in url_list:
                                 
                                if new_url not in seen_queue:
                                    #更新URL列表
                                    crawl_queue.append(new_url)

                                    seen_queue[new_url]=depth+1
                        
                    count=count+1
                    
                print("%s Counter to %s" % (threading.current_thread().name,count))
                
                break
            
            print 'thread %s Done' % threading.current_thread().name    
        
        #self.Downloader.cacheRefresh()
            
            #!!Method Refresh Cache       
        
        threads=[]
        
        crawl_counter={}
        
        for num in range(0,max_thread):
            
            thread_str="Thread"+str(num)
            
            thread_name=threading.Thread(target=thread_pop,name=thread_str)
            
            threads.append(thread_name)
            
            crawl_counter[thread_str]=0
        
  
        for thread in threads:
            
            print("Thread %s Start" % thread.name)
            
            thread.start()
            
            time.sleep(20)

        for thread in threads:
            
            thread.join()    
        
        print("Threads All End")   
        


    def process_crawler(self,seed_url,max_depth=-1,max_iteration=-1,max_process=1,max_thread=1):       

        crawl_queue=multiprocessing.Queue()
        
        crawl_queue.put(seed_url)
        # Crawl Queue 记录
        
        process_m = multiprocessing.Manager()
        
        seen_queue = process_m.dict()
        
        seen_queue[seed_url]=0
        # 已爬网页记录

        
        def process_pop(crawl_queue,seen_queue):
            
            print 'process %s is running...' % os.getpid()
            
            #time.sleep(5)
            
            #print 'thread %s start up after 5s...' % threading.current_thread().name
            
            def process_thread():
                
                thread_name=str(os.getpid())+"-"+str(threading.current_thread().name)
                
                print 'thread %s is running...' % thread_name
            
                count=0
            
                while True:
                    
                    while count != max_iteration:
                        
                        url=crawl_queue.get()
                        
                        depth=seen_queue[url]    
                        
                        html=self.Downloader(url)
                        
                        print 'process %s is downloading...' % thread_name
                        
                        if html:
                            
                            url_list=self.get_links(html)
                                
                            if depth!= max_depth:
                                    
                                for new_url in url_list:
                                     
                                    if new_url not in seen_queue:
                                        #更新URL列表
                                        crawl_queue.put(new_url)
                                        seen_queue[new_url]=depth+1
                            
                        count=count+1
                    
                    print("%s Counter to %s" % (thread_name,count))
                    
                    break
            
            threads=[]
            
            crawl_counter={}
            
            for num in range(0,max_thread):
                
                thread_str="Thread"+str(num)
                
                thread_name=threading.Thread(target=process_thread,name=thread_str)
                
                threads.append(thread_name)
                
                #crawl_counter[thread_str]=0
            
      
            for thread in threads:
                
                print("Pr %s Thread %s Start" % (os.getpid(),thread.name))
                
                thread.start()
                
                time.sleep(20)
    
            for thread in threads:
                
                thread.join()    
            
            print("Threads All End")       
        
        processes=[]
        
        
        for num in range(0,max_process):
            
            process_str="Process"+str(num)
            
            pr=multiprocessing.Process(target=process_pop, args=(crawl_queue,seen_queue))
            
            processes.append(pr)
            
            
        
        for pr in processes:
            
            pr.start()
            
            time.sleep(20)
        
        for pr in processes:
        
            pr.join()
        
        #print seen_queue





        
