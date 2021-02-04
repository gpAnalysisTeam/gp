## -*- coding: utf-8 -*-
import time
import datetime
import re
import random
import sys
import pymongo
import numpy as np

import math
from config import mongodbConfig
import common as cm
from collections import Counter


from prettytable import PrettyTable
# reload(sys)
# sys.setdefaultencoding('utf8')
db = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
db.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 

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

def cosine_similarity(x, y, norm=False):
    """计算两个向量x和y的余弦相似度 """
    assert len(x) == len(y), "len(x) != len(y)"
    zero_list = [0] * len(x)
    if x == zero_list or y == zero_list:
        return float(1) if x == y else float(0)
    ##add wyq
    x = tonear1num(x)
    y = tonear1num(y)
    ##end wyq
    # method 1
    res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
    cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))
    return 0.5 * cos + 0.5 if norm else cos  # 归一化到[0, 1]区间内

"""
30 day data similarity
"""

def day30similarity(templete):
    codes=cm.codes()
    templeteData=cm.getBefor30DaysKData(templete)
    similarityValue = []
    for code in codes:
        if code['code']!=templete:
            codeXdada=cm.getBefor30DaysKData(code['code'])
            if len(templeteData)!=len(codeXdada):
                print(code['code'])
            else:
                t= cosine_similarity(templeteData,codeXdada) 
                similarityValue.append([code['title'],code['code'],t])
    similarityValue.sort(key = lambda similarityValue:similarityValue[1], reverse=True)
    return similarityValue

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
            t= cosine_similarity(templeteData,codeXdada) 
            similarityValue.append([code['title'],code['code'],t,codeXdada])
    similarityValue.sort(key = lambda x: x[2], reverse=True)
    return similarityValue

def data_insert(item,type='cos'):   
    """
    记录计算结果
    """
    item['type']=type
    collection = db['cos']          
    row  =collection.find_one(item)
    if row==None:       
        collection.insert(dict(item))
    else:
        print("yet!")

"""
清除计算结果
"""
db['cos'].delete_many({})

"""
找到匹配模板的目标
联合akshare_transaction_data.py
"""
for j  in range(1,3):
    data = [100+j*i*3 for i in range(1,10)]
    #data = [100-j*i*3 for i in range(1,10)]
    similarityValue = dayXSimilarity(data)
    title=['e1','e2','e3']
    title.extend(data)
    table = PrettyTable(title)
    title=  map ( str ,title)

    for row in similarityValue[:40]:
        test=[row[0],row[1],row[2]]
        test.extend(row[3])
        table.add_row(test)
        """
        记录计算结果        
        """
        if j ==1:
            data_insert({'code':row[1],'name':row[0],'sim':row[2]})
            # s = table.get_csv_string()
            # with open('./tmp/stable.csv','w+') as f:
            #     f.write(s)
    print("\ntotal analysis:"+str(len(similarityValue)))   
    print(table)



    
