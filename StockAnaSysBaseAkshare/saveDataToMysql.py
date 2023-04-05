#!/usr/bin/python
# -*- coding:utf-8 -*-

import pymysql
import akshare as ak
import time

sqlCrtDateBase = "create database if not exists stockDataBase;"
sqlEntryDateBase = "use stockDataBase;"
# sqlDropTable = "drop table if exists stock_%s;"
# sqlCrtTableName = "create table stock_%s" 
# sqlCrtTableCols = "(stockcode VARCHAR(10), name VARCHAR(10), daydate date, \
#                 closingprice float,    highestprice    float, lowestprice float, openingprice float)"

def saveDataFromAkshareRsp():
    #建立本地数据库连接(需要先开启数据库服务)
    db = pymysql.connect(host='localhost', user='root', password= 'Test_123', charset='utf8')  #现在必须指定参数
    cursor = db.cursor()
    cursor.execute(sqlCrtDateBase)#选择使用当前数据库
    cursor.execute(sqlEntryDateBase)

    _todayTime = time.strftime("%Y%m%d",(time.localtime()));

    stock_info_sh_code_name_df = ak.stock_info_sh_name_code()
    for rowTuplesCode in stock_info_sh_code_name_df.itertuples():
        stockCode = getattr(rowTuplesCode, "公司代码")
        stockName = getattr(rowTuplesCode, "公司简称")

        sqlSentenceDel = "drop table if exists stock_%s;" % stockCode
        cursor.execute(sqlSentenceDel)

        #创建数据表，如果数据表已经存在，会跳过继续执行下面的步骤print('创建数据表stock_%s'% fileName[0:6])
        sqlSentence3 = "create table stock_%s" % stockCode + "(stockcode VARCHAR(10), name VARCHAR(10), daydate date, \
                closingprice float, openingprice float,    highestprice    float, lowestprice float)"
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
                sqlSentence4 = "insert into stock_%s" % stockCode + "(stockcode, name, daydate, closingprice, openingprice, highestprice, lowestprice)\
                values ('%s','%s','%s',%s,%s,%s,%s)" %(stockCode, stockName, date, closingprice, openingprice, lowestprice, highestprice)
                #获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值
                sqlSentence4 = sqlSentence4.replace('nan','null').replace('None','null').replace('none','null') 
                cursor.execute(sqlSentence4)
            except:
                #如果以上插入过程出错，跳过这条数据记录，继续往下进行
                print(stockCode ,' insert failure')

        print(stockCode, "_", stockName, " the ending")

	#关闭游标，提交，关闭数据库连接
    cursor.close()
    db.commit()
    db.close()
    print("all stock the ending......")

saveDataFromAkshareRsp()
