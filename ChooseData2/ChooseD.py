#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Charioty
# time:2019/9/25

import configparser
import os
import os.path
import shutil

def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建
        return False

def config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    S_Url = config.get("config1","S_Url")
    O_Url = config.get("config1", "O_Url")
    C_Url = config.get("config1", "CopUrl")
    return S_Url,O_Url,C_Url

def processDirectory(X):
    Fdirs=[]
    for root,dirs,files in os.walk(X):
        for name in files:
            Fdirs.append(os.path.join(root,name))
    return Fdirs

def findData(X):
    Fdir = X[X.find(config()[2]):X.find('U')-1]
    return Fdir

def targeDir(Y):
    Y=Y.replace(config()[2],config()[1])
    mkdir(Y)
    return Y
print('wait for copy data....')
log = open('log.txt','w')
for n in processDirectory(config()[2]):
    targeDir(findData(n))
    NewF = n.replace(config()[2],config()[1])
    SF = n.replace(config()[2],config()[0])
    fileC = [SF,NewF]
    if os.path.exists(fileC[0]) == True:
        shutil.copyfile(fileC[0], fileC[1])
    else:
        print(fileC[0], file=log)
        continue
log.close()
print("Mission Complete")
