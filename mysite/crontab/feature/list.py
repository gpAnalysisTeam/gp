# -*- coding: UTF-8 -*-
# Get all product information for taobao.com
import json
import urllib
import sys
import pymongo
from config import mongodbConfig,sysConfig
import common as cm
import datetime
from prettytable import PrettyTable
from xpinyin import Pinyin

db = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
db.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 
coss = db['cos'].find().sort([('sim', pymongo.DESCENDING)]).limit(50) 
p = Pinyin()

def timestamp2string(timeStamp,format="%Y-%m-%d %H:%M"):
    try:
        d = datetime.datetime.fromtimestamp(timeStamp)
        str1 = d.strftime(format)
        return str1
    except Exception as e:
        print(e)


def codeXfeature(c):
    one =  db[c].find_one(sort=[('pubtime', pymongo.DESCENDING)])
    end = one['pubtime']
    start = one['pubtime']-3600*24*1+3600
    query={"pubtime":{'$gte':start,'$lte':end}}
    detailList = db[c].find(query).sort([('pubtime', pymongo.ASCENDING)])
    # put data in to minute dic
    minuteDic={}
    for ltem in detailList:
        ym=timestamp2string(ltem['pubtime'])
        if ym in minuteDic.keys():
            minuteDic[ym].append(ltem)
        else:
            minuteDic[ym]=[ltem]
    #
    stStart = timestamp2string(one['pubtime'],"%Y-%m-%d 09:00:00")
    d = datetime.datetime.strptime(stStart, "%Y-%m-%d %H:%M:%S")   
    dataGroup={} 
    
    for i in range(0,6):        
        for j in range(0,61):
            startStream =d + datetime.timedelta(minutes=60*i+j)
            dataFix = startStream.strftime('%Y-%m-%d %H:%M')
            fix = startStream.strftime("%H")
            if j >=0 and j<10:
                fix=fix+'0010'
            elif j >=10 and j<20:
                fix=fix+'1020'
            elif j >=20 and j<30:
                fix=fix+'2030'
            elif j >=30 and j<40:
                fix=fix+'3040'
            elif j >=40 and j<50:
                fix=fix+'4050'
            elif j >=50 and j<=60:
                fix=fix+'5060'
            else:
                continue
            fix = int(fix)
            if dataFix in minuteDic.keys():
                if fix in dataGroup.keys():
                    dataGroup[fix].extend(minuteDic[dataFix])
                else:
                    dataGroup[fix]=minuteDic[dataFix]
    ct={} 
    for i in dataGroup:
        ct[i]=len(dataGroup[i])   
    return ct

data=[]
for code in coss:
    try:
        featureValueBuf = codeXfeature(code['code'])
        row = {'name':code['name'],'code':code['code']}
        row.update(featureValueBuf)
        data.append(row)
    except :
        continue
#normal
i=0
for ltem in data:
    if ltem==None:
        continue
    value_list = list(ltem.values())
    if len(value_list)!=29:
        continue
    if i==0:
        table = PrettyTable(ltem.keys())
    i=i+1
    table.add_row(value_list)
print(table)

#special
i=0
similarityValue=[]
for ltem in data:
    if ltem==None:
        continue
    value_list = list(ltem.values())
    if len(value_list)!=29:
        continue
    if i==0:
        special = PrettyTable(ltem.keys())
    i=i+1
    filterAr = value_list[3:27]
    avg = sum(filterAr) / len(filterAr)
    if avg <140:
        continue
    special.add_row(value_list)
    similarityValue.append(value_list)
print(special)

s=[]
query=[]
fileGp='/root/gp/do/gp.sh'
fileQuery='/root/gp/do/query.sh'
listGPStr=open(fileGp).read()
listQueryStr=open(fileQuery).read()
for row in similarityValue[:20]:
    ucName = p.get_initials(row[0], u'')

    if ucName[:1]=='*' or ucName[:2]=='ST'  or row[0][:1]=='S' :
        continue
    
    if ucName  not in listQueryStr:
        query.append(f"/usr/bin/curl -s  \"${ucName}\" |/bin/awk -F , '"+"{print  $4  \"test2\" \"----\"  $11/1000 \"----\" $21/1000 \"%"+ucName+"net\" $2}'")
    
    if ucName  not in listGPStr:
        s.append(f"export {ucName}=\"http://hq.sinajs.cn/list={row[1]}\"")
    
with open(fileGp,'a+') as f:
    text = '\n'.join(s)
    f.write('\n'+text)
    f.close
with open(fileQuery,'a+') as f:
    text = '\n'.join(query)
    f.write('\n'+text)
    f.close

