#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Charioty
# time:2019/6/12

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
    S_Url = config.get("config","Source_Url")
    O_Url = config.get("config", "Out_Url")
    N_Frame = config.get("config", "Normal_Frame")
    D_Frame = config.get("config", "Dry_Frame")
    return S_Url,O_Url,N_Frame,D_Frame

def processDirectory():
    Fdirs=[]
    for root,dirs,files in os.walk(config()[0]):
        # for name in files:
        #     Fdirs.append(os.path.join(root,name))
        for name in files:
            Fdirs.append(os.path.join(root,name))
    return Fdirs

def findData(X):
    SQ_Num = X[X.find('SQ'):X.find('SQ')+5]
    Scene = X[X.find('data_'):X.find('data_')+8]
    Fdir = X[X.find(config()[0]):X.find('U')-1]
    return SQ_Num,Scene,Fdir

def targeDir(Y):
    Y=Y.replace(config()[0],config()[1])
    mkdir(Y)
    # return Y
print('wait for copy data....')
for n in processDirectory():
    targeDir(findData(n)[2])
    if findData(n)[1] == 'data_dry'and findData(n)[0] == 'SQ'+config()[3]:
        NewF = n.replace(config()[0],config()[1])
        fileC = [n,NewF]
        shutil.copyfile(fileC[0], fileC[1])
    elif findData(n)[1] == 'data_nor'and findData(n)[0] == 'SQ'+config()[2]:
        NewF = n.replace(config()[0],config()[1])
        fileC = [n,NewF]
        shutil.copyfile(fileC[0], fileC[1])
    elif findData(n)[1] == 'data_lig'and findData(n)[0] == 'SQ'+config()[2]:
        NewF = n.replace(config()[0],config()[1])
        fileC = [n,NewF]
        shutil.copyfile(fileC[0], fileC[1])
print("Mission Complete")

# print(findData(processDirectory()[0]))
# print(targeDir(findData(processDirectory()[0])[2]))
