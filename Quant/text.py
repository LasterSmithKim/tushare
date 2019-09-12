import datetime
import tushare as ts
import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option("display.max_columns",500)

if __name__ == '__main__':

    # 设置tushare pro的token并获取连接
    ts.set_token('*')
    pro = ts.pro_api()
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。select max(state_dt) from stock_all;

    # 建立数据库连接,剔除已入库的部分
    db = psycopg2.connect(database="tushare", user="tushare", password="*", host="172.20.10.7", port="5432")
    cursor = db.cursor()
    '''
    sql_search = "select max(state_dt) from stock_all;"
    cursor.execute(sql_search)
    df = pd.DataFrame(cursor.fetchall())[0].tolist()[0]
    df_datatime = (datetime.datetime.strptime(df, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    print(df_datatime)
    '''
    sql_search = "select max(state_dt) from stock_all;"
    cursor.execute(sql_search)
    df = pd.DataFrame(cursor.fetchall())[0].tolist()[0]
    start_dt = (datetime.datetime.strptime(df, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y%m%d')

    end_date = datetime.datetime.now().strftime('%Y%m%d')
    data = pro.query('trade_cal', start_date=start_dt, end_date=end_date)
    date_pool = list(data.loc[data.is_open == 1].cal_date)
    print(date_pool)

    max_data = datetime.datetime.strptime(df, '%Y-%m-%d').strftime('%Y%m%d')
    if (max_data != end_date):
        pass
    else:
        print('当前已是最新数据，无需更新，但是也需要查看单日数据完整性。')

    cursor.close()
    db.close()

