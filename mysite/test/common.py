import time
import datetime
import re
import random
import sys
import pymongo
import math
from config import mongodbConfig

connection = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
connection.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 

def industryHot():
    collection = connection['industry']
    industryList = collection.find().sort([('datetime', pymongo.DESCENDING),('percent', pymongo.DESCENDING)]).limit(9) 
    return industryList

def codes():
    collection = connection['codes']
    myquery = { "is_on":  1,"title":{'$nin':["sh","sz"]}} 
    codes = collection.find(myquery).sort([('id', pymongo.DESCENDING)]) 
    data=[]
    for code in codes:        
        try:
            if 'name' in code.keys() and code['name'] !='':
                code['title']=code['name']
            if 'title' not in code.keys() and 'name' not in code.keys():
                continue
            dick={'title':code['title'],'code':code['code']}
            data.append(dick)
        except :
            continue       
        
    return data
def getBefor30DaysKData(code):
    collection = connection['k'+code]
    #
    days =30
    rows = collection.find().sort([('datetime', pymongo.DESCENDING)]).limit(days)
    data = [row['close'] for row in rows]
    data.reverse()
    return data

def getBeforXDaysKData(code,days):
    collection = connection['k'+code]
    rows = collection.find().sort([('datetime', pymongo.DESCENDING)]).limit(days)
    data = [row['close'] for row in rows]
    data.reverse()
    return data