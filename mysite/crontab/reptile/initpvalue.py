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
import akshare as ak
import common as cm
"""
描述：   计算数值
是否已实现：未
缺点：。
"""

# reload(sys)
# sys.setdefaultencoding('utf8')
db = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
db.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 



def update(item): 
    del(item['_id'])      
    collection = db['codes']    
    myquery = { "code": item['code'] }
    newvalues = { "$set": item} 
    collection.update_one(myquery, newvalues)

codes = cm.codes()
"""
更新total数值
"""
for ltem in codes:
    try:
        if 'pb' in ltem.keys() and  ltem['pb']!='':
            continue
        stock= ltem['code'][2:]
        stock_financial_abstract_df = ak.stock_a_lg_indicator(stock)
        total_mv = stock_financial_abstract_df.loc[1,["total_mv"]]
        price = total_mv.total_mv
        if price>1000:
            ltem['total_mv']=price
            ltem['pe']=stock_financial_abstract_df.loc[1,["pe"]].pe
            ltem['pb']=stock_financial_abstract_df.loc[1,["pb"]].pb
            update(ltem)
    except :
        continue



    
