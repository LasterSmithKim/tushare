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
    db = psycopg2.connect(database="tushare", user="tushare", password="8", host="192.168.1.139", port="5432")
    cursor = db.cursor()

    todate = datetime.datetime.now().strftime('%Y%m%d')
    data = pro.query('trade_cal', start_date=start_dt, end_date=todate)
    date_pool = list(data.loc[data.is_open == 1].cal_date)
    print(date_pool)



    '''
    # 设定需要获取数据的股票池
    sql_search = "select ts_code from stock_basic3;"
    cursor.execute(sql_search)
    stock_pool1 = pd.DataFrame(cursor.fetchall())[0].tolist()
    # print(len(stock_pool1))
    # 2、查看已有list
    sql_search = "select ts_code from daily_basic;"
    cursor.execute(sql_search)
    stock_pool2 = pd.DataFrame(cursor.fetchall())[0].tolist()
    set0 = set(stock_pool2)
    stock_pool2 = list(set0)
    # print(len(stock_pool2))
    # 3、大的减小的
    set1 = set(stock_pool1)
    set2 = set(stock_pool2)
    set3 = set1.difference(set2)
    stock_pool = list(set3)
    # print(stock_pool)
    '''
    total = len(date_pool)
    # 循环获取单个股票的日线行情
    for i in range(len(date_pool)):
        try:
            #df = pro.daily_basic(ts_code=stock_pool[i], trade_date='',
                         #fields='ts_code,trade_date,close,turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm,pb,ps,'
                                #'ps_ttm,total_share,float_share,free_share,total_mv,circ_mv')
            df = pro.daily_basic(ts_code='', trade_date=date_pool[i],
                                 fields='ts_code,trade_date,close,turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm,pb,ps,'
                                        'ps_ttm,total_share,float_share,free_share,total_mv,circ_mv')
            # 打印进度
            print('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(date_pool[i]))
            c_len = df.shape[0]
        except Exception as aa:
            print(aa)
            print('No DATA Code: ' + str(i))
            continue
        for j in range(c_len):
            resu0 = list(df.loc[c_len - 1 - j])
            resu = []
            for k in range(len(resu0)):
                if str(resu0[k]) == 'nan':
                    resu.append(-1)
                else:
                    resu.append(resu0[k])
            state_dt = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
            try:
                sql_insert = "INSERT INTO daily_basic(ts_code,trade_date,close,turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm,pb,ps,ps_ttm,total_share,float_share,free_share,total_mv,circ_mv) VALUES ('%s','%s','%.2f','%.4f','%.4f','%.2f','%.4f','%.4f','%.4f','%.4f','%.4f','%.4f','%.4f','%.4f','%.4f','%.4f')" \
                             % (str(resu[0]),state_dt,float(resu[2]),float(resu[3]),float(resu[4]),float(resu[5]),float(resu[6]),float(resu[7]),float(resu[8]),float(resu[9]),float(resu[10]),float(resu[11]),float(resu[12]),float(resu[13]),float(resu[14]),float(resu[15]))
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                print(err)
                continue

    cursor.close()

    db.close()
    print('All Finished!')
