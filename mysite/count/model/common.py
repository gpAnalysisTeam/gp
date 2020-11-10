import time
import datetime
import re
import random
import sys
import pymongo
import math
from config import mongodbConfig

from pyecharts.charts import Page,Bar,WordCloud,EffectScatter,Scatter
from pyecharts import options as opts
    # 内置主题类型可查看 pyecharts.globals.ThemeType
from pyecharts.globals import ThemeType
from pyecharts.faker import Faker

connection = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
connection.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1') 

def codes():
    collection = connection['codes']
    codes = collection.find().sort([('id', pymongo.ASCENDING)]) 
    return codes
      
def common():
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 6, 45, 20, 35, 66])
        .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
    )
    # render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
    # 也可以传入路径参数，如 bar.render("mycharts.html")
    bar.render('templates/count/mycharts.html')
    return 'common test'

def getOneDayData(code,startTime):    
    collection = connection[code]
    rows = collection.find({"v0":{'$regex':startTime+".*"}}).sort([('id', pymongo.ASCENDING)]) 
    return rows
def oneDataMinAndMaxPrice(code,startTime):
    oneDayData = getOneDayData(code,startTime)
    min={'value':999,'time':''}
    max={'value':0,'time':''}
    for i in oneDayData:
        if float(i['v1'])<2:
            continue

        if float(i['v1'])>max['value']:
            max={'value':round(float(i['v1']),2),'time':i['v0']}
        if float(i['v1'])<min['value']:
            min={'value':round(float(i['v1']),2),'time':i['v0']}
    if min['value']==999 or  max['value']==0:
        return None
    else:
        return {'min':min,'max':max}


def getAllData(code):    
    collection = connection[code]
    rows = collection.find().sort([('id', pymongo.ASCENDING)]) 
    data=[]
    for i in rows:        
        if float(i['v1'])>2:
            data.append(i)
    return data

def showx(id,code,startTime):
      #publish 
    templete = 'count/'+str(id)+'.html'
    id= int(id)
    if id==1:
        bar = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
            .add_yaxis("商家B", [15, 6, 45, 20, 35, 66])
            .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
        )
        bar.render('templates/'+templete)
    elif id==2:
        words = [
            ("Sam S Club", 10000),
            ("Macys", 6181),
            ("Amy Schumer", 4386),
            ("Jurassic World", 4055),
            ("Charter Communications", 2467),
            ("Chick Fil A", 2244),
            ("Planet Fitness", 1868),
            ("Pitch Perfect", 1484),
            ("Express", 1112),
            ("Home", 865),
            ("Johnny Depp", 847),
            ("Lena Dunham", 582),
            ("Lewis Hamilton", 555),
            ("KXAN", 550),
            ("Mary Ellen Mark", 462),
            ("Farrah Abraham", 366),
            ("Rita Ora", 360),
            ("Serena Williams", 282),
            ("NCAA baseball tournament", 273),
            ("Point Break", 265),
        ]
     
        worldcloud=(
            WordCloud()
            .add("", words, word_size_range=[20, 100])
            .set_global_opts(title_opts=opts.TitleOpts(title="LinGan WordCloud"))
            )
        worldcloud.render('templates/'+templete)
    elif id==3:      
        bar = Bar()
        ##
        rows = getOneDayData(code,startTime) 
        data = {}
        for x in rows:
            x['v1']= round(float(x['v1']), 2)
            x['v4']= int(x['v4'])
            if x['v1'] not in data.keys():
                data[x['v1'] ]=x['v4']
            else:
                data[x['v1'] ]+=x['v4']                
        ##
        listOrder = sorted(data)
        x_data=[]
        y_data=[]
        for key in listOrder:
            x_data.append(key)
            y_data.append(data[key]) 


        bar.add_xaxis(x_data).add_yaxis("Transaction Data", y_data).reversal_axis()
        bar.set_series_opts(label_opts=opts.LabelOpts(position="right"))
        bar.set_global_opts(title_opts=opts.TitleOpts(title="price:vol"))
        bar.render('templates/'+templete)
    elif id==4:
        #Boxplot
        id=id
    elif id==5:
        #Scatter
        id=id

    elif id==6:
        #Scatter
        rows = getOneDayData(code,startTime) 
        data = []       
        for x in rows:
            if x['v1'] !='':                
                timeArray = time.strptime(x['v0'], "%Y-%m-%d %H:%M:%S")
                dt_new = time.strftime("%H%M%S",timeArray)#%m%d%
                x['v0']= float(dt_new)/3600-20
                x['v1']= float(x['v1'])-17
                if x['v1']>0:
                    data.append([x['v0'],x['v1']])
        
        data.sort(key=lambda x: x[0])
        x_data = [d[0] for d in data]
        y_data = [d[1] for d in data]
        sac = Scatter(init_opts=opts.InitOpts(width="600px", height="400px"))
        sac.add_xaxis(xaxis_data=x_data).add_yaxis( series_name="",
            y_axis=y_data,
            symbol_size=5,
            label_opts=opts.LabelOpts(is_show=False),
        ).set_series_opts().set_global_opts(
            xaxis_opts=opts.AxisOpts(
            type_="value", splitline_opts=opts.SplitLineOpts(is_show=True))
        ).yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ). yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ).tooltip_opts=opts.TooltipOpts(is_show=False),
        sac.render('templates/'+templete)
    return templete
