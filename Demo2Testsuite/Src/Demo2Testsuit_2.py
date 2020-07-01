#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Charioty
# time:2019/7/8

import configparser
import os
import os.path
import shutil
import time
from typing import Union


class Directory:
    def __init__(self, Url):
        self.Url = Url
    def processDir(self):
        Fdirs=[]
        for root,dirs,files in os.walk(self.Url):
            for name in dirs:
                Fdirs.append(os.path.join(root,name))
        return Fdirs
    def processFiles(self):
        Files=[]
        for root,dirs,files in os.walk(self.Url):
            for name in files:
                Files.append(os.path.join(root,name))
        return Files

class Find_data:
    def __init__(self,name):
        self.name = name
    # def findir(self):
    #     dirs = self.name[0:self.name.find('U000000')]
    #     return dirs
    def findname(self):
        TY = self.name[self.name.find('TY'):self.name.find('TY') + 3]
        return TY

class TargeDir:
    def __init__(self,Dirs,SUrl,OUrl):
        self.dirs,self.name = os.path.split(Dirs)
        self.Surl = SUrl
        self.OUrl = OUrl
    def targe_name(self):
        ID ='U' + self.dirs[-6:]
        targe_name = self.name.replace('U000000',ID)
        targe_name = targe_name.replace(targe_name[0:18],'')
        if targe_name[7:10] == 'F00':
            targe_name = targe_name.replace('F00','F01')
        elif targe_name[7:10] == 'F01':
            targe_name = targe_name.replace('F01','F02')
        elif targe_name[7:10] == 'F02':
            targe_name = targe_name.replace('F02','F03')
        elif targe_name[7:10] == 'F03':
            targe_name = targe_name.replace('F03','F04')
        elif targe_name[7:10] == 'F04':
            targe_name = targe_name.replace('F04','F05')
        if config()[2] == '1':
            targe_name = targe_name.replace(config()[3], '')
            targe_name = targe_name.replace(config()[4], '')
        if 'data_reg' in self.dirs:
            targe_name = targe_name.replace('.bmp', '_p.bmp')
        else:
            targe_name = targe_name.replace('.bmp', '_v.bmp')
        return targe_name
    def targe_bmp(self):
        X=self.dirs.replace(self.Surl,self.OUrl)+"\\bmp\\"
        return X
    def targe_raw(self):
        Y=self.dirs.replace(self.Surl,self.OUrl)+"\\raw\\"
        return Y

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
    deltype = config.get("config", "deltype")
    type1 = config.get("config", "type1")
    type2 = config.get("config", "type2")
    return S_Url,O_Url,deltype,type1,type2

print('wait for arrange data....')
log = open('log.txt','w')
SUrl = config()[0]
OUrl = config()[1]
for n in Directory(SUrl).processFiles():
    if Find_data(n).findname() == 'TY1':
        targe = TargeDir(n, SUrl, OUrl).targe_bmp()
        # sdir,sbmp=os.path.split(targe)
        mkdir(targe)
        targe = TargeDir(n, SUrl, OUrl).targe_bmp()+TargeDir(n, SUrl, OUrl).targe_name()
        shutil.move(n,targe)
        print("move %s -> %s" % (n, targe),file=log)
    elif Find_data(n).findname() == 'TY0':
        targe = TargeDir(n, SUrl, OUrl).targe_raw()
        # sdir,sbmp=os.path.split(targe)
        mkdir(targe)
        targe = TargeDir(n, SUrl, OUrl).targe_raw()+TargeDir(n, SUrl, OUrl).targe_name()
        shutil.move(n,targe)
        print("move %s -> %s" % (n, targe),file=log)
log.close()
dtsname = 'log_'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'.txt'
os.rename('log.txt',dtsname)
print("Mission Complete")
