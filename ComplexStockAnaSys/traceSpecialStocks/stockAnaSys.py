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
import random
# ,encoding='utf-8'


#私有变量
__dbName = 'root'                   #数据库账号
__dbPassword = 'Test_123'           #数据库密码,替换为自己的账户名和密码
_todayTime = time.strftime("%Y%m%d",(time.localtime()));
_excelsPath = 'F:\\data\\specialStocks\\stock_' + _todayTime + '\\'

__rstfilepath = 'F:\\LearnFile\\language\\python\\project\\gupiao\\traceSpecialStocks\\result.txt'
_file = None

#__regectStock_trace_sh = {600507}
__regectStock_trace_sh = {600507, 601006, 601118, 600775, 601988, 601328, 600681, 600028, 601700, 603169, 600533, 600280, 601000, 600740}
#__regectStock_trace_sz = {002394, 000488, 002110, 000678}



#生成指定目录,如果有就先删除再创建
def createDirForStockExcels():
	#判单某个目录是否存在
	path = _excelsPath
	if os.path.isdir(path):
		#os.rmdir(path) --只能删除空目录
		shutil.rmtree(path)

	#创建 F:\\data\\stock\\ 目录
	os.mkdir(path)
	return path


def getAllStockExcels():
	filepath = createDirForStockExcels() #定义数据文件保存路径
	#将网页上文件下载并保存到本地csv文件，注意日期
	#todayTime = time.strftime("%Y%m%d",(time.localtime()));
	for code in __regectStock_trace_sh:
		time.sleep(random.random())
		print('正在获取股票%s数据'%code)
		url = 'http://quotes.money.163.com/service/chddata.html?code=0'+str(code)+\
			'&end='+ _todayTime + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
		#print(url)
		try:
			urllib.request.urlretrieve(url, filepath+str(code)+'.csv')
		except:
			print('获取股票%s数据出现异常'%code)


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
	fileList = os.listdir(_excelsPath)
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
		data = pd.read_csv(_excelsPath+fileName, encoding="gbk")
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

	
def createFile():
	if  os.path.exists(__rstfilepath):
		os.remove(__rstfilepath)
	file = open('result.txt','w+')
	file.close()

	
def getFile():
	if  not os.path.exists(__rstfilepath):
		print('create file')
		file = open('result.txt','w+')
		file.write('\n' + _todayTime + ': \n')
		return file	
	#with open(__rstfilepath, 'a') as f1:
	f1 = open(__rstfilepath, 'a')
	print('use exist file')
	f1.write('\n' + _todayTime + ': \n')
	return f1
	
	
def findTargetPriceStock(cursor, code, targerPrice, file):
	#找出当前价格
	sql = "SELECT * FROM stock_%s" %code + " order by daydate Desc limit 1;"
	#print(sql)
	
	try:
		# 执行SQL语句
		cursor.execute(sql)
		# 获取所有记录列表
		results = cursor.fetchall()
		for row in results:
			currPrice = row[3]
			# 打印结果
			#print ("currPrice=%s" % currPrice)
	except:
		print ("Error: unable to fetch data")
		return
			
	if (currPrice > targerPrice):
		return
	
	
	str = "stockeCode:%-10s curr:%-8.4f target%-8.4f " %(code,currPrice,targerPrice)
	file.write(str + '\n')


def getSpecStocks():
	# 打开数据库连接
	db = pymysql.connect(host='localhost', user='root', password= 'Test_123', charset='utf8') 
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	#fileName = '600280'
	
	# SQL 查询语句
	sqlSentence2 = "use stockDataBase;"
	cursor.execute(sqlSentence2)
	#createFile()
	_file = getFile()

	currPrice = 0.0

	findTargetPriceStock(cursor, 600507, 7.2, _file)
	findTargetPriceStock(cursor, 601006, 6.4, _file)
	findTargetPriceStock(cursor, 601118, 5.0, _file)
	findTargetPriceStock(cursor, 600775, 6.6, _file)
	findTargetPriceStock(cursor, 601988, 3.1, _file)
	findTargetPriceStock(cursor, 601328, 4.6, _file)
	findTargetPriceStock(cursor, 600681, 5.0, _file)
	findTargetPriceStock(cursor, 600028, 4.2, _file)
	findTargetPriceStock(cursor, 603169, 4.5, _file)
	findTargetPriceStock(cursor, 600533, 2.9, _file)
	findTargetPriceStock(cursor, 600280, 2.8, _file)
	findTargetPriceStock(cursor, 601000, 2.3, _file)
	findTargetPriceStock(cursor, 600740, 5.3, _file)
	
	_file.close()

	# 关闭数据库连接
	db.close()


if __name__ == '__main__':
	print('下载excels')
	getAllStockExcels()
	print('存储信息到数据库')
	saveDataFromExcels()	
	print('分析股票数据')
	getSpecStocks()		
	print('over')	
	

	
'''
600507 方大特钢 7.2元
601006 大秦铁路 6.4元
601118 海南橡胶 5元
600775 南京熊猫 6.6元
601988 中国银行 3.1
601328 交通银行 4.6元
600681 百川能源 5元
600028 中国石化 4.2元
601700 风范股份 4.5元
603169 兰石重装 4.5元
600533 栖霞建设 2.9元
600280 中央商场 2.8元
601000 唐山港   2.3元
600740 山西焦化 5.3元


002394 联发股份 7.5
000488 晨鸣纸业 6.4元
002110 三钢闽光 7元
000678 襄阳轴承 4.7元
'''	

'''
http://quotes.money.163.com/service/chddata.html?code=0600507&end=20220306&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP
'''