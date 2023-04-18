#!/usr/bin/python
# -*- coding:utf-8 -*-

import akshare as ak

'''
stock_df = ak.stock_zh_a_hist(symbol='600519', period="daily", start_date='20220101', end_date='20220125', adjust="qfq")
'''
#print(stock_df)
'''
       日期       开盘       收盘       最高       最低  ...           成交额    振幅   涨跌幅    涨跌额   换手率
0   2022-01-04  2011.42  2007.65  2025.37  1970.42  ...  6.913653e+09  2.74  0.06   1.23  0.27
1   2022-01-05  2001.42  1980.42  2021.42  1974.42  ...  5.774992e+09  2.34 -1.36 -27.23  0.23
2   2022-01-06  1978.43  1938.64  1992.42  1894.93  ...  1.022693e+10  4.92 -2.11 -41.78  0.41
3   2022-01-07  1931.42  1898.42  1945.30  1895.74  ...  5.831695e+09  2.56 -2.07 -40.22  0.24
4   2022-01-10  1884.43  1922.42  1933.42  1873.97  ...  5.792738e+09  3.13  1.26  24.00  0.24
5   2022-01-11  1904.42  1896.97  1921.42  1887.59  ...  4.332181e+09  1.76 -1.32 -25.45  0.18
6   2022-01-12  1904.42  1923.42  1935.22  1904.42  ...  5.384360e+09  1.62  1.39  26.45  0.22
7   2022-01-13  1921.24  1833.81  1924.41  1821.98  ...  1.078172e+10  5.33 -4.66 -89.61  0.45
12  2022-01-20  1872.42  1925.94  1936.41  1872.42  ...  6.665295e+09  3.42  3.08  57.52  0.27
13  2022-01-21  1916.42  1941.41  1949.91  1907.43  ...  6.091428e+09  2.21  0.80  15.47  0.25
14  2022-01-24  1911.42  1906.62  1940.42  1887.86  ...  4.685442e+09  2.71 -1.79 -34.79  0.19
15  2022-01-25  1899.42  1899.42  1922.42  1887.42  ...  4.971078e+09  1.84 -0.38  -7.20  0.20
'''

#print(type(stock_df))   #<class 'pandas.core.frame.DataFrame'>


#print(stock_df.axes) 
'''
[RangeIndex(start=0, stop=16, step=1), Index(['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'], dtype='object')]
'''

# for row in stock_df:
#     print(type(row))
#     print(row)

'''
for row in stock_df.iterrows():
    print(type(row))
    print(row[0])
    print(type(row[1])) #pandas.core.series.Series
    print(row[1])
'''

'''
for rowTuple in stock_df.itertuples():
    print(type(rowTuple))
    print(rowTuple)
    print(getattr(rowTuple, '日期'))
    print(getattr(rowTuple, '开盘'))
'''

'''
<class 'pandas.core.frame.Pandas'>
Pandas(Index=0, 日期='2022-01-04', 开盘=2011.42, 收盘=2007.65, 最高=2025.37, 最低=1970.42, 成交量=33843, 成交额=6913653248.0,  振幅=2.74, 涨跌幅=0.06, 涨跌额=1.23, 换手率=0.27)
'''

"""
stock_info_sh_code_name_df = ak.stock_info_sh_name_code()
print(stock_info_sh_code_name_df)
"""


"""
        公司代码  公司简称      代码    简称        上市日期
0     600000  浦发银行  600000  浦发银行  1999-11-10
1     600004  白云机场  600004  白云机场  2003-04-28
2     600006  东风汽车  600006  东风汽车  1999-07-27
"""
"""
for rowTuplesCode in stock_info_sh_code_name_df.itertuples():
    stockCode = getattr(rowTuplesCode, "公司代码")
    stockName = getattr(rowTuplesCode, "公司简称")
    print(stockCode)
    print(stockName)
    break
"""


"""
stock_info_sz_code_name_df = ak.stock_info_sz_name_code()
for rowTuplesCode in stock_info_sz_code_name_df.itertuples():
    print(rowTuplesCode)
    break
"""

"""
Pandas(Index=0, 板块='主板', A股代码='000001', A股简称='平安银行', A股上市日期='1991-04-03', A股总股本='19,405,918,198', A股流
通股本='19,405,534,450', 所属行业='J 金融业')
"""

"""
stock_dividents_cninfo_df = ak.stock_dividents_cninfo(symbol="002075")   #可以使用-分红的接口
for rowTuples in stock_dividents_cninfo_df.itertuples():
    print(rowTuples)
    print(getattr(rowTuples, "实施方案公告日期")) #2022-05-31
    break
"""


