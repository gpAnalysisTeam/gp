# -*- coding: UTF-8 -*-
# Get all product information for taobao.com
import json
import urllib
from lxml import etree
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import re
import random
import sys
import pymongo

from bson.objectid import ObjectId
import uuid
import json
import datetime
import pyecharts
from config import mongodbConfig

class gp():  
    keys=[]
    connection = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
    connection.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 
    db = connection
    collection = connection['codes']
    tbs = collection.find().sort([('id', pymongo.DESCENDING)]).limit(30)
    i = 0
    x1={}
    for x in tbs:
        if  'code' in x.keys() and x['code']  != "":
            keys.append(x['code'])
            if 'task' in x.keys():
                task = int(x['task'])+1
            else:
                task=1
            collection.update({'_id': ObjectId(x['_id'])},  {'$set': {"task": task}}) 
            i+=1
    keys = list(set(keys))
    news_urls=[]
    DRIVER_PATH = '/usr/local/bin/chromedriver'
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')  # 
    options.add_argument('--disable-gpu')
    driver = Chrome(executable_path=DRIVER_PATH, options=options)

    def start_getpage_requests(self):
        #keys = urllib.quote(key)\
        driver = self.driver
        for key in self.keys:
            for page in range(1):     
                url="http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol="+key+"&page="+str(page+1)
                driver.get(url)
                time.sleep(random.randint(1,2 ))
                tr = driver.find_elements_by_xpath(("//table[@class='datatbl']/tbody/tr"))
                try:
                    for i in tr:
                        row = {}
                        j=i.find_elements_by_tag_name('td')
                        n=1
                        for item in j:
                            row['v'+str(n)]=item.text
                            n+=1
                        mm=i.find_elements_by_tag_name('th')
                        row['v0']=str(datetime.datetime.now().year)+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)+' '+mm[0].text
                        row['v6']=mm[1].text
                        row['v7']=mm[0].text
                        self.data_insert(key,row)
                except:
                    continue                

    def data_insert(self,key,item):       
        collist =  self.db.list_collection_names()
        if key not in collist:
            self.db[key]     
        collection = self.db[key]          
        row  =collection.find_one(item)
        if row==None:       
            collection.insert(dict(item))
        else:
            print(key+"yet!")

if __name__ == '__main__':
    gp = gp()
    i=0
    while True:
        time.sleep(3)
        i=i+1
        print(i)
        gp.start_getpage_requests()
   
