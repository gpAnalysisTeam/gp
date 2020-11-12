import time
import datetime
import re
import random
import sys
import pymongo
import math
from config import mongodbConfig

from bson.objectid import ObjectId

from pyecharts.charts import Page,Bar,WordCloud,EffectScatter,Scatter
from pyecharts import options as opts
    # 内置主题类型可查看 pyecharts.globals.ThemeType
from pyecharts.globals import ThemeType
from pyecharts.faker import Faker

class hot():
    connection = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
    connection.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 

    def codes(self):
        collection = self.connection['codes']
        codes = collection.find().sort([('id', pymongo.ASCENDING)]) 
        return codes

    def getOneDayData(self,code,startTime):    
        collection = self.connection[code]
        rows = collection.find({"v0":{'$regex':startTime+".*"}}).sort([('id', pymongo.ASCENDING)]) 
        return rows
    def oneDataMinAndMaxPrice(self,code,startTime):
        oneDayData = self.getOneDayData(code,startTime)
        min={'value':999,'time':''}
        max={'value':0,'time':''}
        for i in oneDayData:
            if float(i['v1'])<2:
                continue

            if float(i['v1'])>max['value']:
                max={'value':round(float(i['v1']),2),'time':i['v0']}
            if float(i['v1'])<min['value']:
                min={'value':round(float(i['v1']),2),'time':i['v0']}
        if min['value']==999 or  max['value']==0:
            return None
        else:
            return {'min':min,'max':max}
    def getAllData(self,code,startTime='2020-6-1'):    
        collection = self.connection[code]
        rows = collection.find().sort([('id', pymongo.ASCENDING)]) 
        data=[]
        for i in rows:      
            if 'pubtime' not in i.keys():
                timeSteam= datetime.datetime.strptime(i['v0'],'%Y-%m-%d %H:%M:%S')
                v0time= int(time.mktime(timeSteam.timetuple()))
                collection.update({'_id': ObjectId(i['_id'])},  {'$set': {"pubtime": v0time}}) 
            if float(i['v1'])>2:
                data.append(i)
        return data
    def showHotX(self,id,code,flag=0):
        #publish 
        return 1
    def reset(self,code,mins):    
        codeList = self.codes() 
        for code in codeList:
            self.getAllData(code['code'])
        return [code,mins]
#
hot = hot()

