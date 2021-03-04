## -*- coding: utf-8 -*-
import time
import datetime
import re
import random
import sys
import pymongo
import numpy as np
code='ksh600776'
import math
from config import mongodbConfig
import common as cm
from collections import Counter

from prettytable import PrettyTable
from xpinyin import Pinyin
"""
描述：  从一变量中产生cos模型
"""
# reload(sys)
# sys.setdefaultencoding('utf8')
"""
"""
testModel = cm.creteModelBySE(code,"2021-02-01","2021-02-20")
print(testModel)
