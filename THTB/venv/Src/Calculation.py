#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Charioty
# time:2019/6/21

import  sxtwl
import Elements

Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ShX = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
numCn = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑","白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"]
ymc = ["十一", "十二", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十" ]
rmc = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]
Five_elements = ["金", "木", "水", "火", "土"]
F_elements = [["甲","木"], ["乙","木"],["丙","火"],["丁","火"],["戊","土"],["己","土"],["庚","金"],["辛","金"],["壬","水"],["癸","水"],["子","水"],["丑","土"],["寅","木"],["卯","木"],["辰","土"],["巳","火"],["午","火"],["未","土"],["申","金"],["酉","金"],["戌","土"],["亥","水"]]

def element(Branch):
    elements = [0,1,2,3,4,5,6,7]
    for m,n in enumerate(Branch):
        x = 0
        while x < 22:
            if F_elements[x][0] == n:
                elements[m] = F_elements[x][1]
                break
            x=x+1
    return elements

def calculation(Y,M,D,H):
    # Y = int(input('输入阳历年：'))
    # M = int(input('输入月份：'))
    # D = int(input('输入日期：'))
    # H = int(input('输入时间：'))
    lunar = sxtwl.Lunar()  #实例化日历库
    day = lunar.getDayBySolar(int(Y),int(M), int(D))  # 查询年月日
    gz = lunar.getShiGz(day.Lday2.tg,  int(H))
    Branch = [Gan[day.Lyear2.tg],Zhi[day.Lyear2.dz],Gan[day.Lmonth2.tg],Zhi[day.Lmonth2.dz],Gan[day.Lday2.tg], Zhi[day.Lday2.dz],Gan[gz.tg], Zhi[gz.dz]]
    elements=element(Branch)
    elements =Elements.elements(elements)
    # print("公历:", day.y, "年", day.m, "月", day.d, "日")
    if day.Lleap:
        Lunar_c = "润"+ymc[day.Lmc]+"月 "+rmc[day.Ldi]+"日"
    else:
        Lunar_c = ymc[day.Lmc]+"月 "+rmc[day.Ldi]+"日"
    # print("儒略日:JD", sxtwl.J2000 + day.d0)
    # print("星期", numCn[day.week])
    # print(Gan[day.Lyear2.tg], Zhi[day.Lyear2.dz], "年", Gan[day.Lmonth2.tg],Zhi[day.Lmonth2.dz], "月", \
    #       Gan[day.Lday2.tg], Zhi[day.Lday2.dz], "日", Gan[gz.tg], Zhi[gz.dz], "时")
    # print(Branch)
    # print(elements)
    return Lunar_c,Branch,elements
