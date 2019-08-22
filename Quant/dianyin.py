import tushare as ts
import datetime


today = (datetime.datetime.today()+datetime.timedelta(days=-1)).strftime("%Y%m%d")
print(today)
pro = ts.pro_api('*')
df = pro.bo_daily(date='20191023')

print(df)