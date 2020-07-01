#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Charioty
# time:2020/4/14

import configparser
import os
import os.path
import openpyxl
from openpyxl.styles import Alignment, Border, Side

def config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    S_Url = config.get("config","Source_Url")
    sence = config.get("scene", "scene")
    sence = sence.split('|')
    return S_Url,sence

def processDirectory(Surl):
    Fdirs=[]
    for root,dirs,files in os.walk(Surl):
        #root,文件目录，从给的目录到文件那一层
        #dirs,空
        #files,当前文件目录中所有文件
        for name in files:
            Fdirs.append(os.path.join(root,name))
    return Fdirs

def cla(scene,dirs):
    Sum = [[0,0,0,0,0] for i in range(len(scene))]
    for n in dirs:
        if 'reg' in n:
            i = scene.index('reg')
            Sum[i][0] = Sum[i][0] + 1#该场景总数
            X = os.path.split(n)
            if X[1][X[1].find('IGE$'):X[1].find('IGE$') + 5] == 'IGE$1':
                Sum[i][1] = Sum[i][1] + 1
                if X[1][X[1].find('@RC$'):X[1].find('@RC$') + 7] == '@RC$102':
                    Sum[i][2] = Sum[i][2] + 1
                else:
                    continue
                if X[1][X[1].find('IPE$'):X[1].find('IPE$') + 5] == 'IPE$1':
                    Sum[i][3] = Sum[i][3] + 1
                else:
                    continue
            else:
                Sum[i][4] = Sum[i][4] + 1
        else:
            X = os.path.split(n)
            sce = X[0][X[0].find('data_') + 5:X[0].find('data_') + 8]
            for i, j in enumerate(scene):
                if sce in j:
                    Sum[i][0] = Sum[i][0] + 1
                    if X[1][X[1].find('IGV$'):X[1].find('IGV$') + 5] == 'IGV$1':
                        Sum[i][1] = Sum[i][1] + 1
                        if X[1][X[1].find('@RC$'):X[1].find('@RC$') + 5] == '@RC$0':
                            continue
                        else:
                            Sum[i][2] = Sum[i][2] + 1
                        if X[1][X[1].find('IGL$'):X[1].find('IGL$') + 5] == 'IGL$1':
                            Sum[i][3] = Sum[i][3] + 1
                        else:
                            continue
                    else:
                        Sum[i][4] = Sum[i][4] + 1
                else:
                    continue
    return Sum

if __name__ == '__main__':
    Surl = config()[0]
    scene = config()[1]
    num = int(len(scene))
    book = openpyxl.Workbook()
    sheet1 = book.active
    sheet1["A1"] = Surl
    sheet1["B1"] = 'Total'
    sheet1["C1"] = 'Available'
    sheet1["D1"] = 'Used'
    sheet1["E1"] = 'Pre/Learn'
    sheet1["F1"] = 'Unavailable'
    for i, j in enumerate(scene):
        sheet1['A' + str(i + 2)] = j
    dirs = processDirectory(Surl)
    Sum = cla(scene, dirs)#数据已输出
    for m in range(len(Sum)):
        for n in range(len(Sum[0])):
            sheet1.cell(row=m+2, column=n+2).value = Sum[m][n]
    thin = Side(border_style="thin")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for row in sheet1['A1:F' + str(num + 1)]:
        for cell in row:
            cell.border = border
            cell.alignment = alignment
    book.save('Cla_Flag.xlsx')
    book.close()
    os.rename('Cla_Flag.xlsx', Surl[Surl.rfind('\\') + 1:] + '_Cla_Flag.xlsx')
    print('"Mission Complete"')
