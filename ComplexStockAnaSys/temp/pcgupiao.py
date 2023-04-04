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
# ,encoding='utf-8'


#生成指定目录,如果有就先删除再创建
def createDirForStockExcels():
	#判单某个目录是否存在
	path = 'F:\\data\\stock\\'
	if os.path.isdir(path):
		#os.rmdir(path) --只能删除空目录
		shutil.rmtree(path)

	#创建 F:\\data\\stock\\ 目录
	os.mkdir(path)
	return path


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


#下载所有的6开头的股票，数据一直到今天的日期	
def getAllStockExcels():
	filepath = createDirForStockExcels() #定义数据文件保存路径
	#将网页上文件下载并保存到本地csv文件，注意日期
	todayTime = time.strftime("%Y%m%d",(time.localtime()));
	CodeList = getAllStockCode()
	for code in CodeList:
		print('正在获取股票%s数据'%code)
		url = 'http://quotes.money.163.com/service/chddata.html?code=0'+code+\
			'&end='+ todayTime + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
		urllib.request.urlretrieve(url, filepath+code+'.csv')

#下载指定的股票，数据一直到今天的日期	
def getSpecStockExcels():
	filepath = createDirForStockExcels() #定义数据文件保存路径
	CodeListTemp = ['600280','603169']
	#将网页上文件下载并保存到本地csv文件，注意日期
	todayTime = time.strftime("%Y%m%d",(time.localtime()));
	for code in CodeListTemp:
		print('正在获取股票%s数据'%code)
		url = 'http://quotes.money.163.com/service/chddata.html?code=0'+code+\
			'&end='+ todayTime + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
		urllib.request.urlretrieve(url, filepath+code+'.csv')
	
	
if __name__ == '__main__':
	print('下载excels')
	getAllStockExcels()
	
	
	
	
