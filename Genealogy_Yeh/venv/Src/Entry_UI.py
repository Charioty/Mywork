#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Charioty
# time:2019/4/24
import tkinter as tk
import tkinter.font as tkF
from tkinter import ttk
import tkinter.messagebox
import SelectDb
import InsertDb
import numpy as np
import json

#检验是否全是中文字符
def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True
#下拉列表的值
def chose(C):
    i=0
    Data_Info=[]
    if C == "后代" or C =="排行":
        row = SelectDb.Select_Info(C)
        while i < row.__len__():
            my_list = json.loads(row[i][0])
            Data_Y = np.array(my_list)
            Data_Info.append(int(Data_Y))
            i = i + 1
        return Data_Info
    else:
        rows = SelectDb.Select_Info(C)
        return rows
#Father下拉列表的值，实时获取
def Get_F(*args):
    Fathers = SelectDb.Select_PgFather(C_Native.get(),C_Seniority.get())
    C_Father['values'] = (Fathers)
    return C_Father['values']
#检查数据是否合理
def Check_data(*args):
    global I_Remarks
    I_Remarks.delete(1.0, tk.END)
    if P1.get() =='':
        I_Remarks.insert(tk.INSERT,'姓名不能为空\n')
        tkinter.messagebox.showwarning('警告','姓名不能为空\n')
    elif is_all_chinese(P1.get()) == False:
        I_Remarks.insert(tk.INSERT,'姓名不能输入非汉字\n')
        tkinter.messagebox.showwarning('警告', '姓名不能输入非汉字\n')
    elif C3.get() =='':
        I_Remarks.insert(tk.INSERT,'父亲选项不能为空\n')
        tkinter.messagebox.showwarning('警告', '父亲选项不能为空\n')
    elif SelectDb.Select_ID(Make_ID()) == False:
        I_Remarks.insert(tk.INSERT, '该人已经在数据库存在，请注意检查相关信息\n')
        tkinter.messagebox.showwarning('警告', '该人已经在数据库存在，请注意检查相关信息\n')
    if P1.get() != '' and is_all_chinese(P1.get()) != False and C3.get() !=''and SelectDb.Select_ID(Make_ID()) == True:
        I_Remarks.insert(tk.INSERT, '数据输入正确，请提交数据库\n')
#预览数据处理
def Show_Data(*args):
    global T_Remarks,I_Remarks,P1,C1,C2,C3,C4,C5,C6
    Data=[]
    Data.append('ID：{}\n'.format(Make_ID()))
    Data.append('姓名：{}\n'.format(P1.get()))
    Data.append('分支：{}\n'.format(C1.get()))
    Data.append('辈分：{}\n'.format(C2.get()))
    Data.append('父亲：{}\n'.format(C3.get()))
    Data.append('排行：{}\n'.format(C4.get()))
    Data.append('儿子：{}\n'.format(C5.get()))
    Data.append('女儿：{}\n'.format(C6.get()))
    Data.append('备注：{}\n'.format(T_Remarks.get(1.0, tk.END)))
    I_Remarks.delete(1.0, tk.END)
    for i in Data:
        I_Remarks.insert(tk.INSERT, i)
#根据填写数据进行ID创建
def Make_ID(*args):
    global C1, C2, C3, C4
    F_ID = SelectDb.Select_FatherID(C1.get(), C2.get(), C3.get())
    ID = '{}'.format(F_ID[0][0])+'0'+'{}'.format(C4.get())
    return ID
#提交相应数据
def Submit_data(*args):
    global P_name,T_Remarks, I_Remarks, P1, C1, C2, C3, C4, C5, C6
    Data_S=[]
    Data_S.append('{}'.format(Make_ID()))
    Data_S.append('{}'.format(C2.get()))
    Data_S.append('{}'.format(C1.get()))
    Data_S.append('叶'+'{}'.format(P1.get()))
    Data_S.append('{}'.format(C3.get()))
    Data_S.append('{}'.format(C4.get()))
    Data_S.append('{}'.format(C5.get()))
    Data_S.append('{}'.format(C6.get()))
    Data_S.append('{}'.format(T_Remarks.get(1.0, tk.END)))
    I_Remarks.delete(1.0, tk.END)
    try:
        Show_Data()
        I_Remarks.insert(tk.INSERT, '\n')
        I_Remarks.insert(tk.INSERT, InsertDb.Insert_Data(Data_S))
    except Exception:
        # I_Remarks.insert(tk.INSERT, "该数据已存在，请检查是否填写错误")
        I_Remarks.insert(tk.INSERT, "已提交数据")
        T_Remarks.delete(1.0, tk.END)
        P_name.delete(0,tk.END)
