#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Charioty
# time:2019/6/25

import tkinter as tk
import tkinter.font as tkF
from tkinter import ttk
import tkinter.messagebox
import Calculation
import calendar

def vision():
    tkinter.messagebox.showwarning('版本信息', '版本：V1.2.0\n发布时间：20190925\n作者：Charioty.YE\n邮箱：372600969@qq.com\n非常感谢大家提出宝贵建议')

def validateText(content):
    global P1, P2, P3, P4
    if content.isdigit() or content == "":
        return True
    else:
        return False
        # tkinter.messagebox.showwarning('警告','输入的字符非法，请输入正确数字')

def showC(*args):
    global P1, P2, P3, P4
    if P1.get()==''or P2.get()==''or P3.get()==''or P4.get()=='':
        tkinter.messagebox.showwarning('警告', '请先填写完整年月日时后再计算')
    else:
        check_year = calendar.isleap(int(P1.get()))
        if int(P1.get())<1900 or int(P1.get())>2100 :
            tkinter.messagebox.showwarning('警告', '年份应该在1900-2100之间')
        elif int(P2.get())<1 or int(P2.get())>12 :
            tkinter.messagebox.showwarning('警告', '月份应该在1-12之间')
        elif int(P3.get())<1 or int(P3.get())>31 :
            tkinter.messagebox.showwarning('警告', '日期应该在1-31之间')
        elif check_year == True and int(P2.get())==2 and int(P3.get())>29:
            tkinter.messagebox.showwarning('警告', '闰年2月份只有29天')
        elif check_year == False and int(P2.get())==2 and int(P3.get())>28:
            tkinter.messagebox.showwarning('警告', '平年2月份只有28天')
        elif int(P2.get())==4 and int(P3.get())==31:
            tkinter.messagebox.showwarning('警告', '4月份只有30天')
        elif int(P2.get())==6 and int(P3.get())==31:
            tkinter.messagebox.showwarning('警告', '6月份只有30天')
        elif int(P2.get())==9 and int(P3.get())==31:
            tkinter.messagebox.showwarning('警告', '9月份只有30天')
        elif int(P2.get())==11 and int(P3.get())==31:
            tkinter.messagebox.showwarning('警告', '11月份只有30天')
        elif int(P4.get())<0 or int(P4.get())>23:
            tkinter.messagebox.showwarning('警告', '时间应该在0-23之间')
        else:
            Calcula = Calculation.calculation(P1.get(),P2.get(),P3.get(),P4.get())
            NL_name['state'] = 'normal'
            NL_name.delete(0,tk.END)
            NL_name.insert(0, Calcula[0])
            NL_name['state'] = 'disabled'
            BZ_name['state'] = 'normal'
            BZ_name.delete(0,tk.END)
            BZ_name.insert(0, Calcula[1])
            BZ_name['state'] = 'disabled'
            JG_name.delete(1.0,tk.END)
            for i in Calcula[2]:
                JG_name.insert(tk.INSERT, i)

app = tk.Tk()
P1 = tk.StringVar()
P2 = tk.StringVar()
P3 = tk.StringVar()
P4 = tk.StringVar()
P5 = tk.StringVar()
P6 = tk.StringVar()
test_cmd = app.register(validateText)

LtkF = tkF.Font(family='Times New Roman',size=40,weight=tkF.BOLD)
PtkF = tkF.Font(family='Times New Roman',size=20)
StkF = tkF.Font(family='Times New Roman',size=40)
TtkF = tkF.Font(family='Times New Roman')
BtkF = tkF.Font(family='Times New Roman',size=15,weight=tkF.BOLD)
DtkF = tkF.Font(family='Times New Roman',size=10,weight=tkF.BOLD)
# 设置窗口标题:
app.title('命理八字叶大师版')
app.geometry('1024x768')
app.resizable(0, 0)
#定义各种组件的样式字体等
Title_name =  tk.Label(app, text='命理八字及五行圆缺', bg='pink', font=('Times New Roman',18),width=50, height=2)
Edition = tk.Button(app, text='....',command=vision,font=DtkF, width=5,height=1)
L_name = tk.Label(app, text='公历：', bg='SkyBlue', relief= 'raised',font=LtkF,width=5, height=1)
Ye_name = tk.Entry(app,textvariable=P1,bd =16,relief= 'sunken',font=PtkF,width=6,validate="key",validatecommand = (test_cmd,'%P'))
Y_name = tk.Label(app, text='年', relief= 'raised',font=StkF,width=2, height=1)
Mo_name = tk.Entry(app,textvariable=P2,bd =16,relief= 'sunken',font=PtkF,width=6,validate="key",validatecommand = (test_cmd,'%P'))
M_name = tk.Label(app, text='月', relief= 'raised',font=StkF,width=2, height=1)
Da_name = tk.Entry(app,textvariable=P3,bd =16,relief= 'sunken',font=PtkF,width=6,validate="key",validatecommand = (test_cmd,'%P'))
D_name = tk.Label(app, text='日', relief= 'raised',font=StkF,width=2, height=1)
Ho_name = tk.Entry(app,textvariable=P4,bd =16,relief= 'sunken',font=PtkF,width=6,validate="key",validatecommand = (test_cmd,'%P'))
H_name = tk.Label(app, text='时', relief= 'raised',font=StkF,width=2, height=1)
N_name = tk.Label(app, text='农历：', bg='SkyBlue', relief= 'raised',font=LtkF,width=5, height=1)
NL_name = tk.Entry(app,textvariable=P5,bd =16, state='disabled',relief= 'sunken',font=PtkF,width=40)
B_name = tk.Label(app, text='八字：', bg='SkyBlue', relief= 'raised',font=LtkF,width=5, height=1)
BZ_name = tk.Entry(app,textvariable=P6,bd =16,state='disabled',relief= 'sunken',font=PtkF,width=40)
J_name = tk.Label(app, text='解卦：', bg='SkyBlue', relief= 'raised',font=LtkF,width=5, height=1)
JG_name = tk.Text(app,font=TtkF,width=124,height=21)
Show = tk.Button(app, text='计算',command=showC,font=BtkF, width=14,height=5)

Title_name.pack(side='top')
Edition.place(x=980,y=1,anchor='nw')
L_name.place(x=13,y=70,anchor='nw')
Ye_name.place(x=180,y=70,anchor='nw')
Y_name.place(x=310,y=70,anchor='nw')
Mo_name.place(x=390,y=70,anchor='nw')
M_name.place(x=520,y=70,anchor='nw')
Da_name.place(x=600,y=70,anchor='nw')
D_name.place(x=730,y=70,anchor='nw')
Ho_name.place(x=810,y=70,anchor='nw')
H_name.place(x=930,y=70,anchor='nw')
N_name.place(x=13,y=140,anchor='nw')
NL_name.place(x=180,y=140,anchor='nw')
B_name.place(x=13,y=210,anchor='nw')
BZ_name.place(x=180,y=210,anchor='nw')
J_name.place(x=13,y=280,anchor='nw')
JG_name.place(x=13,y=350,anchor='nw')
Show.place(x=810,y=140,anchor='nw')

app.mainloop()
