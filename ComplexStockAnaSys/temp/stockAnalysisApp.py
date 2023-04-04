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
__filepath = 'F:\\data\\stock_all\\'    #放excel表格的位置
__dbName = 'root'                   #数据库账号
__dbPassword = 'Test_123'           #数据库密码,替换为自己的账户名和密码
__CodeList = []                     #获取所有以6开头的股票代码的集合

#生成指定目录,如果有就先删除再创建
def createDirForStockExcels():
	#判单某个目录是否存在
	if os.path.isdir(__filepath):
		#os.rmdir(__filepath) --只能删除空目录
		shutil.rmtree(__filepath)

	#创建 F:\\data\\stock\\ 目录
	os.mkdir(__filepath)
	
#生成指定目录,如果有就先删除再创建
def useExistDirForStockExcels():
	#判单某个目录是否存在
	if os.path.isdir(__filepath):
		return
	#创建 F:\\data\\stock\\ 目录
	os.mkdir(__filepath)


#爬虫抓取网页函数
def getHtml(url):
	html = urllib.request.urlopen(url).read()
	html = html.decode('gbk')
	return html


#获取所有的股票编号，正则表达式带（）时，返回值只包含括号里内容，即股票编号数组
def getStackCode(html):
	print('enter getAllStockCode()')
	s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
	pat = re.compile(s)
	code = pat.findall(html)
	return code


#获取所有以6开头的股票代码的集合 600001,600002等等	
def getAllStockCode():
	print('enter getAllStockCode()')
	#东方财富网股票网址
	Url = 'http://quote.eastmoney.com/stocklist.html'
	#进行抓取
	code = getStackCode(getHtml(Url))	
	#获取所有以6开头的股票代码的集合
	for item in code:
		print(item)
		if item[0]=='6':
			__CodeList.append(item)


#下载所有的6开头的股票，数据一直到今天的日期	
def getAllStockExcels():
	print('enter getAllStockExcels():')
	createDirForStockExcels() #定义数据文件保存路径
	#将网页上文件下载并保存到本地csv文件，注意日期
	todayTime = time.strftime("%Y%m%d",(time.localtime()));
	getAllStockCode()
	for code in __CodeList:
		print('正在获取股票%s数据'%code)
		url = 'http://quotes.money.163.com/service/chddata.html?code=0'+code+\
			'&end='+ todayTime + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
		urllib.request.urlretrieve(url, __filepath+code+'.csv')

#获取所有以6开头的股票代码的集合 600001,600002等等,写死遍历获得	
#2506 这个有问题 要跳过去
def getAllStockCodeNew():
	for i in range(2506,3999):
		item = 600000+i
		__CodeList.append(item)			

		
#下载所有的6开头的股票，数据一直到今天的日期， 写死的数组获取，部分不存在，所以要考虑异常
def getAllStockExcelsNew():
	print('enter getAllStockExcels():')
	#createDirForStockExcels() #定义数据文件保存路径
	useExistDirForStockExcels() 
	#将网页上文件下载并保存到本地csv文件，注意日期
	todayTime = time.strftime("%Y%m%d",(time.localtime()));
	getAllStockCodeNew()
	for code in __CodeList:
		print('正在获取股票%s数据'%code)
		url = 'http://quotes.money.163.com/service/chddata.html?code=0'+str(code)+\
			'&end='+ todayTime + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
		urllib.request.urlretrieve(url, __filepath+str(code)+'.csv')

#下载指定的股票，数据一直到今天的日期	
def getSpecStockExcels():
	createDirForStockExcels() #定义数据文件保存路径
	CodeListTemp = ['600280','603169']
	#将网页上文件下载并保存到本地csv文件，注意日期
	todayTime = time.strftime("%Y%m%d",(time.localtime()));
	for code in CodeListTemp:
		print('正在获取股票%s数据'%code)
		url = 'http://quotes.money.163.com/service/chddata.html?code=0'+code+\
			'&end='+ todayTime + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
		urllib.request.urlretrieve(url, __filepath+code+'.csv')



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

	
if __name__ == '__main__':
	print('下载excels')
	#getSpecStockExcels()
	getAllStockExcelsNew()
	
	#print('存储信息到数据库')
	#saveDataFromExcels()
	
	print('over')
	
	
	
	
	
