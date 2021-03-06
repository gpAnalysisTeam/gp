from django.shortcuts import render
from count.model import common,hot
from count.model import datas


# Create your views here.
def index(request):
    context = {} 
    context['code'] =request.GET['code']
    context['startTime'] = request.GET['startTime']
    context['codes'] =common.coss()
    context['industryHot'] =common.industryHot()
    #
    data15= datas.datas15().wordsWenziList(context['code'])
    context['data15'] =data15
    return render(request,'count/index.html',context)    

def test(request):
    context = {}    
    code=None
    if 'code' in request.GET:
        str = common.common()
        code = request.GET['code']
    else:
        str=None        
    context['result'] = f"你搜索的内容为：{code}; response:{str}"
    return render(request,'count/mycharts.html',context)
   
def showx(request):
    if 'id' in request.GET and 'code' in request.GET and 'startTime' in request.GET:
        id= request.GET['id']
        code= request.GET['code']
        startTime= request.GET['startTime']
        str = common.showx(id,code,startTime)
        return render(request,str)

def showAllX(request):
    if 'id' in request.GET and 'code' in request.GET and 'startTime' in request.GET:
        id= request.GET['id']
        code= request.GET['code']
        str = common.showAllX(id,code)
        return render(request,str)

def showHotlX(request):
    if 'id' in request.GET and 'code' in request.GET and 'startTime' in request.GET:
        id= request.GET['id']
        code= request.GET['code']
        str = hot.showHotX(id,code)
        return render(request,str)
