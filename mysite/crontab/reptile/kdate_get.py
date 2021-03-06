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
import os
import multiprocessing

from bson.objectid import ObjectId
import uuid
import json
import datetime
from config import mongodbConfig,sysConfig

import akshare as ak
import tushare as ts
import baostock as bs
import jqdatasdk
jqdatasdk.auth("15915888476","Benben123")

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

"""
获取15分数据并保存
"""

connection = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
connection.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 
db = connection

class gp():  
    days=30
    historyData=[]
    keys=[]
    connection = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
    connection.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 
    db = connection
    def start_getK(self):
        #get_hist_data
        collection = self.connection['codes']
        tbs = collection.find({"is_on":1}).sort([('aktask', pymongo.ASCENDING)]).limit(2000)
        j = 0
        x1={}
        # pro = ts.pro_api()
        for x in tbs:
            # collection.update({'_id': ObjectId(x['_id'])},  {'$set': {"is_on": 1}}) 
            # continue

            if  'code' in x.keys() and x['code']  != "":
                if 'aktask' in x.keys() and x['aktask']!=None:
                    task = int(x['aktask'])+1
                else:
                    task=1
                self.connection['codes'].update({'_id': ObjectId(x['_id'])},  {'$set': {"aktask": task}}) 
                j+=1
                print(j)
                code = x['code'][2:]
                #set startdate 
                try:                    
                    df=jqdatasdk.get_bars(security=jqdatasdk.normalize_code(code), count=17, unit='15m',fields=['date','open','high','low','close'],
         include_now=False, end_dt=None, fq_ref_date=None,df=True)                                          
                    try:
                        #tests  = json.loads(df.to_json(orient='records'))    
                        allKD = []  
                        for row in df.iterrows():
                            line = row[1].to_dict()
                            allKD.append(line)
                        allKD.reverse()
                        i=0        
                        for row in allKD:
                            self.data_insert('k15'+x['code'],row)             
                    except :
                        #collection.update({'_id': ObjectId(x['_id'])},  {'$set': {"aktask": (task-1)}}) 
                        print(x['code']+'error!')
                        continue
                except :
                    if 'aktaskerror' in x.keys():
                        aktaskerror = int(x['aktaskerror'])+1
                    else: 
                        aktaskerror=1
                    collection.update({'_id': ObjectId(x['_id'])},  {'$set': {"aktaskerror": (aktaskerror+1)}}) 
                    print(x['code']+'error!')
                    continue
        return True
        

    def start_getpage_requests(self):
        collection = self.connection['cos']
        tbs = collection.find({}).sort([('sim', pymongo.DESCENDING)]).limit(100)
        j = 0
        x1={}
        for x in tbs:
            tb=x['code']
            if  'code' in x.keys() and x['code']  != "":
                if 'task' in x.keys():
                    task = int(x['task'])+1
                else:
                    task=1
                collection.update({'code': x['code']},  {'$set': {"task": task}}) 
                j+=1                
                code = x['code'][2:]
                print(str(j)+"/"+code)
                #set startdate
                days = 2
                startStream = datetime.datetime.now() - datetime.timedelta(days)

                for i in range(days+1):
                    try:
                        dateTime = (startStream+datetime.timedelta(i))
                        timeArray = dateTime.timetuple()
                        queryStr = time.strftime("%Y-%m-%d",timeArray)
                        print(queryStr)
                        #'2020-11-16',
                        df = ts.get_tick_data(code,date=queryStr,src='tt')

                        ###dateTime
                        startTime=0
                        timeArray = time.strptime(queryStr, "%Y-%m-%d")
                        startTime = int(time.mktime(timeArray))

                        collection = self.db[tb] 
                        rows  =collection.find({"pubtime":{'$gte':startTime},"pubtime":{'$lte':(startTime+3600*24)}})
                        rowsDt=[]
                        for x in rows:
                            rowsDt.append(x['pubtime'])

                        try:
                            tests  = json.loads(df.to_json(orient='records'))
                            for row in tests:
                                row['datetime']=queryStr+' '+row['time']         
                                dataStr =  row['datetime']                                              
                                timeSteam= datetime.datetime.strptime(dataStr,'%Y-%m-%d %H:%M:%S')
                                row['pubtime']  = int(time.mktime(timeSteam.timetuple()))
                                if row['pubtime'] in rowsDt:
                                    continue
                                self.data_insert(tb,row)
                        
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

    def clear_oldK(self):
        collection = self.connection['codes']
        tbs = collection.find({"is_on":1}).sort([('task', pymongo.ASCENDING)]).limit(500)
        i = 0

        for x in tbs:
            tb=x['code']
            kCollection = self.connection['k15'+tb]
            days = 200
            startStream = datetime.datetime.now() - datetime.timedelta(days)
            dateTime = (startStream+datetime.timedelta(i))
            timeArray = dateTime.timetuple()
            startTime = time.strftime("%Y-%m-%d",timeArray)

            query = {"datetime":{'$lte':startTime}}
            kCollection.delete_many(query)

"""
Suggest:
step0 :this gp.start_getK
step1: test daysimilarycos.py 
step2: this start_getpage_requests
step3 web show them
"""
if __name__ == '__main__':
    gp = gp()    
    #gp.start_getpage_requests()
    #print("######start_getpage_requests complete")
    """
    renew kdata
    """
    gp.start_getK()
    #print("######start_getK complete")

    """
    clear old kdata
    """
    #gp.clear_oldK()
    #print("######start_getK complete")

