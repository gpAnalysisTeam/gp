import time
import datetime
import re
import random
import sys
import pymongo
import numpy as np

import math
from config import mongodbConfig
from collections import Counter

def bit_product_sum(x, y):
    return sum([item[0] * item[1] for item in zip(x, y)])

def cosine_similarity(x, y, norm=False):
    """ 计算两个向量x和y的余弦相似度 """
    assert len(x) == len(y), "len(x) != len(y)"
    zero_list = [0] * len(x)
    if x == zero_list or y == zero_list:
        return float(1) if x == y else float(0)

    # method 1
    res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
    cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))
    return 0.5 * cos + 0.5 if norm else cos  # 归一化到[0, 1]区间内

t= cosine_similarity([80,100,90,70], [6,5,4.5,3.5])  # 1.0
