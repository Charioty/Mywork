#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Charioty
# time:2019/4/26

import sqlite3

#查询上级分支相关信息
def Superior(X,Y):

    conn = sqlite3.connect('./Gy.db')
    c = conn.cursor()
    Sup_N = 0
    ID_X = c.execute("SELECT ID FROM Info WHERE V=? ", (X,)).fetchall();
    if Y == "六世":
        if ID_X[0][0] == 2 or ID_X[0][0] == 12 or ID_X[0][0] == 4 or ID_X[0][0] == 5 :
            Sup_Native ="濮州叶氏"
            return Sup_Native
        else:
            return Sup_N
    elif Y == "十二世":
        if ID_X[0][0] == 7 :
            Sup_Native ="凤祖后江苏省沛县朱寨镇梅村"
            return Sup_Native
        else:
            return Sup_N
    elif Y == "十六世":
        if ID_X[0][0] == 6 or ID_X[0][0] == 10 or ID_X[0][0] == 11 :
            Sup_Native ="凤祖后江苏省沛县朱寨镇梅村"
            return Sup_Native
        elif ID_X[0][0] == 13 or ID_X[0][0] == 14 or ID_X[0][0] == 15 or ID_X[0][0] == 16 or ID_X[0][0] == 18 or ID_X[0][0] == 19:
            Sup_Native ="凤祖后河南省范县濮城"
            return Sup_Native
        else:
            return Sup_N
    elif Y == "十七世":
        if ID_X[0][0] == 8 :
            Sup_Native ="凤祖后江苏省沛县朱寨镇梅村胡庙王店"
            return Sup_Native
        elif ID_X[0][0] == 9 :
            Sup_Native ="凤祖后江苏省沛县朱寨镇梅村"
            return Sup_Native
        else:
            return Sup_N
    elif Y == "十九世":
        if ID_X[0][0] == 17 :
            Sup_Native ="凤祖后河南省范县濮城"
            return Sup_Native
        elif ID_X[0][0] == 3 :
            Sup_Native ="鸾祖后河南省范县王楼乡叶庄"
            return Sup_Native
        else:
            return Sup_N
    else:
        return Sup_N
    c.close()
    conn.close()

#查询Info数据库内容信息
def Select_Info(X):

    conn = sqlite3.connect('./Gy.db')
    c = conn.cursor()
    Data_Info = c.execute("SELECT V FROM Info WHERE AV =?",(X,)).fetchall();

    return Data_Info
    c.close()
    conn.close()
#查询父亲相关名字
def Select_PgFather(X,Y):

    conn = sqlite3.connect('./Gy.db')
    c = conn.cursor()
    Sup_F = Superior(X,Y)
    if Y == "一世":
        Data_Info = c.execute("SELECT Father FROM Gy WHERE Native =? and Seniority=? ", (X, Y)).fetchall();
        return Data_Info
    elif Sup_F == 0:
        A = c.execute("SELECT ID FROM Info WHERE V=? ", (Y,)).fetchall();
        B = A[0][0] - 1
        C = c.execute("SELECT V FROM Info WHERE ID=? ", (B,)).fetchall();
        Y = C[0][0]
        Data_Info = c.execute("SELECT NAME FROM Gy WHERE Native =? and Seniority=? ",(X,Y)).fetchall();
        return Data_Info
    else:
        A = c.execute("SELECT ID FROM Info WHERE V=? ", (Y,)).fetchall();
        B = A[0][0] - 1
        C = c.execute("SELECT V FROM Info WHERE ID=? ", (B,)).fetchall();
        Y = C[0][0]
        Data_Info1 = c.execute("SELECT NAME FROM Gy WHERE Native =? and Seniority=? ",(X,Y)).fetchall();
        Data_Info2 = c.execute("SELECT NAME FROM Gy WHERE Native =? and Seniority=? ",(Sup_F,Y)).fetchall();
        Data_Info = Data_Info1+Data_Info2
        return Data_Info
    c.close()
    conn.close()
#查询父亲相关ID
def Select_FatherID(X,Y,Z):

    conn = sqlite3.connect('./Gy.db')
    c = conn.cursor()
    Sup_F = Superior(X, Y)
    if Y == "一世":
        FatherID = c.execute("SELECT ID FROM Gy WHERE Native =? and Seniority=? ", (X, Y)).fetchall();
        return FatherID
    elif Sup_F == 0:
        A = c.execute("SELECT ID FROM Info WHERE V=? ", (Y,)).fetchall();
        B = A[0][0] - 1
        C = c.execute("SELECT V FROM Info WHERE ID=? ", (B,)).fetchall();
        Y = C[0][0]
        FatherID = c.execute("SELECT ID FROM Gy WHERE Native =? and Seniority=? and Name=?",(X,Y,Z)).fetchall();
        return FatherID
    else:
        A = c.execute("SELECT ID FROM Info WHERE V=? ", (Y,)).fetchall();
        B = A[0][0] - 1
        C = c.execute("SELECT V FROM Info WHERE ID=? ", (B,)).fetchall();
        Y = C[0][0]
        FatherID = c.execute("SELECT ID FROM Gy WHERE Native =? and Seniority=? and Name=?",(Sup_F,Y,Z)).fetchall();
        return FatherID
    c.close()
    conn.close()

def Select_ID(X):
    conn = sqlite3.connect('./Gy.db')
    c = conn.cursor()
    Data_ID = c.execute("SELECT * FROM Gy WHERE ID =?",(X,)).fetchall();
    if len(Data_ID):
        return False
    else:
        return True
    c.close()
    conn.close()
def Select_Last():
    conn = sqlite3.connect('./Gy.db')
    c = conn.cursor()
    Data_last= c.execute("select * from Gy order by rowid desc limit 0,1").fetchall();
    return Data_last
    c.close()
    conn.close()

#print(Select_FatherID("鸾祖后河南省范县王楼乡叶庄","六世","叶臣"))
#print(Select_PgFather("鸾祖后河南省范县王楼乡叶庄","六世"))
# print(Select_Last())
