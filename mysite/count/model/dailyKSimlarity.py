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

import pyecharts.options as opts
from pyecharts.charts import Line

class db():
    def conn(self):
        conn = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
        conn.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1')  
        return conn
conn = db().conn()

def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]

def calcMean(x,y):
    sum_x = sum(x)
    sum_y = sum(y)
    n = len(x)
    x_mean = float(sum_x+0.0)/n
    y_mean = float(sum_y+0.0)/n
    return x_mean,y_mean

code='sh000001'

#计算Pearson系数
def calcPearson(x,y):
    x_mean,y_mean = calcMean(x,y)	#计算x,y向量平均值
    n = len(x)
    sumTop = 0.0
    sumBottom = 0.0
    x_pow = 0.0
    y_pow = 0.0
    for i in range(n):
        sumTop += (x[i]-x_mean)*(y[i]-y_mean)
    for i in range(n):
        x_pow += math.pow(x[i]-x_mean,2)
    for i in range(n):
        y_pow += math.pow(y[i]-y_mean,2)
    sumBottom = math.sqrt(x_pow*y_pow)
    p = sumTop/sumBottom
    return p

def getOneKData(code,startTime):     
    collection = conn[code]   
    row = collection.find_one({"datetime":{'$regex':startTime+".*"}}) 
    return row

"""
order: every 10 days line simlarity
"""
class calc10DaysKSimlarity():
    def set5DayToArray(self,code,startDt,days):     
        d = datetime.datetime.strptime(startDt, '%Y-%m-%d')  
        lastData = []
        i=0
        while True:
            try:
                dateTime = d+datetime.timedelta(i)
                timeArray = dateTime.timetuple()
                queryStr = time.strftime("%Y-%m-%d",timeArray)  
                oneData = getOneKData('k'+code,queryStr)
                if oneData:
                    lastData.append(oneData['close'])
                i=i+1
                if len(lastData)==days:
                    break
                if i >=50:
                    break
            except :
                continue
        return lastData;

    def calcxDaysKSimlarity(self,code,pkCode):        
        #1,one match history;2,find the top history  
        beforDays =10
        dateTime = datetime.datetime.now() - datetime.timedelta(beforDays)
        timeArray = dateTime.timetuple()
        queryStr = time.strftime("%Y-%m-%d",timeArray)  
        target = self.set5DayToArray(code,queryStr,beforDays)

        days = beforDays
        pkDatas=[]
        for i in range(days,360*3,3):
            dateTime = datetime.datetime.now() - datetime.timedelta(i)
            timeArray = dateTime.timetuple()
            queryStr = time.strftime("%Y-%m-%d",timeArray)  
            onePieceData= self.set5DayToArray(pkCode,queryStr,days)
            try:
                pt = calcPearson(target,onePieceData)
                pkDatas.append([pkCode,pt,queryStr,onePieceData])
            except :
                continue
        #sort by pt
        pkDatas.sort(key = lambda pkDatas:pkDatas[1], reverse=True)
        simlarityData = pkDatas[:5]
        return simlarityData



demo = calc10DaysKSimlarity()
collection = conn['codes']
tbs = collection.find({"is_on":1}).sort([('task', pymongo.ASCENDING)]).limit(100)
i = 0
matchs=[]
matchsNotCode=[]
for x in tbs:
    if  'code' in x.keys() and x['code']  != "" and x['code']!=code:
        data = demo.calcxDaysKSimlarity(code,x['code'])
        matchs.append([x['code'],data])
        matchsNotCode.extend(data)
        #break

matchsNotCode.sort(key = lambda matchsNotCode:matchsNotCode[1], reverse=True)
matchsNotCodeData = matchsNotCode[:5]

print(matchsNotCodeData)
###############


"""
Gallery 使用 pyecharts 1.1.0
参考地址: https://echarts.baidu.com/examples/editor.html?c=line-stack
暂无
"""


x_data = range(len(matchsNotCodeData[0][3]))


line=Line().add_xaxis(xaxis_data=x_data)

for one in matchsNotCodeData:
    line.add_yaxis(
        series_name=one[0],
        stack="总量",
        y_axis=one[3],
        label_opts=opts.LabelOpts(is_show=False),
    )

line.set_global_opts(
    title_opts=opts.TitleOpts(title="折线图堆叠"),
    tooltip_opts=opts.TooltipOpts(trigger="axis"),
    yaxis_opts=opts.AxisOpts(
        type_="value",
        axistick_opts=opts.AxisTickOpts(is_show=True),
        splitline_opts=opts.SplitLineOpts(is_show=True),
    ),
    xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
).render("templates/count/stacked_line_chart.html")
