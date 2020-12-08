# -*- coding: UTF-8 -*-
# Get all product information for taobao.com
import json
import urllib
import sys
import pymongo
from config import mongodbConfig,sysConfig

class GpToMongoCode():
    db = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
    db.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 
    codeRows = db['codes'].find()

    def readGpSh(self,path):
        with open(path,'r') as f :
            row={}
            for line in f.readlines():
                #get code
                line = line.strip('export  ')
                line = line.strip('"\n')  
                words = line.split('list=')
                #get title
                titleLine = line.split('="') 
                row['code']=words[1]
                row['title']=titleLine[0]
                
                self.codeDataInsert(row)

    def codeDataInsert(self,item):       
        collection = self.db['codes']          
        row  =collection.find_one(item)
        item['is_on']=1
        if row==None:       
            collection.insert(dict(item))
        else:
            print("yet!")


deam = GpToMongoCode()
deam.readGpSh('/root/gp.sh')