import time
import datetime
import re
import random
import sys
import pymongo
import numpy as np

import math
from config import mongodbConfig
from collections import Counter


class db():
    def conn(self):
        conn = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
        conn.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1')  
        return conn
dbInit = db()

def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]
def euclidean(p, q):
    # 如果两数据集数目不同，计算两者之间都对应有的数
    same = 0
    for i in p:
        if i in q:
            same += 1
 
    # 计算欧几里德距离,并将其标准化
    e = sum([(p[i] - q[i]) ** 2 for i in range(same)])
    return 1 / (1 + e ** .5)

def pearson(p,q):
#只计算两者共同有的
    same = 0
    for i in p:
        if i in q:
            same +=1

    n = same
    #分别求p，q的和
    sumx = sum([p[i] for i in range(n)])
    sumy = sum([q[i] for i in range(n)])
    #分别求出p，q的平方和
    sumxsq = sum([p[i]**2 for i in range(n)])
    sumysq = sum([q[i]**2 for i in range(n)])
    #求出p，q的乘积和
    sumxy = sum([p[i]*q[i] for i in range(n)])
    # print sumxy
    #求出pearson相关系数
    up = sumxy - sumx*sumy/n
    down = ((sumxsq - pow(sumxsq,2)/n)*(sumysq - pow(sumysq,2)/n))**.5
    #若down为零则不能计算，return 0
    if down == 0 :return 0
    r = up/down
    return r
a=[80,100,90,71]
b=[8,1,5,11]
t = pearson(a,b)
t = 0


"""
order: every 15minute avg value 
"""
class datas15():
    minuteArr = [m for m in range(60)]
    minuteGroup =list_split(minuteArr,15)
    def getPieceNameByTime(self,timesteam):       
        time_array = time.localtime(timesteam)
        prefix =time.strftime("%Y-%m-%d %H@",time_array)
        minuteCurrent = int(time.strftime("%M",time_array))
        # minuteCurrent=45
        key = 0
        for i in range(len(self.minuteGroup)):
            if minuteCurrent in self.minuteGroup[i]:
                key=i+1
                break
        return prefix+str(key)             

    def group15(self,code):
        connect = db().conn()[code]
        rows = connect.find().sort([('pubtime', pymongo.DESCENDING)]).limit(5000)
        ##############group ###########################
        data={}
        for row in rows:
            dataMinuteGroup=self.getPieceNameByTime(int(row['pubtime']))
            if dataMinuteGroup in data.keys():
                data[dataMinuteGroup].append({"pubtime":row['pubtime'],"price":row['price'],"volumn":row['volume']})
            else :
                data[dataMinuteGroup]=[{"pubtime":row['pubtime'],"price":row['price'],"volumn":row['volume']}]
        return data


    def wordsWenziList(self,code):
        connect = db().conn()['words_wenzi']
        modelList = self.get4TapsBy15Minute(code)
        modelLen = len(modelList)

        for i in range(0,modelLen):
            modelKeyCount = Counter(modelList[i][1])
            if modelKeyCount[0]<2:
                modelSelect = modelList[i][1]
                modelDateTimeSelect = modelList[i][0]
                break

       # modelSelect=[4,3,2,1]
        rows = connect.find()
        data=[]
        times=0
        for row in rows:
            q=[]
            for indes,ch in enumerate(str(row['pattern'])):
                try:
                    q.append(int(ch))
                except:
                    continue               
            if q and 'pattern' in row.keys() and 'words' in row.keys() :                       
                releas = euclidean(modelSelect, q)
                if 'des' not in row.keys():   
                       row['des'] = row['words']
                data.append([releas,row['pattern'],row['words'],row['des']])
                times=times+1
                if times==6 :
                    break
        data.sort(key = lambda data:data[0], reverse=True)
        return {'modelDateTimeSelect':modelDateTimeSelect,'data':data,'modelList':modelList} 

    def get4TapsBy15Minute(self,code):
        #### get price and group by 15minute
        data = self.group15(code)
        #### get group's  avg price  
        avgList = []        
        for group in data:
            priceList = [float(row['price']) for row in data[group] ]
            while 0.0 in priceList:
                priceList.remove(0.0)
            if not priceList:
                continue
            max1 = max(priceList)     
            min1 = min(priceList)
            avg =round((max1+min1)/2,2)
            if max1>0 and min1>0 and avg>0:
                avgList.append([group,avg]) 
        
        #15minute group by 4
        # group15_4=list_split(avgList, 4)
        group15_4={}
        for quarter in avgList:
            splitList = quarter[0].split('@', 1 )
            key = splitList[0]
            if key in group15_4.keys():
                group15_4[key].append(quarter)
            else :
                group15_4[key]=[quarter]

        ##################################
        taps=[]
        for i  in group15_4.keys():
            piece=','
            arr=self.calculate15_4(group15_4[i])
            num_list_new = [str(x) for x in arr]
            arrStr=piece.join(num_list_new)
            taps.append([i,arr,group15_4[i],arrStr])
        return taps

    def calculate15_4(self,group15_4):
        oldGroup15_4 = list(np.array(group15_4).T[1])
        newGroup15_4= list(np.array(group15_4).T[1])
        newGroup15_4.sort()
        model =  [ newGroup15_4.index(num)+1 for num in oldGroup15_4]   
        ##pad
        oldGroup15_4KeyList = list(np.array(group15_4).T[0])
        dateKeysList = []
        for dateKey in oldGroup15_4KeyList:
            dateKeysplitList = dateKey.split('@', 1 )
            dateKeysList.append(int(dateKeysplitList[1]))
        for i in range(4):
            if i+1 not in dateKeysList:
                model.insert(i,0)
        return model
         

# demo = datas15()
# demo.words_wenziList('sh601003')