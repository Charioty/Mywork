#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Charioty
# time:2020/3/24

import os
import shutil
import configparser
import sqlite3
import subprocess
import Calculater
import json


#加解密配置文件处理
class Encryption():
    def __init__(self,encryptFile,decryptFile):
        self.key = 0xa9
        self.encryptFile=encryptFile
        self.decryptFile=decryptFile
    # 加密处理
    def encrypt(self):
        F = open(self.decryptFile, "rb")
        E = open(self.encryptFile, "wb")
        data = F.read()
        lth = (data[0].bit_length() + 7) // 8
        dec_byte = int.to_bytes(data[0], lth, 'big')
        E.write(dec_byte)
        data = data[1:]
        for i in data:
            decrypted = i ^ self.key
            length = (decrypted.bit_length() + 7) // 8
            decrypted_bytes = int.to_bytes(decrypted, length, 'big')
            E.write(decrypted_bytes)
        E.close()
        F.close()
        print('Profile encryption complete')

    # 解密处理
    def decrypt(self):
        M = open(self.encryptFile, "rb")
        N = open(self.decryptFile, "wb")
        data = M.read()
        lth = (data[0].bit_length() + 7) // 8
        dec_byte = int.to_bytes(data[0], lth, 'big')
        N.write(dec_byte)
        data = data[1:]
        for i in data:
            decrypted = i ^ self.key
            length = (decrypted.bit_length() + 7) // 8
            decrypted_bytes = int.to_bytes(decrypted, length, 'big')
            N.write(decrypted_bytes)
        N.close()
        M.close()
        print('Profile decryption complete')

#读取Json文件
def readJsonFileToStr(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.readlines()
        f.close()
    return text
#将学习阈值写入Json文件
def setJsonFileTH(file_name,txt):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.writelines(txt)
        f.close()
#读取所需配置处理
def conf():
    config = configparser.ConfigParser()
    config.read("conf.ini")
    S_Url = config.get("config","Source_Url")
    Level = config.get("option","Level")
    upLevel = config.get("option","upLevel")
    return S_Url,Level,upLevel
#拷贝学习数据
def copy_data(url):
    L_Url = url + '_L'
    # mkdir(L_Url)
    shutil.copytree(url, L_Url)
    print('copy files finished!')
    return L_Url
#不学习跑库
def run_nolearn(url):
    Url = url+'\VksTestDemo.exe'
    print('Testing for the first time: no_learn')
    child = subprocess.Popen(Url, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    child.communicate()
    # os.system(Url)
    print('no_learn complete')
#获取学习阈值
def get_Threshold(url,L1,up):
    conn = sqlite3.connect(url+'\MatchResult.dat')
    c = conn.cursor()
    Data_Sum_nor = c.execute("SELECT count(*) FROM MatchResult WHERE MatchType = 0 and SampleID not like '%light%'  and SampleID like '%FT$0%' ").fetchall()
    Data_Sum_dry = c.execute("SELECT count(*) FROM MatchResult WHERE MatchType = 0 and SampleID not like '%light%'  and SampleID like '%FT$1%' ").fetchall()
    num1 = round(Data_Sum_nor[0][0] / int(L1))+1
    num2 = round(Data_Sum_dry[0][0] / int(L1))+1
    THS_temp_nor = c.execute("select Score from MatchResult where MatchType = 0 and SampleID not like '%light%' and SampleId like'%FT$0%' order by Score DESC limit ?", (num1,)).fetchall()
    THS_temp_dry = c.execute("select Score from MatchResult where MatchType = 0 and SampleID not like '%light%' and SampleId like'%FT$1%' order by Score DESC limit ?", (num2,)).fetchall()
    return THS_temp_nor[0][0]+int(up),THS_temp_nor[num1-1][0]+1,THS_temp_dry[0][0]+int(up),THS_temp_dry[num2-1][0]+1#查出分数+1
    c.close()
    conn.close()
    print('Get threshold successfully')
#设置学习阈值
def setTh(json_path,LS,LT,SLT,DLT,DSLT):
    text = readJsonFileToStr(json_path)
    for j,i in enumerate(text):
        if 'isLearningOnLine' in i :
            text[j]=i.replace(i[i.find(":")+1:-2],LS)
        if '"vt":'in i :
            text[j]=i.replace(i[i.find(":")+1:-2],LT)
        if '"dvt":'in i :
            text[j]=i.replace(i[i.find(":")+1:-2],DLT)
        if '"clt":'in i :
            text[j]=i.replace(i[i.find(":")+1:-2],LT)
        if '"dclt":'in i :
            text[j]=i.replace(i[i.find(":")+1:-2],DLT)
        if '"slt":'in i :
            text[j]=i.replace(i[i.find(":")+1:-2],SLT)
        if '"dslt":'in i :
            text[j]=i.replace(i[i.find(":")+1:-1],DSLT)
    text=''.join(text)
    setJsonFileTH(json_path, text)
#学习跑库
def run_learn(url):
    Url = url+'\VksTestDemo.exe'
    print('Testing for the second time: learn')
    child = subprocess.Popen(Url, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    child.communicate()
    print('learn complete')

if __name__ == "__main__":
    noUrl = conf()[0]
    Level = conf()[1]
    upLevel = conf()[2]
    LearnUrl = copy_data(noUrl)
    decryptFile_no = noUrl + '\config.ini'
    encryptFile_no = noUrl + '\config.en'
    no_Json = noUrl +'\SensorData.json'
    Encryption(encryptFile_no, decryptFile_no).encrypt()
    shutil.copy(no_Json,'./')
    run_nolearn(noUrl)
    Encryption(encryptFile_no, decryptFile_no).decrypt()
    LThershold_nor = get_Threshold(noUrl,Level,upLevel)[1]
    SLThershold_nor = get_Threshold(noUrl,Level,upLevel)[0]
    DLThershold_dry = get_Threshold(noUrl,Level,upLevel)[3]
    DSLThershold_dry = get_Threshold(noUrl,Level,upLevel)[2]
    json_path = LearnUrl + '\SensorData.json'
    decryptFile_L = LearnUrl + '\config.ini'
    encryptFile_L = LearnUrl + '\config.en'
    L_Json = LearnUrl + '\SensorData.json'
    setTh(json_path, ' 1',str(LThershold_nor), str(SLThershold_nor), str(DLThershold_dry), str(DSLThershold_dry))
    Encryption(encryptFile_L, decryptFile_L).encrypt()
    shutil.copy(L_Json, './')
    run_learn(LearnUrl)
    Encryption(encryptFile_L, decryptFile_L).decrypt()
    shutil.copyfile('result_T.xlsx', 'result.xlsx')
    print('Calculating no learning test results')
    Calculater.Calculater(noUrl)
    print('Calculating learning run results')
    Calculater.Calculater(LearnUrl)
    os.rename('result.xlsx', noUrl[noUrl.rfind('\\')+1:]+'_result.xlsx')
    print('Test completed, please check the results')
