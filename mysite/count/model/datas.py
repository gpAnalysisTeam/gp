import time
import datetime
import re
import random
import sys
import pymongo
import numpy as np

import math
from config import mongodbConfig
import common
import dbInit


def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]

class datas15():
    minuteArr = [m+1 for m in range(60)]
    minuteGroup =list_split(minuteArr,15)
    def getPieceNameByTime(self,timesteam):       
        time_array = time.localtime(timesteam)
        minuteCurrent = int(time.strftime("%m",time_array))
        # minuteCurrent=45
        key = 0
        for i in range(len(self.minuteGroup)):
            if minuteCurrent in self.minuteGroup[i]:
                key=i
                break
        prefix =time.strftime("%Y-%m-%d %H",time_array)
        return prefix+'#'+str(key*15)             

    def group15(self,code):
        connect = dbInit.db().conn()[code]
        rows = connect.find().sort([('v0', pymongo.ASCENDING)])
        ##############group ###########################
        data={}
        for row in rows:
            dataMinuteGroup=self.getPieceNameByTime(int(row['pubtime']))
            if dataMinuteGroup in data.keys():
                data[dataMinuteGroup].append({"pubtime":row['pubtime'],"price":row['v1'],"volumn":row['v5']})
            else :
                data[dataMinuteGroup]=[{"pubtime":row['pubtime'],"price":row['v1'],"volumn":row['v5']}]
        return data

    def get4TapsBy15Minute(self,code):
        data = self.group15(code)
        avgList = []
        
        for group in data:
            priceList = [float(row['price']) for row in data[group] ]
            max1 = max(priceList)     
            min1 = min(priceList)
            avg =round((max1+min1)/2,2)
            avgList.append(avg)
        
        #15minute group by 4
        group15_4=list_split(avgList, 4)
        taps=[]
        for i  in range(len(group15_4)):
            taps.append(self.calculate15_4(group15_4[i]))

        return True
    def calculate15_4(self,group15_4):
        group15_4Copy = group15_4
        group15_4.sort()
        

        return True
          



demo = datas15()










demo.get4TapsBy15Minute('sh601003')