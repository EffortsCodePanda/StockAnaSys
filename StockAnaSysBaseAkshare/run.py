#!/usr/bin/python
# -*- coding:utf-8 -*-

import saveDataToMysql as sd
import anaStocksInMysql as ad
import time

print("保存沪市股票开始......")
sd.saveSHDataFromAkshareRsp()

time.sleep(5) #沪市下载完之后，暂停5s，防止被限流
print("保存深市股票开始......")
sd.saveSzDataFromAkshareRsp()

print('分析股票数据开始......')
ad.getSpecStocks()
print('分析股票数据结束......')


