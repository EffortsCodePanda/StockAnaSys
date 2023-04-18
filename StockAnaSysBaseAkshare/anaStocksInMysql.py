# -*- coding: UTF-8 -*-
#!/usr/bin/python3

import pymysql
import os
import time

__ShCodeList = []
__SzCodeList = []
_todayTime = time.strftime("%Y%m%d",(time.localtime()));
_file = None

def getFile():
	currPath = os.path.abspath('.')
	filepath = currPath + "\\result.txt"
	if not os.path.exists(filepath):
		print('create file')
		file = open('result.txt','w+', encoding="utf-8") #不加utf-8,写进去之后会乱码
		file.write('\n' + _todayTime + ': \n')
		return file

	f1 = open(filepath, 'a', encoding="utf-8")
	print('use exist file')
	f1.write('\n' + _todayTime + ': \n')
	return f1

#获取所有以6开头的股票代码的集合 600001,600002等等,写死遍历获得
def getAllShStockCode(): #得到沪市的股票
	for i in range(1,5599): #5599
		item = 600000+i
		__ShCodeList.append(item)

#获取所有以6开头的股票代码的集合 600001,600002等等,写死遍历获得
def getAllSzStockCode(): #得到沪市的股票
	for i in range(1,3599): #3599
		item = str(i).zfill(6)  #000001  #item = "000000"+i error
		__SzCodeList.append(item)

	# for i in range(1,1599): #创业板，暂时不在分析范围
	# 	item = "300000"+i
	# 	__SzCodeList.append(item)

def getSpecStocks():
	# 打开数据库连接
	db = pymysql.connect(host='localhost', user='root', password= 'Test_123', charset='utf8') 
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	#fileName = '600280'

	# SQL 查询语句
	sqlSentence2 = "use stockDb;"
	cursor.execute(sqlSentence2)
	getAllShStockCode()
	getAllSzStockCode()

	_file = getFile()

	currPrice = 0.0
	highPrice = 0.0
	lowPrice = 0.0
	stockMode = "NULL"
	stockName = "NULL"
	_file.write('------------------------------------沪市分析开始------------------------------------------\n')
	for code in __ShCodeList:
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
			continue

		#当前价格为0，退市或者停盘
		if (currPrice == 0):
			continue

		#找出最低价格
		sql = "SELECT * FROM stock_%s" %code + " WHERE TO_DAYS(NOW()) - TO_DAYS(daydate) <= 1100 and closingprice>0 order by closingprice Asc limit 1;  "
		#print(sql)
		try:
			# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表
			results = cursor.fetchall()
			for row in results:
				lowPrice = row[3]
				stockName = row[1]
				#print("沪市名称：%s" %stockName)
				# 打印结果
				#print ("lowPrice=%s" % lowPrice)
		except:
			print ("Error: unable to fetch data")
			continue

		#找出最高价格
		sql = "SELECT * FROM stock_%s" %code + " WHERE TO_DAYS(NOW()) - TO_DAYS(daydate) <= 1100 order by closingprice Desc limit 1; "
		#print(sql)
		try:
			# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表
			results = cursor.fetchall()
			for row in results:
				highPrice = row[3]
				# 打印结果
				#print ("highPrice=%s" % highPrice) 
		except:
			print ("Error: unable to fetch data")
			continue

		#这边判断才是核心的，筛选出自己想要的股票
		if (currPrice > 15.0):
			continue

		if (highPrice/currPrice < 3.0):
			continue

		if (currPrice/lowPrice > 1.2):
			continue
		if (currPrice/lowPrice < 1.05):
			continue
		str = "stockeCode:%-10s stockeName:%-20s curr:%-8.4f high%-8.4f low%-8.4f" %(code,stockName,currPrice,highPrice,lowPrice)
		_file.write(str + '\n')
		#print ("stockeCode:%-10s curr:%-8.4f high%-8.4f low%-8.4f" %(code,currPrice,highPrice,lowPrice))
	_file.write('------------------------------------沪市分析结束------------------------------------------\n')


	_file.write('------------------------------------深市分析开始------------------------------------------\n')
	for code in __SzCodeList:
		#找出当前价格
		sql = "SELECT * FROM stock_%s" %code + " order by daydate Desc limit 1;"
		#print(sql)
		try:
			# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表
			results = cursor.fetchall()
			for row in results:
				#print(row)
				currPrice = row[3]
				stockMode = row[7]
				#print(stockMode)
				stockName = row[1]
				#print(stockName)
				# 打印结果
				#print ("currPrice=%s" % currPrice)
		except:
			print ("Error: unable to fetch data")
			continue

		#当前价格为0，退市或者停盘
		if (currPrice == 0):
			continue

		#找出最低价格
		sql = "SELECT * FROM stock_%s" %code + " WHERE TO_DAYS(NOW()) - TO_DAYS(daydate) <= 1100 and closingprice>0 order by closingprice Asc limit 1;  "
		#print(sql)
		try:
			# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表
			results = cursor.fetchall()
			for row in results:
				lowPrice = row[3]
				# 打印结果
				#print ("lowPrice=%s" % lowPrice)
		except:
			print ("Error: unable to fetch data")
			continue

		#找出最高价格
		sql = "SELECT * FROM stock_%s" %code + " WHERE TO_DAYS(NOW()) - TO_DAYS(daydate) <= 1100 order by closingprice Desc limit 1; "
		#print(sql)
		try:
			# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表
			results = cursor.fetchall()
			for row in results:
				highPrice = row[3]
				# 打印结果
				#print ("highPrice=%s" % highPrice)
		except:
			print ("Error: unable to fetch data")
			continue

		#这边判断才是核心的，筛选出自己想要的股票
		if (currPrice > 15.0):
			continue

		# if (highPrice/currPrice < 3.0):
		# 	continue

		if (currPrice/lowPrice > 1.2):
			continue
		# if (currPrice/lowPrice < 1.05):
		# 	continue
		str = "stockeCode:%-10s stockeName:%-20s curr:%-8.4f high%-8.4f low%-8.4f model%-20s" %(code,stockName,currPrice,highPrice,lowPrice,stockMode)
		_file.write(str + '\n')
		#print ("stockeCode:%-10s curr:%-8.4f high%-8.4f low%-8.4f" %(code,currPrice,highPrice,lowPrice))

	_file.write('------------------------------------深市分析结束------------------------------------------\n')

	_file.close()

	# 关闭数据库连接
	db.close()

if __name__ == '__main__':
	print('分析股票数据开始......')
	getSpecStocks()
	print('分析股票数据结束......')