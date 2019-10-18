#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Charioty
# time:2019/4/24


import sqlite3

conn = sqlite3.connect('./Gy.db')

print('Opened database successfully')

c = conn.cursor()
c.execute('''CREATE TABLE Gy
       (ID char(250) PRIMARY KEY     NOT NULL,
       Seniority      INT     NOT NULL,
       Native         TEXT    NOT NULL,
       NAME           TEXT    NOT NULL,
       Father         TEXT     NOT NULL,
       Ranking        INT     NOT NULL,
       Sun            INT ,
       Doc            INT ,
       Remarks        CHAR(250));''')
c.execute('''CREATE TABLE Info
       (ID INT PRIMARY KEY     NOT NULL,
       AV     TEXT     NOT NULL,
       V      TEXT    NOT NULL);''')
print('Table created successfully')
conn.commit()
conn.close()
