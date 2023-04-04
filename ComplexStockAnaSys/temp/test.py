# -*- coding: UTF-8 -*-

#!/usr/bin/python3
 
import pymysql
import os

__CodeList = []
 
# �����ݿ�����
db = pymysql.connect(host='localhost', user='root', password= 'Test_123', charset='utf8') 
# ʹ��cursor()������ȡ�����α� 
cursor = db.cursor()
fileName = '600280'
__filepath = 'D:\LearnFile\language\python\project\gupiao\result.txt'

def createFile():
	if  os.path.exists(__filepath):
		os.remove(__filepath)
	file = open('result.txt','w+')
	file.close()

#��ȡ������6��ͷ�Ĺ�Ʊ����ļ��� 600001,600002�ȵ�,д���������
#2506 ��������� Ҫ����ȥ
def getAllStockCodeNew():
	for i in range(0,2500):
		if (i == 2506):
			continue
		item = 600000+i
		__CodeList.append(item)	

		
# SQL ��ѯ���
sqlSentence2 = "use stockDataBase;"
cursor.execute(sqlSentence2)
#getAllStockCodeNew()
createFile()

currPrice = 0.0
highPrice = 0.0
lowPrice = 0.0

for code in __CodeList:
	#�ҳ���ǰ�۸�
	sql = "SELECT * FROM stock_%s" %code + " order by daydate Desc limit 1;"
	#print(sql)
	try:
		# ִ��SQL���
		cursor.execute(sql)
		# ��ȡ���м�¼�б�
		results = cursor.fetchall()
		for row in results:
			currPrice = row[3]
			# ��ӡ���
			#print ("currPrice=%s" % currPrice)
	except:
		print ("Error: unable to fetch data")
		continue

	#��ǰ�۸�Ϊ0�����л���ͣ��	
	if (currPrice == 0):
		continue
	
	#�ҳ���ͼ۸�
	sql = "SELECT * FROM stock_%s" %code + " WHERE TO_DAYS(NOW()) - TO_DAYS(daydate) <= 1100 and closingprice>0 order by closingprice Asc limit 1;  "
	#print(sql)
	try:
		# ִ��SQL���
		cursor.execute(sql)
		# ��ȡ���м�¼�б�
		results = cursor.fetchall()
		for row in results:
			lowPrice = row[3]
			# ��ӡ���
			#print ("lowPrice=%s" % lowPrice)
	except:
		print ("Error: unable to fetch data")
		continue

	#�ҳ���߼۸�
	sql = "SELECT * FROM stock_%s" %code + " WHERE TO_DAYS(NOW()) - TO_DAYS(daydate) <= 1100 order by closingprice Desc limit 1; "
	#print(sql)
	try:
		# ִ��SQL���
		cursor.execute(sql)
		# ��ȡ���м�¼�б�
		results = cursor.fetchall()
		for row in results:
			highPrice = row[3]
			# ��ӡ���
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

		
# �ر����ݿ�����
db.close()
	
