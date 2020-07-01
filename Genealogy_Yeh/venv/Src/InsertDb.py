#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Charioty
# time:2019/4/26

import sqlite3
import xlrd
import xlwt

def Insert_Info():
    i=0
    workbook = xlrd.open_workbook(r'Info_data.xlsx')
    sheet = workbook.sheet_by_name('Info')
    conn = sqlite3.connect('./Gy.db')
    # print('Opened database successfully')
    while i < sheet.nrows:
        rows = sheet.row_values(i)
        c = conn.cursor()
        c.execute("INSERT INTO Info (ID,AV,V) values(?,?,?)",(rows[0],rows[1],rows[2]))
        c.close()
        i = i + 1
    # print('Records created successfully')
    workbook.close()
    conn.commit()
    conn.close()

def Insert_Data(Data):
    conn = sqlite3.connect('./Gy.db')
    c = conn.cursor()
    c.execute("INSERT INTO Gy (ID, Seniority, Native, NAME, Father, Ranking, Sun, Doc, Remarks) values(?,?,?,?,?,?,?,?,?)",(Data[0],Data[1],Data[2],Data[3],Data[4],Data[5],Data[6],Data[7],Data[8]));
    c.close()
    # print('Records created successfully')
    conn.commit()
    conn.close()