def showAllX(id,code,flag=0):
    #publish 
    templete = 'count/'+str(id)+'.html'
    id= int(id)
    if id==1:
        days =10
        startStream = datetime.datetime.now() - datetime.timedelta(days)
        dayX = []
        dayY = []
        for i in range(days+2):
            try:
                queryTime = (startStream+datetime.timedelta(i))
                queryStr = str(queryTime.year)+'-'+str(queryTime.month)+'-'+str(queryTime.day)
                ondDayData = getOneDayData(code,queryStr)
                b=[]
                for x in ondDayData:
                    if x['v1'] !='' and (float(x['v1'])>1): 
                        b.append(x['v1'])
                if b!=[]:
                    dayX.append(queryStr)
                    yV = round(float(max(b))-float(min(b)),2)
                    dayY.append(yV)
            except :
                continue

        bar = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(dayX)
            .add_yaxis("test", dayY)
            .set_global_opts(title_opts=opts.TitleOpts(title="wave", subtitle="."))
        )
        bar.render('templates/'+templete)
    elif id==2:
        conn = connection['words_count']
        rows = conn.find() 
        words = []
        for x in rows:
            if x['title'] !='':    
                words.append((x['title'],int(x['count'])))  
     
        worldcloud=(
            WordCloud()
            .add("", words, word_size_range=[20, 100])
            .set_global_opts(title_opts=opts.TitleOpts(title="LinGan WordCloud"))
            )
        worldcloud.render('templates/'+templete)
    elif id==3:      
        bar = Bar()
        ##
        rows = getAllData(code) 
        data = {}
        for x in rows:
            x['v1']= round(float(x['v1']), 2)
            x['v4']= int(x['v4'])
            if x['v1'] not in data.keys():
                data[x['v1'] ]=x['v4']
            else:
                data[x['v1'] ]+=x['v4']                
        ##
        listOrder = sorted(data)
        x_data=[]
        y_data=[]
        for key in listOrder:
            x_data.append(key)
            y_data.append(data[key]) 


        bar.add_xaxis(x_data).add_yaxis("Transaction Data", y_data).reversal_axis()
        bar.set_series_opts(label_opts=opts.LabelOpts(position="right"))
        bar.set_global_opts(title_opts=opts.TitleOpts(title="count"))
        if flag==1:
            return bar
        bar.render('templates/'+templete)
    elif id==4:
         #Scatter
        days = 20
        startStream = datetime.datetime.now() - datetime.timedelta(days)
        dayX = []
        dayY = []
        for i in range(days+2):
            try:
                queryTime = (startStream+datetime.timedelta(i))
                queryStr = str(queryTime.year)+'-'+str(queryTime.month)+'-'+str(queryTime.day)
                ondDayData = oneDataMinAndMaxPrice(code,queryStr)
                if None == ondDayData:
                    continue
                dayX.append(ondDayData['min']['time'])
                dayY.append(ondDayData['min']['value'])
               # dayMaxY.append(ondDayData['max']['value'])

            except :
                continue
        #add_yaxis("max", dayMaxY).
        Scatter().add_xaxis(dayX).add_yaxis("min", dayY).set_global_opts(
            title_opts=opts.TitleOpts(title="Scatter-dailymin"),
            xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
        ).render('templates/'+templete)
        #  bar.add_xaxis(x_data).add_yaxis("Transaction Data", y_data)
    elif id==5:
        #Scatter
        days = 20
        startStream = datetime.datetime.now() - datetime.timedelta(days)
        dayX = []
        dayY = []
        for i in range(days+2):
            try:
                queryTime = (startStream+datetime.timedelta(i))
                queryStr = str(queryTime.year)+'-'+str(queryTime.month)+'-'+str(queryTime.day)
                ondDayData = oneDataMinAndMaxPrice(code,queryStr)
                if None == ondDayData:
                    continue
                dayX.append(ondDayData['max']['time'])
                dayY.append(ondDayData['max']['value'])
               # dayMaxY.append(ondDayData['max']['value'])

            except :
                continue
        #add_yaxis("max", dayMaxY).
        Scatter().add_xaxis(dayX).add_yaxis("max", dayY).set_global_opts(
            title_opts=opts.TitleOpts(title="Scatter-dailymax"),
            xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
        ).render('templates/'+templete)

        

    elif id==6:
        #Scatter
        rows = getAllData(code) 
        data = []  
        # b = [i['v1'] for i in rows]

        for x in rows:
            if x['v1'] !='':                
                timeArray = time.strptime(x['v0'], "%Y-%m-%d %H:%M:%S")
                dt_new = time.strftime("%H%M%S",timeArray)#%m%d%
                x['v0']= float(dt_new)/3600-20
                x['v1']= float(x['v1'])
                if x['v1']>0:
                    data.append([x['v0'],x['v1']])
        
        data.sort(key=lambda x: x[0])
        x_data = [d[0] for d in data]
        y_data = [d[1] for d in data]
        sac = Scatter(init_opts=opts.InitOpts(width="600px", height="1000px"))
        sac.add_xaxis(xaxis_data=x_data).add_yaxis( series_name="",
            y_axis=y_data,
            symbol_size=5,
            label_opts=opts.LabelOpts(is_show=False),
        ).set_series_opts().set_global_opts(
            xaxis_opts=opts.AxisOpts(
            type_="value", splitline_opts=opts.SplitLineOpts(is_show=True))
        ).yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ). yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ).tooltip_opts=opts.TooltipOpts(is_show=False),
        if flag==1:
            return sac
        sac.render('templates/'+templete)
    elif id==7:
        templete = ''

    return templete