## -*- coding: utf-8 -*-
import time
import datetime
import re
import random
import sys
import pymongo

import numpy as np 
from scipy.stats import pearsonr,spearmanr,kendalltau

import math
from config import mongodbConfig
import common as cm
from collections import Counter

from prettytable import PrettyTable
# reload(sys)
# sys.setdefaultencoding('utf8')

"""
cos数据源
统计给定时段成果量
"""
def transactionCount(dayData):
    startTime=3600*9;
    group = 12
    piece = [int(startTime+i*3600*6/group) for i in range(group+1)]
    pieceGroup = [piece[i:i+2] for i in range(0,(group))]
    #init
    pieceData={(str(int(startTime+i*3600*6/group))+"_"+str(int(startTime+(i+1)*3600*6/group) )):0  for i in range(group)}
    for i in dayData:
        timeSteam= datetime.datetime.strptime(i['datetime'][:10],'%Y-%m-%d')
        dsecond = int(time.mktime(timeSteam.timetuple()))
        for pg in pieceGroup:
            if i['pubtime']>=(dsecond+pg[0]) and  i['pubtime']<=(dsecond+pg[1]):
                key =str(pg[0])+"_"+str(pg[1])
                pieceData[key] = pieceData[key]+1
                break
    return list(pieceData.values())


    # for i in codes[:10]:
    #     tanslateData = cm.getTanslateDateByOneDay(code,weekn)



"""
test
"""
codes = cm.coss()

titlebase=['e1','e2']
title = [ i for i in range(1,13)]
titlebase.extend(title)
table = PrettyTable(titlebase)

dateSet = '2021-02-04';
print(dateSet+' translate vol:')
for code in codes:
    translateData = cm.getTanslateDateByOneDay(code['code'],dateSet)    
    data = transactionCount(translateData)
    test=[code['title'],code['code']]
    test.extend(data)
    table.add_row(test)
print(table)
# for j  in range(1,3):
#     table = PrettyTable(title)
#     table.add_row(test)
#     print(table)



    
