#导入需要使用到的模块
import urllib
import urllib.request
import re
import os
import pandas as pd
import pymysql

##########################将股票数据存入数据库###########################
filepath = 'F:\\data\\stock\\'#定义数据文件保存路径

#数据库名称和密码
name = 'root'
password = 'Test_123'  #替换为自己的账户名和密码
#建立本地数据库连接(需要先开启数据库服务)
#db = pymysql.connect('localhost', name, password, charset='utf8')
db = pymysql.connect(host='localhost', user='root', password= 'Test_123', charset='utf8')
cursor = db.cursor()
#创建数据库stockDataBase
sqlSentence1 = "create database  if not exists stockDataBase"
cursor.execute(sqlSentence1)#选择使用当前数据库
sqlSentence2 = "use stockDataBase;"
cursor.execute(sqlSentence2)

#获取本地文件列表
fileList = os.listdir(filepath)
#依次对每个数据文件进行存储
for fileName in fileList:
	sqlSentenceDel = "drop table if exists stock_%s;" % fileName[0:6]
	cursor.execute(sqlSentenceDel)
	
	#创建数据表，如果数据表已经存在，会跳过继续执行下面的步骤print('创建数据表stock_%s'% fileName[0:6])
	sqlSentence3 = "create table stock_%s" % fileName[0:6] + "(日期 date, 股票代码 VARCHAR(10),     名称 VARCHAR(10),\
                       收盘价 float,    最高价    float, 最低价 float, 开盘价 float, 前收盘 float, 涨跌额    float, \
                       涨跌幅 float, 换手率 float, 成交量 bigint, 成交金额 bigint, 总市值 bigint, 流通市值 bigint)"
	cursor.execute(sqlSentence3)


	#迭代读取表中每行数据，依次存储（整表存储还没尝试过）
	print('正在存储stock_%s'% fileName[0:6])
	#data = pd.read_csv(filepath+fileName, encoding="gbk")
	data = pd.read_csv(filepath+fileName, encoding="gbk")
	length = len(data)
	for i in range(0, length):
		record = tuple(data.loc[i])
		#插入数据语句
		try:
			sqlSentence4 = "insert into stock_%s" % fileName[0:6] + "(日期, 股票代码, 名称, 收盘价, 最高价, 最低价, 开盘价, 前收盘, 涨跌额, 涨跌幅, 换手率, \
			成交量, 成交金额, 总市值, 流通市值) values ('%s',%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % record
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
