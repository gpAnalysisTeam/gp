# stock analyze system


## 前言

通过股票技术分析结合现代统计学、各类算法等提高个人股票投资分析成功率，实现赚钱目的


## 使用方法

## Requirements and Installation
Highly recommended to use [miniconda](https://conda.io/miniconda.html) for easier installation.
  * python>=3.6
  * pytorch>=0.4.1
  * Django
  * librosa
  * tensorboard
  * tensorboardX
  * matplotlib
  * unidecode
  
环境
```
0,python cli+web
1;use mongodb 
```

目录描述：
```
1,采集脚本：crontab/
2,mysite ：dgango web,
    运行：cd /root/gp/mysite/;python3 /root/gp/mysite/manage.py runserver 0.0.0.0:8000 --noreload 
```
git 管理规则： 
gp1.0表示大家的第一个版本，
请创建自己的分支：如：gp1.0_wenyq  (gp1.0_（自己的名字）)，各人在自己的分支下改代码，合并到阶段性的版本中。
release：第一个正式版本。
test表示测试版本。

QQ交流群：659642073
<br>
<img src="https://github.com/gpAnalysisTeam/gp/blob/master/qq.png" width="260px"/> 



## Major TODOs
- [x] 股票基础数据爬取和保存.
- [ ] 微信小程序设计及开发.
- [ ] 大盘相关指标分析.
- [ ] 热点版块相关分析.
- [x] 股票分时图、日线图、周线图、月线图、根据需要图形化展示.
- [ ] 整合各种指标测试分析效果
- [x] 股票按日线模型匹配，按高低显示，并在此基础上显示相关结果的细粒度统计。


