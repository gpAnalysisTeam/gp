主要有两部分组成：
    采集模块系统，可单独运行。在目录reptile。详细使用可参考reptile/readme.txt
    计算模块或计算与展模块。在目录count。

架构：
     数据库mongodb;

运行：（注：数据有延时）
    cd /root/gp/mysite/crontab/reptile; sh bash.sh
输出：
     1,计算与查看推荐列表： /root/gp/mysite/crontab/feature；python3 list.py
     2, 实时查看1中数据：/root/gp/do; sh do.sh
     