#!/usr/bin/python
# -*- coding:utf-8 -*-

import pymysql
import akshare as ak
import time
import os

sqlCrtDateBase = "create database if not exists stockDb;"
sqlEntryDateBase = "use stockDb;"
__CyCodeList = []
_todayTime = time.strftime("%Y%m%d",(time.localtime()));
#_file = None

def getAllCyStockCode(): #得到创业板的股票
	for i in range(1,5599): #5599
		item = 300000+i
		__CyCodeList.append(item)

def getFile():
	currPath = os.path.abspath('.')
	print(currPath)
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

def saveCyDataFromAkshareRsp():
    #建立本地数据库连接(需要先开启数据库服务)
    db = pymysql.connect(host='localhost', user='root', password= 'Test_123', charset='utf8')  #现在必须指定参数
    cursor = db.cursor()
    cursor.execute(sqlCrtDateBase)#选择使用当前数据库
    cursor.execute(sqlEntryDateBase)
    count = 0

    _todayTime = time.strftime("%Y%m%d",(time.localtime()));

    stock_info_sz_code_name_df = ak.stock_info_sz_name_code()
    for rowTuplesCode in stock_info_sz_code_name_df.itertuples():
        count = count+1
        if (0 == count % 500):
            time.sleep(3)  #每下载500条数据，休眠3s

        stockCode = getattr(rowTuplesCode, "A股代码")
        if (stockCode<"300000"):
            continue

        #print("只入库创业板")
        # if (stockCode<"000669"): #有时候会被禁掉，从之前断掉的地方开始，第一次跑的时候，这边要注释掉
        #     continue
        stockName = getattr(rowTuplesCode, "A股简称")
        stockModel = getattr(rowTuplesCode, "所属行业")

        sqlSentenceDel = "drop table if exists stock_%s;" % stockCode
        cursor.execute(sqlSentenceDel)

        #创建数据表，如果数据表已经存在，会跳过继续执行下面的步骤print('创建数据表stock_%s'% fileName[0:6])
        sqlSentence3 = "create table stock_%s" % stockCode + "(stockcode VARCHAR(10), name VARCHAR(10), daydate date, \
                closingprice float, openingprice float,    highestprice    float, lowestprice float, stockmodel VARCHAR(100))"
        cursor.execute(sqlSentence3)

        stock_df = ak.stock_zh_a_hist(symbol=stockCode, period="daily", start_date='20200101', end_date=_todayTime, adjust="")

        for rowTuple in stock_df.itertuples(): #type(rowTuple) is : <class 'pandas.core.frame.Pandas'>
            date = getattr(rowTuple, '日期');
            closingprice = getattr(rowTuple, '收盘');
            openingprice = getattr(rowTuple, '开盘');
            highestprice = getattr(rowTuple, '最高');
            lowestprice = getattr(rowTuple, '最低');
            #插入数据语句
            try:
                sqlSentence4 = "insert into stock_%s" % stockCode + "(stockcode, name, daydate, closingprice, openingprice, highestprice, lowestprice, stockmodel)\
                values ('%s','%s','%s',%s,%s,%s,%s,'%s')" %(stockCode, stockName, date, closingprice, openingprice, lowestprice, highestprice, stockModel)
                #获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值
                sqlSentence4 = sqlSentence4.replace('nan','null').replace('None','null').replace('none','null') 
                cursor.execute(sqlSentence4)
            except:
                #如果以上插入过程出错，跳过这条数据记录，继续往下进行
                print(stockCode ,' insert failure')
                print(sqlSentence4)
                #break #调试000001第一条插入错误的

        print(stockCode, "_", stockName, " the ending")
        #break #调试000001

	#关闭游标，提交，关闭数据库连接
    cursor.close()
    db.commit()
    db.close()
    print("all shenzhen stock the ending......")

def getSpecStocks():
	# 打开数据库连接
	db = pymysql.connect(host='localhost', user='root', password= 'Test_123', charset='utf8') 
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	#fileName = '600280'

	# SQL 查询语句
	sqlSentence2 = "use stockDb;"
	cursor.execute(sqlSentence2)
	getAllCyStockCode()

	_file = getFile()

	currPrice = 0.0
	highPrice = 0.0
	lowPrice = 0.0
	stockMode = "NULL"
	stockName = "NULL"
	_file.write('------------------------------------创业板分析开始------------------------------------------\n')
	for code in __CyCodeList:
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
				stockMode = row[7]
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

		if (currPrice/lowPrice > 1.2):
			continue

		str = "stockeCode:%-10s stockeName:%-20s curr:%-8.4f high%-8.4f low%-8.4f model%-20s" %(code,stockName,currPrice,highPrice,lowPrice,stockMode)
		_file.write(str + '\n')
		#print ("stockeCode:%-10s curr:%-8.4f high%-8.4f low%-8.4f" %(code,currPrice,highPrice,lowPrice))
	_file.write('------------------------------------创业板分析结束------------------------------------------\n')

	_file.close()

	# 关闭数据库连接
	db.close()

if __name__ == "__main__":
    print("保存创业板股票开始......")
    #saveCyDataFromAkshareRsp()
    print("分析创业板股票开始......")
    getSpecStocks()