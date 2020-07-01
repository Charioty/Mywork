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
#读取所需配置处理
def conf():
    config = configparser.ConfigParser()
    config.read("conf.ini")
    S_Url = config.get("config","Source_Url")
    Level = config.get("option","Level")
    return S_Url,Level
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
def get_Threshold(url,L1):
    conn = sqlite3.connect(url+'\MatchResult.dat')
    c = conn.cursor()
    Data_Sum = c.execute("SELECT count(*) FROM MatchResult WHERE MatchType = 0").fetchall()
    num1 = round(Data_Sum[0][0] / int(L1))+1
    THS_temp = c.execute("select Score from MatchResult where MatchType = 0 order by Score DESC limit ?", (num1,)).fetchall()
    return THS_temp[0][0]+1,THS_temp[num1-1][0]+1#查出分数+1
    c.close()
    conn.close()
    print('Get threshold successfully')
#学习跑库
def run_learn(url):
    Url = url+'\VksTestDemo.exe'
    print('Testing for the second time: learn')
    child = subprocess.Popen(Url, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    child.communicate()
    print('learn complete')
#获取FRR结果

if __name__ == "__main__":
    noUrl = conf()[0]
    Level = conf()[1]
    LearnUrl = copy_data(noUrl)
    decryptFile_no = noUrl + '\config.ini'
    encryptFile_no = noUrl + '\config.en'
    Encryption(encryptFile_no, decryptFile_no).encrypt()
    run_nolearn(noUrl)
    Encryption(encryptFile_no, decryptFile_no).decrypt()
    LThershold = get_Threshold(noUrl,Level)[0]
    LVThershold = get_Threshold(noUrl,Level)[1]
    decryptFile_L = LearnUrl + '\config.ini'
    encryptFile_L = LearnUrl + '\config.en'
    curpath = os.path.dirname(os.path.realpath(__file__))
    cfgpath = os.path.join(curpath, decryptFile_L)
    config = configparser.ConfigParser()
    config.read(cfgpath)
    config.set("General","LearnThreshold",str(LThershold))
    config.set("General","LVThreshold",str(LVThershold))
    config.set("General","LearnOnline",'1')
    config.write(open(cfgpath, "w"))
    Encryption(encryptFile_L, decryptFile_L).encrypt()
    run_learn(LearnUrl)
    Encryption(encryptFile_L, decryptFile_L).decrypt()
    shutil.copyfile('result_T.xlsx', 'result.xlsx')
    print('Calculating no learning test results')
    Calculater.Calculater(noUrl)
    print('Calculating learning run results')
    Calculater.Calculater(LearnUrl)
    os.rename('result.xlsx', noUrl[noUrl.rfind('\\')+1:]+'_result.xlsx')
    print('Test completed, please check the results')
