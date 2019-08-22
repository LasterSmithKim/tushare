import datetime
import tushare as ts
import psycopg2
import pandas as pd
pd.set_option("display.max_columns",500)

if __name__ == '__main__':

    # 设置tushare pro的token并获取连接
    ts.set_token('*')
    pro = ts.pro_api()
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = '20190822'
    time_temp = datetime.datetime.now()
    #time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
    end_dt = time_temp.strftime('%Y%m%d')
    # 建立数据库连接,剔除已入库的部分
    db = psycopg2.connect(database="tushare", user="tushare", password="*", host="192.168.1.139", port="5432")
    cursor = db.cursor()
    # 设定需要获取数据的股票池
    sql_search = "select ts_code from stock_basic3;"
    cursor.execute(sql_search)

    todate = datetime.datetime.now().strftime('%Y%m%d')
    data = pro.query('trade_cal', start_date=start_dt, end_date=todate)
    date_pool = list(data.loc[data.is_open == 1].cal_date)
    print(date_pool)

    #df = pro.daily(ts_code='603912.SH', start_date=start_dt, end_date=end_dt)
    #ts_code trade_date   open  high   low  close  pre_close  change  pct_chg   vol     amount
    #df = pro.daily(trade_date='20190819')
    #ts_code trade_date   open   high    low  close  pre_close  change pct_chg  vol      amount
    #print(df)



    '''
    #stock_pool = pandas.DataFrame(cursor.fetchall())[0].tolist()
    #stock_pool = ['603912.SH','300666.SZ','300618.SZ','002049.SZ','300672.SZ']
    #1.所有list
    sql_search = "select ts_code from stock_basic3;"
    cursor.execute(sql_search)
    stock_pool1 = pandas.DataFrame(cursor.fetchall())[0].tolist()
    
    # 循环获取单个股票的日线行情
    '''
    total = len(date_pool)
    for i in range(len(date_pool)):
        try:
            #df = pro.daily(ts_code=stock_pool1[i], start_date=start_dt, end_date=end_dt)
            df = pro.daily(trade_date=date_pool[i])
            # 打印进度
            print('Seq: ' + str(i+1) + ' of ' + str(total) + '   Code: ' + str(date_pool[i]))
            c_len = df.shape[0]
        except Exception as aa:
            print(aa)
            print('No DATA Code: ' + str(i))
            continue
        for j in range(c_len):
            resu0 = list(df.loc[c_len-1-j])
            resu = []
            for k in range(len(resu0)):
                if str(resu0[k]) == 'nan':
                    resu.append(-1)
                else:
                    resu.append(resu0[k])
            state_dt = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
            #for m in range(len(resu)):
                #print(resu[m])
            try:
                sql_insert = "INSERT INTO stock_all(state_dt,stock_code,open,close,high,low,vol,amount,pre_close," \
                             "amt_change,pct_change) VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f'," \
                             "'%.2f','%.2f','%.2f')" % \
                             (state_dt,str(resu[0]),float(resu[2]),float(resu[5]),float(resu[3]),float(resu[4]),
                              float(resu[9]),float(resu[10]),float(resu[6]),float(resu[7]),float(resu[8]))
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                continue
    cursor.close()
    db.close()

    print('All Finished!')
