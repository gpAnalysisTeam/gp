#! /bin/bash
cd /root/gp/mysite/crontab/reptile; python3 ./akshare_transaction_data.py -k
cd /root/gp/mysite/tes; python3 daysimilaritycos.py
cd /root/gp/mysite/crontab/reptile; python3 ./akshare_transaction_data.py -t