"""
Pandas(Index=0, 实施方案公告日期=datetime.date(2022, 5, 31), 送股比例=nan, 转增比例=nan, 派息比例=0.8, 股权登记日=datetime.date(2022, 6, 7), 除权日=datetime.date(2022, 6, 8), 派息日=datetime.date(2022, 6, 8), 股份到账日='', 实施方案分红说明='10派0.8元(含税)', 分红类型='年度分红', 报告时间='2021年报')
Pandas(Index=1, 实施方案公告日期=datetime.date(2021, 5, 11), 送股比例=nan, 转增比例=nan, 派息比例=1.0, 股权登记日=datetime.date(2021, 5, 17), 除权日=datetime.date(2021, 5, 18), 派息日=datetime.date(2021, 5, 18), 股份到账日='', 实施方案分红说明='10派1元( 含税)', 分红类型='年度分红', 报告时间='2020年报')
Pandas(Index=2, 实施方案公告日期=datetime.date(2020, 6, 5), 送股比例=nan, 转增比例=nan, 派息比例=1.002034, 股权登记日=datetime.date(2020, 6, 10), 除权日=datetime.date(2020, 6, 11), 派息日=datetime.date(2020, 6, 11), 股份到账日='', 实施方案分红说明='10派1.002034元(含税)', 分红类型='年度分红', 报告时间='2019年报')
Pandas(Index=3, 实施方案公告日期=datetime.date(2019, 4, 19), 送股比例=nan, 转增比例=nan, 派息比例=0.3, 股权登记日=datetime.date(2019, 4, 24), 除权日=datetime.date(2019, 4, 25), 派息日=datetime.date(2019, 4, 25), 股份到账日='', 实施方案分红说明='10派0.3元(含税)', 分红类型='年度分红', 报告时间='2018年报')
Pandas(Index=4, 实施方案公告日期=datetime.date(2018, 9, 4), 送股比例=nan, 转增比例=nan, 派息比例=0.3, 股权登记日=datetime.date(2018, 9, 7), 除权日=datetime.date(2018, 9, 10), 派息日=datetime.date(2018, 9, 10), 股份到账日='', 实施方案分红说明='10派0.3元（含税）', 分红类型='中期分红', 报告时间='2018半年报')
Pandas(Index=5, 实施方案公告日期=datetime.date(2015, 10, 9), 送股比例=nan, 转增比例=4.0, 派息比例=nan, 股权登记日=datetime.date(2015, 10, 15), 除权日=datetime.date(2015, 10, 16), 派息日=NaT, 股份到账日='2015-10-16', 实施方案分红说明='10转增4股', 分红类型='中期分红', 报告时间='2015半年报')
Pandas(Index=6, 实施方案公告日期=datetime.date(2007, 5, 30), 送股比例=3.0, 转增比例=7.0, 派息比例=0.4, 股权登记日=datetime.date(2007, 6, 5), 除权日=datetime.date(2007, 6, 6), 派息日=datetime.date(2007, 6, 6), 股份到账日='2007-06-06', 实施方案分红说明='10送3转增7股派0.4元（含税）', 分红类型='年度分红', 报告时间='2006年报')
"""

#stock_a_indicator_df = ak.stock_a_indicator_lg(symbol="002075")   #not has

"""
get_bond_bank_df = ak.get_bond_bank(page_num=1) #没啥用
print(get_bond_bank_df)
for rowTuples in get_bond_bank_df.itertuples():
    print(rowTuples)
    break

   firstIssueAmount isReg                                 regFileName regPrdtType          releaseTime projPhase
0                10     1      青岛全球财富中心开发建设有限公司关于发行2023年度第一期中期票据的注册报告         MTN  2023-04-14 19:48:28        20
1                 5     1        泰州华诚医学投资集团有限公司关于发行2023年度第一期中期票据的注册报告         MTN  2023-04-14 18:36:27        30

"""

"""
bond_zh_hs_spot_df = ak.bond_zh_hs_spot()
for rowTuples in bond_zh_hs_spot_df.itertuples():
    print(rowTuples)
    break
"""

bond_zh_hs_cov_spot_df = ak.bond_zh_hs_cov_spot()
print(bond_zh_hs_cov_spot_df)
for rowTuples in bond_zh_hs_cov_spot_df.itertuples():
    print(rowTuples)
    print(getattr(rowTuples, "symbol"))
    print(getattr(rowTuples, "code"))
    print(getattr(rowTuples, "name"))
    break