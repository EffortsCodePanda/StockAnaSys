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
import string
# ,encoding='utf-8'


#私有变量
__dbName = 'root'                   #数据库账号
__dbPassword = 'Test_123'           #数据库密码,替换为自己的账户名和密码
_todayTime = time.strftime("%Y%m%d",(time.localtime()));
_excelsPath = 'F:\\data\\shenstock_' + _todayTime + '\\'
__CodeList = []
#__rstfilepath = 'F:\LearnFile\language\python\project\gupiao\result.txt'
__rstfilepath = 'F:\\LearnFile\\language\\python\\project\\gupiao\\result.txt'
_file = None
#__filepath = 'F:\\data\\shenstock_all_20210405\\'    #放excel表格的位置
__filepath = 'F:\\data\\shenstock_' + _todayTime + '\\'

__regectStock_chongfu = {3000}
__regectStock_tuishi = {3001}


#获取所有以6开头的股票代码的集合 600001,600002等等,写死遍历获得	
def getRangeAllStockCode():
	for i in range(1, 2500):
		if (i in __regectStock_tuishi or i in __regectStock_chongfu):
		    continue
		stringCodeTemp='%d06' %i
		print("code:%s" %stringCodeTemp)
		__CodeList.append(stringCodeTemp)			
	return __CodeList


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

'''
#爬虫抓取网页函数
def getHtml(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode('utf-8')
    return html


#获取所有的股票编号，正则表达式带（）时，返回值只包含括号里内容，即股票编号数组
def getStackCode(html):
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    return code


#获取所有以6开头的股票代码的集合 600001,600002等等	
def getAllStockCode():
	#东方财富网股票网址
	Url = 'http://quote.eastmoney.com/stocklist.html'
	#进行抓取
	code = getStackCode(getHtml(Url))	
	#获取所有以6开头的股票代码的集合
	CodeList = []
	for item in code:
		if item[0]=='6':
			CodeList.append(item)
	return CodeList


#下载指定的股票，数据一直到今天的日期	
def getSpecStockExcels():
	filepath = createDirForStockExcels() #定义数据文件保存路径
	CodeListTemp = ['600280','603169']
	#将网页上文件下载并保存到本地csv文件，注意日期
	#todayTime = time.strftime("%Y%m%d",(time.localtime()));
	for code in CodeListTemp:
		print('正在获取股票%s数据'%code)
		url = 'http://quotes.money.163.com/service/chddata.html?code=0'+code+\
			'&end='+ _todayTime + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
		urllib.request.urlretrieve(url, filepath+code+'.csv')


'''	


#下载所有的6开头的股票，数据一直到今天的日期	
def getAllStockExcels():
	filepath = createDirForStockExcels() #定义数据文件保存路径
	#将网页上文件下载并保存到本地csv文件，注意日期
	#todayTime = time.strftime("%Y%m%d",(time.localtime()));
	for code in __CodeList:
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


def getSpecStocks():
	# 打开数据库连接
	db = pymysql.connect(host='localhost', user='root', password= 'Test_123', charset='utf8') 
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	
	# SQL 查询语句
	sqlSentence2 = "use stockDataBase;"
	cursor.execute(sqlSentence2)
	#createFile()
	_file = getFile()

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
		str = "stockeCode:%-10s curr:%-8.4f high%-8.4f low%-8.4f" %(code,currPrice,highPrice,lowPrice)
		_file.write(str + '\n')
		
		#print ("stockeCode:%-10s curr:%-8.4f high%-8.4f low%-8.4f" %(code,currPrice,highPrice,lowPrice))
	_file.close()

	# 关闭数据库连接
	db.close()


if __name__ == '__main__':
	print('获取要处理的股票编号')
	getRangeAllStockCode()
	print('下载excels')
	getAllStockExcels()
	print('存储信息到数据库')
	saveDataFromExcels()	
	print('分析股票数据')
	getSpecStocks()		
	print('over')	
	
