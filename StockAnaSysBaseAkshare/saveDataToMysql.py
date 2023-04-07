#!/usr/bin/python
# -*- coding:utf-8 -*-

import pymysql
import akshare as ak
import time

#stockDataBase
sqlCrtDateBase = "create database if not exists stockDb;"
sqlEntryDateBase = "use stockDb;"
# sqlDropTable = "drop table if exists stock_%s;"
# sqlCrtTableName = "create table stock_%s" 
# sqlCrtTableCols = "(stockcode VARCHAR(10), name VARCHAR(10), daydate date, \
#                 closingprice float,    highestprice    float, lowestprice float, openingprice float)"

def saveSHDataFromAkshareRsp():
    #建立本地数据库连接(需要先开启数据库服务)
    db = pymysql.connect(host='localhost', user='root', password= 'Test_123', charset='utf8')  #现在必须指定参数
    cursor = db.cursor()
    cursor.execute(sqlCrtDateBase)#选择使用当前数据库
    cursor.execute(sqlEntryDateBase)
    count = 0

    _todayTime = time.strftime("%Y%m%d",(time.localtime()));

    stock_info_sh_code_name_df = ak.stock_info_sh_name_code()
    for rowTuplesCode in stock_info_sh_code_name_df.itertuples():
        count = count+1
        if (0 == count % 500):
            time.sleep(3)  #每下载500条数据，休眠3s
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
    print("all shanghai stock the ending......")

def saveSzDataFromAkshareRsp():
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
        if (stockCode>"300000"): #创业板的先不入库，节省时间
            print("创业板不入库")
            break

        # if (stockCode<"002212"): #有时候会被禁掉，从之前断掉的地方开始，第一次跑的时候，这边要注释掉
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
    print("all shanghai stock the ending......")

if __name__ == "__main__":
    print("保存沪市股票开始......")
    saveSHDataFromAkshareRsp()
    print("保存深市股票开始......")
    saveSzDataFromAkshareRsp()

