# -*- coding: utf-8 -*-
import urllib2
import re
import bs4
import urlparse
import datetime
import time
import os
import logging
import pickle
import random

from zdatabase import ZDownData

#logging.basicConfig(level="INFO")

class ZCache():
    
    def __init__(self,category=1,parameters={"lib":{},"doc":{},"db":{},"csv":{},"text":{}}):

        #category:
        #1 lib
        #2 document system : doc:{"category": "URL", "folder":"","surfix":""}
        #3 sqlite db:{"db":ZDb,"info":{"table":,"key":,"att":}}
        #4 csv
        #5 file
        #6 xls
        #7 multi db:{"db":ZDb,"info":{"table":,"key":,"att":[]}} att has the same length as content
        
        print("Zcache Started")

        self.category=category
        
        if category==1:

            self.setter=self.set_lib

            self.getter=self.get_lib

            self.library={}

        elif category==2:

            self.setter=self.set_doc

            self.getter=self.get_doc

            self.doc_para=parameters["doc"]

        elif category==3:

            self.setter=self.set_db

            self.getter=self.get_db

            self.db_para=parameters["db"]

            self.db=self.db_para["db"]#zdb example

            self.db_setting=self.db_para["info"]
      
        elif category==7:

            self.setter=self.set_db_multi

            self.getter=self.get_db_multi

            self.db_para=parameters["db"]

            self.db=self.db_para["db"]#zdb example

            self.db_setting=self.db_para["info"]

    #category 1 set&get

    def set_lib(self,item,content):

        self.library[item]=content

    def get_lib(self,item):

        try:
            result=self.library.get(item,0)

        except Exception,error:
                
            logging.info("Cache Get Cat%s Mistake: %s" % (self.category,error))

            result=None

        return result
        

    #category 2 set&get
    def set_doc(self,item,content):
     
        path=self.doc_path(item)
            
        folder=os.path.dirname(path)
            
        if not os.path.exists(folder):

            os.makedirs(folder)
            
            with open(path,"wb") as fp:
                
                fp.write(pickle.dumps(content))

    def get_doc(self,item):

        path=self.doc_path(item)
                  
        if os.path.exists(path):
                
            try:
                with open(path) as fp:
                        
                    result=pickle.load(fp)
                
            except Exception,error:
                    
                logging.info("Cache Get Cat%s Mistake: %s" % (self.category,error))

                result=None
            
        else:

            result=None

        return result

    def doc_path(self,item):
        #doc_path chocice

        doc_cat=self.doc_para["category"]
        
        if doc_cat=="URL":

            url_modified=self.url_to_path(item)

            path=self.doc_para["folder"]+"/"+url_modified 

        else:
        
            path=self.doc_para["folder"]+"/"+str(item)+self.doc_para["surfix"]

        return path


    def url_to_path(self,url):
        
        url_analysis=urlparse.urlsplit(url)
        
        path=url_analysis.path
        
        if not path:
            
            path="index.html"
        
        elif path[-1]==("/"):
            
            path=path + "index.html"
            
        filename=url_analysis.netloc+path+url_analysis.query
        
        logging.debug(filename)
        
        filename=re.sub('[^/0-9a-zA-Z\-.,;_]','_',filename)
        
        filename="/".join(segment[:255] for segment in filename.split("/"))
              
        return filename


    #category 3 set&get    

    def set_db(self,item,content):

        self.db.insert_not_exist(table=self.db_setting["table"],\
        primekey=self.db_setting["key"],subkey=self.db_setting["att"],\
        primecontent=item,subcontent=content)
 

    def get_db(self,item):

        try:
            da_data=self.db.extract_by_text(table=self.db_setting["table"],\

            att=self.db_setting["att"],key=self.db_setting["key"],value=item)
                
            result=da_data[0]               
                
        except Exception,error:
                
            logging.info("Cache Get Cat%s Mistake: %s" % (self.category,error))

            result=None

        return result


    #category 7 set&get    

    def set_db_multi(self,item,content):

        lens=min(len(content),len(self.db_setting["att"]))

        for num in range(0,lens):
      
            self.db.insert_not_exist(table=self.db_setting["table"],\
            primekey=self.db_setting["key"],subkey=self.db_setting["att"][num],\
            primecontent=item,subcontent=content[num])
     

    def get_db_multi(self,item):

        try:      

            da_data=self.db.extract_by_text(table=self.db_setting["table"],\

            att="*",key=self.db_setting["key"],value=item)
           
            result=list(da_data)              

            #A list plus tuple
                
        except Exception,error:
                
            logging.info("Cache Get Cat%s Mistake: %s" % (self.category,error))

            result=None

        return result
    
    #set&get
    def __getitem__(self,url):
        
        return self.getter(url)

    
    def __setitem__(self,item,content):
        
        self.setter(item,content)
            
      
    
   
    
if __name__=="__main__":

    #2 document system : doc:{"category": "URL", "folder":"","surfix":""}
    #3 sqlite db:{"db":ZDb,"info":{"table":,"key":,"att":}}

    db=ZDownData("test.db")

    db.create_table(table="dbtest",primekey="field1",cat="TEXT")

    db.add_column_not_exist(table="dbtest",newkey="field2",cat="TEXT")

    db1=ZDownData("test1.db")

    db1.create_table(table="dbtest",primekey="field1",cat="TEXT")

    db1.add_column_not_exist(table="dbtest",newkey="field2",cat="TEXT")
    db1.add_column_not_exist(table="dbtest",newkey="field3",cat="TEXT")
    
    parameters={"doc":{"category": None, "folder":"abc","surfix":".txt"},"db":{"db":db,"info":{"table":"dbtest","key":"field1","att":"field2"}}}
    parameters1={"doc":{"category": None, "folder":"abc","surfix":".txt"},"db":{"db":db1,"info":{"table":"dbtest","key":"field1","att":["field2","field3"]}}}       

    Z1=ZCache(1,parameters)

    Z2=ZCache(2,parameters)

    Z3=ZCache(3,parameters)

    Z4=ZCache(7,parameters1)
    
    
   