def History_data():
    global I_Remarks
    Data_l=[]
    Data_l.append('上次完成的信息是：\n')
    Data_l.append('姓名：{}\n'.format(SelectDb.Select_Last()[0][3]))
    Data_l.append('分支：{}\n'.format(SelectDb.Select_Last()[0][2]))
    Data_l.append('辈分：{}\n'.format(SelectDb.Select_Last()[0][1]))
    Data_l.append('父亲：{}\n'.format(SelectDb.Select_Last()[0][4]))
    Data_l.append('\n\n请注意对照相关关系检查输入')
    I_Remarks.delete(1.0, tk.END)
    for i in Data_l:
        I_Remarks.insert(tk.INSERT, i)

app = tk.Tk()
P1 = tk.StringVar()
C1 = tk.StringVar()
C2 = tk.StringVar()
C3 = tk.StringVar()
C4 = tk.StringVar()
C5 = tk.StringVar()
C6 = tk.StringVar()
# 设置窗口标题:
app.title('Gy数据输入处理')
app.geometry('1024x768')
app.resizable(0,0)
#定义各种组件的样式字体等
LtkF = tkF.Font(family='Times New Roman',size=40,weight=tkF.BOLD)
PtkF = tkF.Font(family='Times New Roman',size=20)
CtkF = tkF.Font(family='Times New Roman',size=40)
RtkF = tkF.Font(family='Times New Roman',size=25,weight=tkF.BOLD)
TtkF = tkF.Font(family='Times New Roman')
BtkF = tkF.Font(family='Times New Roman',size=15,weight=tkF.BOLD)
#各种组件的设置
Title_name =  tk.Label(app, text='Gy数据库输入程序', bg='pink', font=('Times New Roman',18),width=50, height=2)
L_name = tk.Label(app, text='姓名', bg='SkyBlue', relief= 'raised',font=LtkF,width=6, height=1)
P_name = tk.Entry(app,textvariable=P1,bd =18,relief= 'raised',font=PtkF,width=25)
L_Native = tk.Label(app, text='分支', bg='SkyBlue', relief= 'raised',font=LtkF,width=6, height=1)
C_Native = tk.ttk.Combobox(app,state='readonly',textvariable=C1,font=CtkF,width=13)
C_Native['values'] = (chose(L_Native.cget("text")))
C_Native.current(0)
C_Native.bind("<<ComboboxSelected>>",Get_F)
L_Seniority = tk.Label(app, text='辈分', bg='SkyBlue', relief= 'raised',font=LtkF,width=6, height=1)
C_Seniority = tk.ttk.Combobox(app,state='readonly',textvariable=C2,font=CtkF,width=13)
C_Seniority['values'] = (chose(L_Seniority.cget("text")))
C_Seniority.current(0)
C_Seniority.bind("<<ComboboxSelected>>",Get_F)
L_Father = tk.Label(app, text='父亲', bg='SkyBlue', relief= 'raised',font=LtkF,width=6, height=1)
C_Father = tk.ttk.Combobox(app,state='readonly',textvariable=C3,font=CtkF,width=13,)
L_Rank = tk.Label(app, text='排行', bg='SkyBlue', relief= 'raised',font=RtkF,width=4, height=1)
C_Rank = tk.ttk.Combobox(app,state='readonly',textvariable=C4,font=RtkF,width=4)
C_Rank['values'] = (chose(L_Rank.cget("text")))
C_Rank.current(0)
L_Sun = tk.Label(app, text='儿子', bg='SkyBlue', relief= 'raised',font=RtkF,width=4, height=1)
C_Sun = tk.ttk.Combobox(app,state='readonly',textvariable=C5,font=RtkF,width=4)
C_Sun['values'] = (chose('后代'))
C_Sun.current(0)
C_Sun['state'] = 'readonly'
L_Doc = tk.Label(app, text='女儿', bg='SkyBlue', relief= 'raised',font=RtkF,width=4, height=1)
C_Doc = tk.ttk.Combobox(app,state='readonly',textvariable=C6,font=RtkF,width=4)
C_Doc['values'] = (chose('后代'))
C_Doc.current(0)
L_Remarks = tk.Label(app, text='备注', bg='SkyBlue', relief= 'raised',font=RtkF,width=5, height=1)
T_Remarks = tk.Text(app,font=TtkF,width=73,height=11)
Show = tk.Button(app, text='预览',command=Show_Data,font=BtkF, width=12,height=2)
Check = tk.Button(app, text='检查',command=Check_data,font=BtkF, width=12,height=2)
Submit = tk.Button(app, text='提交',command=Submit_data,font=BtkF, width=12,height=2)
History = tk.Button(app, text='历史记录',command=History_data,font=BtkF, width=12,height=2)
Information = tk.Label(app, text='详细信息', bg='SkyBlue', relief= 'raised',font=LtkF,width=11, height=1)
I_Remarks = tk.Text(app,font=TtkF,width=44,height=27)
#各种组件的布局
Title_name.grid(row=0,column=1)
L_name.grid(row=1,column=0,sticky=tk.W)
P_name.grid(row=1,column=1,sticky=tk.W)
L_Native.grid(row=2,column=0,sticky=tk.W)
C_Native.grid(row=2,column=1,sticky=tk.W)
L_Seniority.grid(row=3,column=0,sticky=tk.W)
C_Seniority.grid(row=3,column=1,sticky=tk.W)
L_Father.grid(row=4,column=0,sticky=tk.W)
C_Father.grid(row=4,column=1,sticky=tk.W)
L_Rank.grid(row=5,column=0,sticky=tk.W)
C_Rank.grid(row=5,column=1,sticky=tk.W)
L_Sun.grid(row=5,column=2,sticky=tk.W)
C_Sun.grid(row=5,column=3,sticky=tk.W)
L_Doc.grid(row=5,column=4,sticky=tk.W)
C_Doc.grid(row=5,column=5,sticky=tk.W)
L_Remarks.grid(row=6,column=0,sticky=tk.W)
T_Remarks.grid(row=7,column=1,sticky=tk.W)
Show.grid(row=8,column=0,sticky=tk.W)
Check.grid(row=8,column=1,sticky=tk.W)
Submit.grid(row=8,column=2,sticky=tk.W)
History.grid(row=8,column=3,sticky=tk.W)
Information.grid(row=1,column=2,sticky=tk.W)
I_Remarks.grid(row=2,column=2,sticky=tk.W)

