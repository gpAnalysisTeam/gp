import time
import datetime
import re
import random
import sys
import pymongo
import math
from config import mongodbConfig

from pyecharts.charts import Page,Bar,WordCloud,EffectScatter,Scatter
from pyecharts import options as opts
    # 内置主题类型可查看 pyecharts.globals.ThemeType
from pyecharts.globals import ThemeType
from pyecharts.faker import Faker

connection = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
connection.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 

def getOneDayData(code,startTime):    
    collection = connection[code]
    rows = collection.find({"v0":{'$regex':startTime+".*"}}).sort([('id', pymongo.ASCENDING)]) 
    return rows
def oneDataMinAndMaxPrice(code,startTime):
    oneDayData = getOneDayData(code,startTime)
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
def getAllData(code):    
    collection = connection[code]
    rows = collection.find().sort([('id', pymongo.ASCENDING)]) 
    data=[]
    for i in rows:        
        if float(i['v1'])>2:
            data.append(i)
    return data
def showHotX(id,code,flag=0):
    #publish 
    templete = 'hot/'+str(id)+'.html'
    id= int(id)
    if id==1:
        templete = ''      
    elif id==4:
        templete = ''

    return templete