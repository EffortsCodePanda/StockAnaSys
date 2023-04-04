# -*- coding: UTF-8 -*-


#导入需要使用到的模块
import urllib
import urllib.request
import re
import os
import pandas as pd
import pymysql
import time
import shutil

#私有变量
_todayTime = time.strftime("%Y%m%d",(time.localtime()));
__filepath = 'C:\\data\\stock\\stock_' + _todayTime #+ '\\'    #放excel表格的位置
__dbName = 'root'                   #数据库账号
__dbPassword = 'Test_123'           #数据库密码,替换为自己的账户名和密码
#__CodeList = []                     #获取所有以6开头的股票代码的集合



def saveDataFromExcels():
	#建立本地数据库连接(需要先开启数据库服务)
	#db = pymysql.connect('localhost', name, password, charset='utf8')
	db = pymysql.connect(host='localhost', user='root', password= 'Test_123', charset='utf8')  #现在必须指定参数
	cursor = db.cursor()
	#创建数据库stockDataBase
	sqlSentence1 = "create database  if not exists stockDataBase"
	cursor.execute(sqlSentence1)#选择使用当前数据库
	sqlSentence2 = "use stockDataBase;"
	cursor.execute(sqlSentence2)

	#获取本地文件列表
	print(__filepath)
	fileList = os.listdir(__filepath)
	#依次对每个数据文件进行存储
	for fileName in fileList:
		sqlSentenceDel = "drop table if exists stock_%s;" % fileName[0:6]
		cursor.execute(sqlSentenceDel)

		#创建数据表，如果数据表已经存在，会跳过继续执行下面的步骤print('创建数据表stock_%s'% fileName[0:6])
		sqlSentence3 = "create table stock_%s" % fileName[0:6] + "(daydate date, stockcode VARCHAR(10),     name VARCHAR(10),\
                       closingprice float,    highestprice    float, lowestprice float, openingprice float, previousclosingprice float, riseandfall    float, \
                       riseandfallrange float, turnoverrate float, turnover bigint, turnoverprice bigint, totalmarketvalue bigint, circulationmarketvalue bigint)"
		cursor.execute(sqlSentence3)


		#迭代读取表中每行数据，依次存储（整表存储还没尝试过）
		print('正在存储stock_%s'% fileName[0:6])
		#data = pd.read_csv(__filepath+fileName, encoding="gbk")
		data = pd.read_csv(__filepath+fileName, encoding="gbk")
		length = len(data)
		for i in range(0, length):
			record = tuple(data.loc[i])
			#插入数据语句
			try:
				sqlSentence4 = "insert into stock_%s" % fileName[0:6] + "(daydate, stockcode, name, closingprice, highestprice, lowestprice, openingprice, previousclosingprice,\
				riseandfall, riseandfallrange, turnoverrate, turnover, turnoverprice, totalmarketvalue, circulationmarketvalue) values ('%s',%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % record
				#获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值
				sqlSentence4 = sqlSentence4.replace('nan','null').replace('None','null').replace('none','null') 
				cursor.execute(sqlSentence4)
			except:
				#如果以上插入过程出错，跳过这条数据记录，继续往下进行
				break

	#关闭游标，提交，关闭数据库连接
	cursor.close()
	db.commit()
	db.close()


if __name__ == '__main__':
	print('存储信息到数据库')
	saveDataFromExcels()

	print('over')

