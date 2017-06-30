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


class ZFilter():

    def __init__(self,method="BS4",parameters={"base_url":None,"re_filter":".","2nd_filter":None}):

        if method=="BS4":

            self.filters=self.bs4_filter

            self.parameters=parameters

        else:           

            self.filters=default_filter

            self.parameters={"base_url":None,"re_filter":".","2nd_filter":None}
            

    def __call__(self,html):
        

        url_list=self.filters(html)

        
        return url_list


    def default_filter(self,html):

        #For link crawler, default filter

        link_list=[]
                        
        bs4obj=bs4.BeautifulSoup(html)                                
                        
        h2content=bs4obj.find_all("a")
                
                
        for link in h2content:

            new_url=link["href"]                    

            link_list.append(new_url)                            
                
        return link_list


    def bs4_filter(self,html):

        
        link_list=[]
        
        bs4obj=bs4.BeautifulSoup(html)
               
        h2content=bs4obj.find_all("a",href=re.compile(self.parameters["re_filter"]))
        
        url_base=self.parameters["base_url"]
        
        for link in h2content:

            new_url=urlparse.urljoin(url_base,link["href"])
            
            link_list.append(new_url)
            

        if self.parameters["2nd_filter"]:
        
            further_filter=lambda x : re.match(self.parameters["2nd_filter"],x)
        
            link_list=filter(further_filter,link_list)


        return link_list

    
        




    '''def get_links(self,html,link_filter):
        
        link_list=[]
        
        bs4obj=bs4.BeautifulSoup(html)
        
        link_list=link_filter(html)
        
        h2content=bs4obj.find_all("a",href=re.compile("^/((?!\?)(?!\:).)*$"))
        #!好的正则!
        
        url_base="http://www.eu4wiki.com"
        
        for link in h2content:
            new_url=urlparse.urljoin(url_base,link["href"])
            
            link_list.append(new_url)
            
        #暂时直接在get_links内全部过滤好
        
        eu_filter=lambda x:re.match(".+eu4",x)
        
        link_list=filter(eu_filter,link_list)
        
        return link_list



    #def links_filter(seed_url,url,link_regex):
        
        #urlparse.urljoin(seed_rul,url.a["href"])
        
        #return 1
    
    def threaded_test(self):
        
        time.sleep(1)
        
        print "haha"'''
