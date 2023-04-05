#!/usr/bin/python
# -*- coding:utf-8 -*-

import pymysql

sqlCrtDateBase = "create database if not exists testBase;"
sqlEntryDateBase = "use testBase;"
sqlDropTable = "drop table if exists stock600015;"

db = pymysql.connect(host='localhost', user='root', password= 'Test_123', charset='utf8')  #现在必须指定参数
cursor = db.cursor()
cursor.execute(sqlCrtDateBase)#选择使用当前数据库
cursor.execute(sqlEntryDateBase)
cursor.execute(sqlDropTable)

sqlSentence3 = "create table stock600015 (stockcode VARCHAR(10), name VARCHAR(10), daydate date, \
        closingprice float,    highestprice    float, lowestprice float, openingprice float)"
cursor.execute(sqlSentence3)

sqlSentence4 = "insert into stock600015(stockcode, name, daydate, closingprice, highestprice, lowestprice, openingprice)\
            values ('600015','中国茅台','20230405',1800,1900,1700.2,1800)"
cursor.execute(sqlSentence4)

#关闭游标，提交，关闭数据库连接
cursor.close()
db.commit()
db.close()