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


connection = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
connection.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 
db = connection

class gp():  
    keys=[]
    connection = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
    connection.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 
    db = connection
    def start_getpage_requests(self):
        collection = self.connection['codes']
        tbs = collection.find().sort([('tstask', pymongo.ASCENDING)]).limit(100)
        i = 0
        x1={}
        for x in tbs:
            if  'code' in x.keys() and x['code']  != "":
                if 'tstask' in x.keys():
                    task = int(x['tstask'])+1
                else:
                    task=1
                collection.update({'_id': ObjectId(x['_id'])},  {'$set': {"aktask": task}}) 
                i+=1
                code = x['code'][2:]
                #set startdate
                days =440
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
                                row['datatime']=queryStr+' '+row['time']
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
        row  =None#collection.find_one(item)
        if row==None:       
            collection.insert(dict(item))
        else:
            print(key+"yet!")

if __name__ == '__main__':
    gp = gp()
    gp.start_getpage_requests()

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
   
