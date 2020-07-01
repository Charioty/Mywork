#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Charioty
# time:2020/1/2

import os

def file_name(url):
    Files = []
    for root, dirs, files in os.walk(url):
        for name in files:
            Files.append(name)
    return Files

def load_file(Fname,Durl):
    for root, dirs, files in os.walk(Durl):
        if Fname in files:
            root = str(root)
            dirs = str(dirs)
            return os.path.join(root,dirs,Fname)
    return -1

log = open('file.txt','w')
FUrl = input("File_Url: ")
DUrl = input("Del_Url: ")
Filename=file_name(FUrl)
for Fname in Filename:
    print(load_file(Fname,DUrl), file=log)
log.close()
