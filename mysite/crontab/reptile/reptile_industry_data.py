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
from config import mongodbConfig,sysConfig

def industryFilter(url):
    bfRow = url.split("#")
    return bfRow[1]
class reptileIndustryData():  
    db = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
    db.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 
    industryRows = db['industry'].find().sort([('id', pymongo.DESCENDING)]).limit(30)

    DRIVER_PATH = '/usr/local/bin/chromedriver'
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')  # 
    options.add_argument('--disable-gpu')
    driver = Chrome(executable_path=DRIVER_PATH, options=options)

    industryUrls=[]

    #http://finance.sina.com.cn/stock/sl/ page 
    #http://vip.stock.finance.sina.com.cn/mkt/#new_mthy detail
    def start_getpage_requests(self):
        driver = self.driver
        url="http://finance.sina.com.cn/stock/sl/"
        driver.get(url)
        WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "datatbl"))
                )
        tr = driver.find_elements_by_xpath(("//div[@class='wrap']/div[@class='tblOuter']/table[@class='datatbl']/tbody/tr"))
        
        for i in range(len(tr)):
            try:
                row = {}
                  
                text  = tr[i].text
                industryLink=tr[i].find_elements_by_xpath((".//td/a"))[0].get_attribute('href')        
                bfRow = text.split(" ")
                if 'ST' in bfRow[0]:
                    continue

                row['industry_type']=industryFilter(industryLink) 
                row['industry']=bfRow[0]
                row['num']=bfRow[1]
                row['avg_price']=bfRow[2]
                row['plus_price']=bfRow[3]
                pencent = bfRow[4][0:-1]
                row['percent']=round(float(pencent),2)
                row['volume']=bfRow[5]
                row['volume_price']=bfRow[6]
                row['top_gp_name']=bfRow[7]
                row['top_gp_code']=bfRow[8]
                row['top_gp_pencent']=bfRow[9]
                row['top_gp_price']=bfRow[10]
                row['top_gp_amount']=bfRow[11]
                row['v0']=time.strftime("%Y-%m-%d %H:0:0", time.localtime())
                timeSteam= datetime.datetime.strptime(row['v0'],'%Y-%m-%d %H:%M:%S')
                row['pubtime']  = int(time.mktime(timeSteam.timetuple()))
                self.industryPageDataInsert(row)
            except:
                print('error found!')           

#1604991603.0
    def industryPageDataInsert(self,item):       
        collection = self.db['industry']          
        row  =collection.find_one(item)
        if row==None:       
            collection.insert(dict(item))
        else:
            print("yet!")

    #
    def systemSetIndustryCodes(self):       
        driver = self.driver
        rows = self.db['industry'].find().sort([('id', pymongo.DESCENDING)]).limit(100)
        for row in rows:
            url = 'http://vip.stock.finance.sina.com.cn/mkt/#'+row['industry_type']
            driver.get(url)
            time.sleep(random.randint(1,2 ))#
            tr = driver.find_elements_by_xpath(("//div[@class='tbl_wrap']/table/tbody/tr"))
            industryType=industryFilter(url)
            
            for i in tr:
                try:
                    row = {}
                    text  = i.text                       
                    bfRow = text.split(" ")
                    row['industry']=industryType
                    row['code']  = bfRow[0]
                    row['name']  = bfRow[1]
                    self.industryDetailDataIinsert(row)
                except:
                    print('error found!')        
        return True


    #insert one industry's code_list
    def industryDetailDataIinsert(self,item):       
        collection = self.db['codes']          
        row  =collection.find_one(item)
        if row==None:       
            collection.insert(dict(item))
        else:
            print("yet!")

if __name__ == '__main__':
    rid = reptileIndustryData()
    i=0
    runtype = sysConfig.runWay # always or onetimes
    if runtype=='always':
        while True:
            i=i+1
            print(i)
            #rid.start_getpage_requests()
            rid.systemSetIndustryCodes()
            time.sleep(1)
    elif runtype=='onetimes':
        i=i+1
        print(i)
        rid.start_getpage_requests()
        rid.systemSetIndustryCodes()
   
