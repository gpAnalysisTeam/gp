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


def bit_product_sum(x, y):
    return sum([item[0] * item[1] for item in zip(x, y)])

def tonear1num(arrList):
    avgNum = sum(arrList)/len(arrList)
    minNum = min(arrList)
    list=[]
    for item in arrList:
        v= round((item-minNum+0.0001)/avgNum,4)
        list.append(v)
    return list


def pearsonrSim(x,y):
    '''
    皮尔森相似度
    '''
    x = tonear1num(x)
    y = tonear1num(y)
    return pearsonr(x,y)[0]

"""
计算一组数据与数据库中数据的相似结果 xdata similarity
"""
def dayXSimilarity(templeteData):
    days = len(templeteData)
    codes=cm.codes()
    similarityValue = []
    for code in codes:
        codeXdada=cm.getBeforXDaysKData(code['code'],days)
        if len(templeteData)!=len(codeXdada):
            continue
            #print("'"+code['code']+"',",end='')
        else:
            t= pearsonrSim(templeteData,codeXdada) 
            similarityValue.append([code['title'],code['code'],t,codeXdada])
    similarityValue.sort(key = lambda x: x[2], reverse=True)
    return similarityValue

"""
找到匹配模板的目标
联合akshare_transaction_data.py
"""
for j  in range(1,3):
    data = [100+j*i*1 for i in range(1,10)]
    similarityValue = dayXSimilarity(data)
    title=['e1','e2','e3']
    title.extend(data)
    table = PrettyTable(title)
    title=  map ( str ,title)
    for row in similarityValue[:40]:
        test=[row[0],row[1],row[2]]
        test.extend(row[3])
        table.add_row(test)
    print("\ntotal analysis:"+str(len(similarityValue)))
    print(table)



    
