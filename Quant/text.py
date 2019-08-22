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
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = '20190101'
    time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
    end_dt = time_temp.strftime('%Y%m%d')

    # 建立数据库连接,剔除已入库的部分
    db = psycopg2.connect(database="tushare", user="tushare", password="*", host="192.168.1.139", port="5432")
    cursor = db.cursor()

    '''
    # 设定需要获取数据的股票池
    #1.所有list
    sql_search = "select ts_code from stock_basic3;"
    cursor.execute(sql_search)
    stock_pool1 = pandas.DataFrame(cursor.fetchall())[0].tolist()
    print(len(stock_pool1))
    #2、查看已有list
    sql_search = "select stock_code from stock_all;"
    cursor.execute(sql_search)
    stock_pool2 = pandas.DataFrame(cursor.fetchall())[0].tolist()
    set0 = set(stock_pool2)
    stock_pool2 = list(set0)
    print(len(stock_pool2))
    #3、大的减小的
    set1 = set(stock_pool1)
    set2 = set(stock_pool2)
    set3 = set1.difference(set2)
    stock_pool = list(set3)
    print(stock_pool)
    '''
    '''
    #sql_search = "select * from stock_all where state_dt = '2019-08-16';"
    sql_search = "select  state_dt,sum(amount) from stock_all group by state_dt;"
    cursor.execute(sql_search)
    stock_pool = pd.DataFrame(cursor)
    #stock_pool.columns = ['id','state_dt','stock_code','open','amount','amt_change','close',
                                                     #'high','low','pct_change','pre_close','vol']
    print(stock_pool)
    #stock_pool.plot()
    #plt.show()
    plt.plot(stock_pool[0],stock_pool[1].values,lw=1.5,label="amount",color="blue")
    plt.show()
    
    df = pro.daily_basic(ts_code='300787.SZ', trade_date='',
                    fields='ts_code,trade_date,close,turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm,pb,ps,'
                           'ps_ttm,total_share,float_share,free_share,total_mv,circ_mv')
    print(df)
    '''
    sql_search = "select max(id) from daily_basic;"
    df = cursor.execute(sql_search)
    max_id = pd.DataFrame(cursor.fetchall())[0].tolist()[0]
    for i in range(max_id):
        try:
            sql_search = "select trade_date from daily_basic where id = '%d';" % i
            df = cursor.execute(sql_search)
            trade_date = pd.DataFrame(cursor.fetchall())[0].tolist()[0]
        except Exception as aa:
            print('No ID Code: ' + str(i))
            continue
        #更新日期数据
        state_dt = (datetime.datetime.strptime(trade_date, "%Y%m%d")).strftime('%Y-%m-%d')
        sql_search = "update daily_basic set trade_date = '%s' where id = '%d';" %(state_dt, i)
        cursor.execute(sql_search)
        db.commit()
        print(str(i) + ' of ' + str(max_id))
    cursor.close()
    db.close()


