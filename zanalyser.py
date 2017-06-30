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


class ZAnalyser():

    def __init__(self,method="RE",parameters={"re_filter":["*"],"bs4_filter":["title"],"match_filter":["*"]},cache=None):

        #analyser re_filter is a list
        #RE with a * will return a None
        #MATCH

        #Cache is a zdb example
        
        print "Analyser Started"
        
        if method=="RE":

            self.analyser=self.re_analyser

            self.parameters=parameters

            num=0
            
            for att in parameters["re_filter"]:

                attname="att"+str(num)

                setattr(self,attname,[])  


        elif method=="BS4":

            self.analyser=self.bs4_analyser

            self.parameters=parameters

            pass      

        elif method=="MATCH":

            self.analyser=self.ma_analyser

            self.parameters=parameters

        elif method=="GEN":

            self.analyser=self.gen_analyser

            self.parameters=parameters

      
        else:           

            self.filters=default_analyser

            self.parameters={"re_filter":["*"]}

        self.cache=cache

    def __call__(self,url,html):
        
        
        result=self.analyser(html)

        print "Analyse Result:",result

        if self.cache:

            if result:

                self.cache[url]= result

            else:

                self.cache[url]="NA"

            #result
            
        #return url_list


    def re_analyser(self,html):

        result={}

        for att in self.parameters["re_filter"]:

            result=re.findall(att,html)                  

            #result[att]=re.findall(att,html)                  

        return result
       
        
    def bs4_analyser(self,html):

        bs4obj=bs4.BeautifulSoup(html)
        
        for att in self.parameters["bs4_filter"]:
    
            result=bs4obj.find_all(att)
            
            print("analyse result: %s" % result)
        
        return result     

    def gen_analyser(self,html):

        #返回一个列表,长度=bs4+

        result=[]

        bs4obj=bs4.BeautifulSoup(html)
        
        for att in self.parameters["re_filter"]:

            result.append(re.findall(att,html))                  

            #result[att]=re.findall(att,html)  

        for att in self.parameters["bs4_filter"]:
    
            result.append(bs4obj.find_all(att))
            
            #print("analyse result: %s" % result)
                     
        print result
        
        return result
       
    def ma_analyser(self,html):
        #match与db_multi匹配
        
        result=re.match(att,html)

        return result

















        
