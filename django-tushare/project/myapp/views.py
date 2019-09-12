from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
import pandas as pd
import numpy as np
import tushare as ts

# Create your views here.

def hello(request):

    # 设置tushare pro的token并获取连接
    ts.set_token('c4329c2966bd199671bc3708a6906cbb364bd920588b2a28ccf14f55')
    pro = ts.pro_api()
    # 建立数据库连接,剔除已入库的部分
    db = psycopg2.connect(database="tushare", user="tushare", password="smith123", host="192.168.43.226", port="5432")
    cursor = db.cursor()
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    sql_search = "select trade_date , sum(total_mv)/100000000 from daily_basic group by trade_date;"
    cursor.execute(sql_search)
    df = pd.DataFrame(cursor.fetchall())
    cursor.close()
    db.close()

    data = ''
    c_len = df.shape[0]
    for j in range(c_len):
        resu0 = list(df.loc[c_len - 1 - j])
        resu = []

        for k in range(len(resu0)):
            if str(resu0[k]) == 'nan':
                resu.append(-1)
            else:
                resu.append(resu0[k])
        if (j != (c_len - 1)):
            data = data + (
                        str("\"") + str(resu[0]) + str(",\"") + str(" + ") + str(resu[1]) + str(" + \"\\n\" +") + str(
                    "\n"))
        else:
            data = data + (str("\"") + str(resu[0]) + str(",\"") + str(" + ") + str(resu[1]) + str(" + \"\\n\""))

    return render(request, "hello.html", {"date": data})

def market(request):

    # 建立数据库连接,剔除已入库的部分
    db = psycopg2.connect(database="tushare", user="tushare", password="smith123", host="192.168.43.226", port="5432")
    cursor = db.cursor()
    sql_search = "select max(trade_date) from daily_basic;"
    cursor.execute(sql_search)
    maxdate =cursor.fetchall()[0][0]
    sql_search = "select daily_basic_basic.market,sum(total_mv)/10000 as 亿元 from (select * from (select * from daily_basic where trade_date = '%s') as daily left join (select * from stock_basic3) as basic on daily.ts_code=basic.ts_code) as daily_basic_basic group by market order by 亿元 desc;" % str(maxdate)
    cursor.execute(sql_search)
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return render(request, "market.html", {"market_rows": rows})

def area(request):

    # 建立数据库连接,剔除已入库的部分
    db = psycopg2.connect(database="tushare", user="tushare", password="smith123", host="192.168.43.226", port="5432")
    cursor = db.cursor()
    sql_search = "select max(trade_date) from daily_basic;"
    cursor.execute(sql_search)
    maxdate =cursor.fetchall()[0][0]
    sql_search = "select daily_basic_basic.area,sum(total_mv)/10000 as 亿元 from (select * from (select * from daily_basic where trade_date = '%s') as daily left join (select * from stock_basic3) as basic on daily.ts_code=basic.ts_code) as daily_basic_basic group by area order by 亿元 desc;" % str(maxdate)
    cursor.execute(sql_search)
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return render(request, "area.html", {"area_rows": rows})

def industry(request):
    # 建立数据库连接,剔除已入库的部分
    db = psycopg2.connect(database="tushare", user="tushare", password="smith123", host="192.168.43.226", port="5432")
    cursor = db.cursor()
    sql_search = "select max(trade_date) from daily_basic;"
    cursor.execute(sql_search)
    maxdate = cursor.fetchall()[0][0]
    sql_search = "select daily_basic_basic.industry,sum(total_mv)/10000 as 亿元 from (select * from (select * from daily_basic where trade_date = '%s') as daily left join (select * from stock_basic3) as basic on daily.ts_code=basic.ts_code) as daily_basic_basic group by industry order by 亿元 desc;" % str(
        maxdate)
    cursor.execute(sql_search)
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return render(request, "industry.html", {"industry_rows": rows})