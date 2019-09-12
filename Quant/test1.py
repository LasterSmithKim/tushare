import datetime
import tushare as ts
import psycopg2
import pandas as pd
import numpy as np
import csv
pd.set_option("display.max_columns",500)
import matplotlib.pyplot as plt
from bokeh.plotting import figure,show,output_file


#select * from (select * from daily_basic where trade_date = '2019-09-02') as daily left join (select * from stock_basic3) as basic on daily.ts_code=basic.ts_code
#select daily_basic_basic.industry,sum(total_mv) from (select * from (select * from daily_basic where trade_date = '2019-09-02') as daily left join (select * from stock_basic3) as basic on daily.ts_code=basic.ts_code) as daily_basic_basic group by industry;
#select daily_basic_basic.area,sum(total_mv)/10000 as 亿元 from (select * from (select * from daily_basic where trade_date = '2019-09-02') as daily left join (select * from stock_basic3) as basic on daily.ts_code=basic.ts_code) as daily_basic_basic group by area order by 亿元 desc;
#select daily_basic_basic.market,sum(total_mv)/10000 as 亿元 from (select * from (select * from daily_basic where trade_date = '2019-09-02') as daily left join (select * from stock_basic3) as basic on daily.ts_code=basic.ts_code) as daily_basic_basic group by market order by 亿元 desc;
#select daily_basic_basic.industry,sum(total_mv)/10000 as 亿元 from (select * from (select * from daily_basic where trade_date = '2019-09-02') as daily left join (select * from stock_basic3) as basic on daily.ts_code=basic.ts_code) as daily_basic_basic group by industry order by 亿元 desc;



if __name__ == '__main__':
    # 建立数据库连接,剔除已入库的部分
    db = psycopg2.connect(database="tushare", user="tushare", password="*", host="192.168.43.226", port="5432")
    cursor = db.cursor()
    sql_search = "select max(trade_date) from daily_basic;"
    cursor.execute(sql_search)
    maxdate =cursor.fetchall()[0][0]
    print(rows)
    cursor.close()
    db.close()