# Title_name.pack(side='top')
# L_name.place(x=16,y=70,anchor='nw')
# P_name.place(x=220,y=70,anchor='nw')
# L_Native.place(x=16,y=140,anchor='nw')
# C_Native.place(x=220,y=140,anchor='nw')
# L_Seniority.place(x=16,y=210,anchor='nw')
# C_Seniority.place(x=220,y=210,anchor='nw')
# L_Father.place(x=16,y=280,anchor='nw')
# C_Father.place(x=220,y=280,anchor='nw')
# L_Rank.place(x=16,y=350,anchor='nw')
# C_Rank.place(x=115,y=350,anchor='nw')
# L_Sun.place(x=220,y=350,anchor='nw')
# C_Sun.place(x=317,y=350,anchor='nw')
# L_Doc.place(x=420,y=350,anchor='nw')
# C_Doc.place(x=516,y=350,anchor='nw')
# L_Remarks.place(x=16,y=400,anchor='nw')
# T_Remarks.place(x=16,y=450,anchor='nw')
# Show.place(x=16,y=680,anchor='nw')
# Check.place(x=233,y=680,anchor='nw')
# Submit.place(x=450,y=680,anchor='nw')
# History.place(x=866,y=680,anchor='nw')
# Information.place(x=649,y=70,anchor='nw')
# I_Remarks.place(x=649,y=140,anchor='nw')

# #P_name.insert(0, '输入姓名')
# def show():
#     print("name: %s" % P_name.get())

# 主消息循环:
app.mainloop()
