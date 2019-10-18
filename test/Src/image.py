#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Charioty
# time:2019/8/30

from PIL import Image
import xlsxwriter
import os
import os.path

def Directory(url):
    Files = []
    for root, dirs, files in os.walk(url):
        for name in files:
            Files.append(os.path.join(root, name))
    return Files
def Clal(num,Sum):
    x=int(num/10)
    Sum[x]= Sum[x]+1
    return Sum

SUrl = input("Images_Url: ")
print('Prepare to process data')
workbook = xlsxwriter.Workbook('Pixel_brightness.xlsx')
worksheet = workbook.add_worksheet('data')
coloumn = 0
for n in Directory(SUrl):
    if 'desktop.ini' in n:
        continue
    else:
        Sum=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        row = 0
        worksheet.write(row, coloumn, n[6:21])
        i = 1
        j = 1
        img = Image.open(n)  # 读取图像
        width = img.size[0]  # 长度
        height = img.size[1]  # 宽度
        for i in range(0, width):  # 遍历所有长度的点
            for j in range(0, height):  # 遍历所有宽度的点
                pix = (img.getpixel((i, j)))  # 获取点的亮度值
                Clal(pix, Sum)
        for data in Sum:
            row= row+1
            worksheet.write(row, coloumn, data)
        coloumn = coloumn+1
    print('Completed：'+n[6:21])
workbook.close()
print('Mission Completed')