import datetime
import tushare as ts
import psycopg2
import pandas as pd
pd.set_option("display.max_columns",500)

if __name__ == '__main__':

    # 设置tushare pro的token并获取连接
    ts.set_token('*')
    pro = ts.pro_api()
    # 建立数据库连接,剔除已入库的部分
    db = psycopg2.connect(database="tushare", user="tushare", password="*", host="192.168.1.139", port="5432")
    cursor = db.cursor()

    #上市状态： L上市 D退市 P暂停上市
    data = pro.query('stock_basic', exchange='', list_status='L', fields=
    'ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
    data = pd.DataFrame(data)
    c_len = data.shape[0]
    print(c_len)
    print(data)

    for j in range(c_len):
        resu0 = list(data.loc[c_len - 1 - j])
        resu = []
        for k in range(len(resu0)):
            if str(resu0[k]) == 'nan':
                resu.append(-1)
            else:
                resu.append(resu0[k])
        #检查ename字段中是否包含 单引号 ？
        resu6 = str(resu[6]).replace('\'','\'\'')

        try:
            sql_insert = "INSERT INTO stock_basic3(ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (str(resu[0]),str(resu[1]),str(resu[2]),str(resu[3]),str(resu[4]),str(resu[5]),resu6,str(resu[7]),str(resu[8]),str(resu[9]),str(resu[10]),str(resu[11]),str(resu[12]),str(resu[13]))
            cursor.execute(sql_insert)
            db.commit()
        except Exception as err:
            continue

    cursor.close()
    db.close()
    print('All Finished!')
