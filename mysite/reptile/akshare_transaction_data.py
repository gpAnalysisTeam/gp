# -*- coding: UTF-8 -*-
# Get all product information for taobao.com
import json
import urllib
from lxml import etree
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

import akshare as ak
import tushare as ts
import baostock as bs

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

#ts.set_token('195580d80938c4f6a1ffba040281f380c3888c97d1ad7a4e39a8f17a')
#lg = bs.login()

connection = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
connection.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 
db = connection

class gp():  
    keys=[]
    connection = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
    connection.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 
    db = connection
    def start_getK(self):
        #get_hist_data
        collection = self.connection['codes']
        tbs = collection.find({"is_on":1}).sort([('task', pymongo.ASCENDING)]).limit(100)
        i = 0
        x1={}
        pro = ts.pro_api()
        for x in tbs:
            if  'code' in x.keys() and x['code']  != "":
                if 'task' in x.keys():
                    task = int(x['task'])+1
                else:
                    task=1
                collection.update({'_id': ObjectId(x['_id'])},  {'$set': {"task": task}}) 
                i+=1
                print(i)
                code = x['code'][2:]
                #set startdate 
                try:
                    #df = ts.get_k_data(code,index=True)   
                    # tsCode=code+'.'+str.upper(x['code'][0:2])
                    # #df = pro.index_daily(ts_code='', start_date='20180101', end_date='20181010')
                    # df = pro.index_daily(ts_code=tsCode)
                    #################################
                    df = ak.stock_zh_index_daily_tx(symbol=x['code'])           
                    ###################################
                    # ###################################
                    print(df)                 
                    try:
                        #tests  = json.loads(df.to_json(orient='records'))
                        for row in df.iterrows():
                            line = row[1].to_dict()
                            line['datetime'] = str(row[0])
                            self.data_insert('k'+x['code'],line)                
                    except :
                        continue
                except :
                    continue
        return True
        

    def start_getpage_requests(self):
        collection = self.connection['codes']
        tbs = collection.find({"is_on":1}).sort([('task', pymongo.ASCENDING)]).limit(100)
        i = 0
        x1={}
        for x in tbs:
            if  'code' in x.keys() and x['code']  != "":
                if 'task' in x.keys():
                    task = int(x['task'])+1
                else:
                    task=1
                collection.update({'_id': ObjectId(x['_id'])},  {'$set': {"task": task}}) 
                i+=1
                print(i)
                code = x['code'][2:]
                #set startdate
                days =30
                startStream = datetime.datetime.now() - datetime.timedelta(days)

                for i in range(days+2):
                    try:
                        dateTime = (startStream+datetime.timedelta(i))
                        timeArray = dateTime.timetuple()
                        queryStr = time.strftime("%Y-%m-%d",timeArray)
                        #'2020-11-16',
                        df = ts.get_tick_data(code,date=queryStr,src='tt')
                               
                        try:
                            tests  = json.loads(df.to_json(orient='records'))
                            for row in tests:
                                row['datetime']=queryStr+' '+row['time']         
                                dataStr =  row['datetime']               
                                timeSteam= datetime.datetime.strptime(dataStr,'%Y-%m-%d %H:%M:%S')
                                row['pubtime']  = int(time.mktime(timeSteam.timetuple()))
                                self.data_insert(x['code'],row)
                        
                        except :
                            continue
                    except :
                        continue

    def data_insert(self,key,item):       
        # collist =  self.db.list_collection_names()
        # if key not in collist:
        #     self.db[key]     
        collection = self.db[key]          
        row  =collection.find_one(item)
        if row==None:       
            collection.insert(dict(item))
        else:
            print(key+"yet!")

if __name__ == '__main__':
    gp = gp()
    gp.start_getpage_requests()
    #gp.start_getK()

    # i=0
    # runtype = sysConfig.runWay # always or onetimes
    # if runtype=='always':
    #     while True:
    #        # time.sleep(3)
    #         i=i+1
    #         print(i)
    #         gp.start_getpage_requests()
    # elif runtype=='onetimes':
    #     i=i+1
    #     print(i)
    #     gp.start_getpage_requests()
   
