from django.db import models


# Create your models here.

class Stock_all(models.Model):
    state_dt = models.CharField(max_length=45)
    stock_code = models.CharField(max_length=45)
    open = models.DecimalField(max_digits=20, decimal_places=2)
    close = models.DecimalField(max_digits=20, decimal_places=2)
    high = models.DecimalField(max_digits=20, decimal_places=2)
    low = models.DecimalField(max_digits=20, decimal_places=2)
    vol = models.IntegerField()
    amount = models.DecimalField(max_digits=30, decimal_places=2)
    pre_close = models.DecimalField(max_digits=20, decimal_places=2)
    amt_change = models.DecimalField(max_digits=20, decimal_places=2)
    pct_change = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        db_table = "stock_all"
        unique_together = ('state_dt', 'stock_code',)

class Stock_basic3(models.Model):
    ts_code = models.CharField(max_length=45)
    symbol = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    area = models.CharField(max_length=45)
    industry = models.CharField(max_length=45)
    fullname = models.CharField(max_length=45)
    enname = models.CharField(max_length=145)
    market = models.CharField(max_length=45)
    exchange = models.CharField(max_length=45)
    curr_type = models.CharField(max_length=45)
    list_status = models.CharField(max_length=45)
    list_date = models.CharField(max_length=45)
    delist_date = models.CharField(max_length=45,null=True)
    is_hs = models.CharField(max_length=45)

    class Meta:
        db_table = "stock_basic3"
        unique_together = ('ts_code', 'symbol',)

class Daily_basic(models.Model):
    ts_code = models.CharField(max_length=45)
    trade_date = models.CharField(max_length=45)
    close = models.DecimalField(max_digits=20, decimal_places=2)
    turnover_rate = models.DecimalField(max_digits=20, decimal_places=4)
    turnover_rate_f = models.DecimalField(max_digits=20, decimal_places=4)
    volume_ratio = models.DecimalField(max_digits=20, decimal_places=2)
    pe = models.DecimalField(max_digits=20, decimal_places=4)
    pe_ttm = models.DecimalField(max_digits=20, decimal_places=4)
    pb = models.DecimalField(max_digits=20, decimal_places=4)
    ps = models.DecimalField(max_digits=20, decimal_places=4)
    ps_ttm = models.DecimalField(max_digits=20, decimal_places=4)
    total_share = models.DecimalField(max_digits=20, decimal_places=4)
    float_share = models.DecimalField(max_digits=20, decimal_places=4)
    free_share = models.DecimalField(max_digits=20, decimal_places=4)
    total_mv = models.DecimalField(max_digits=20, decimal_places=4)
    circ_mv = models.DecimalField(max_digits=20, decimal_places=4)

    class Meta:
        db_table = "daily_basic"
        unique_together = ('ts_code', 'trade_date',)