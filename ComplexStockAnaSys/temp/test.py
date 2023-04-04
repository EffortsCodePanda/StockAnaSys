# -*- coding: UTF-8 -*-

#!/usr/bin/python3
 
import pymysql
import os

__CodeList = []
 
# 打开数据库连接
db = pymysql.connect(host='localhost', user='root', password= 'Test_123', charset='utf8') 
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
fileName = '600280'
__filepath = 'D:\LearnFile\language\python\project\gupiao\result.txt'

def createFile():
	if  os.path.exists(__filepath):
		os.remove(__filepath)
	file = open('result.txt','w+')
	file.close()

#获取所有以6开头的股票代码的集合 600001,600002等等,写死遍历获得
#2506 这个有问题 要跳过去
def getAllStockCodeNew():
	for i in range(0,2500):
		if (i == 2506):
			continue
		item = 600000+i
		__CodeList.append(item)	

		
# SQL 查询语句
sqlSentence2 = "use stockDataBase;"
cursor.execute(sqlSentence2)
#getAllStockCodeNew()
createFile()

currPrice = 0.0
highPrice = 0.0
lowPrice = 0.0

for code in __CodeList:
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
		
	if (currPrice > 15.0):
		continue
	
	if (highPrice/currPrice < 3.0):
		continue
		
	if (currPrice/lowPrice > 1.2):
		continue
		
	print ("stockeCode:%-10s curr:%-8.4f high%-8.4f low%-8.4f" %(code,currPrice,highPrice,lowPrice))

		
# 关闭数据库连接
db.close()
	
