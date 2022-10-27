#!/usr/bin/.venv python3
import datetime
from peewee import *

database = SqliteDatabase('Test.db')


class UnknownField(object):

    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Company(BaseModel):
    _id = AutoField(column_name='id', unique=True)
    exchange = TextField(null=True)
    index = IntegerField(index=True, null=True)
    name = TextField(null=True)
    symbol = TextField(null=True)

    class Meta:
        table_name = 'company'
        database = database
        primary_key = CompositeKey('symbol', '_id')


class Fundamentals(BaseModel):
    _id = AutoField(primary_key=True)
    beta = FloatField(null=True)
    book_value_per_share = FloatField(column_name='bookValuePerShare', null=True)
    current_ratio = FloatField(column_name='currentRatio', null=True)
    div_growth_rate3_year = FloatField(column_name='divGrowthRate3Year', null=True)
    dividend_amount = FloatField(column_name='dividendAmount', null=True)
    dividend_date = TextField(column_name='dividendDate', null=True)
    dividend_pay_amount = FloatField(column_name='dividendPayAmount', null=True)
    dividend_pay_date = TextField(column_name='dividendPayDate', null=True)
    dividend_yield = FloatField(column_name='dividendYield', null=True)
    eps_change = FloatField(column_name='epsChange', null=True)
    eps_change_percent_ttm = FloatField(column_name='epsChangePercentTTM', null=True)
    eps_change_year = FloatField(column_name='epsChangeYear', null=True)
    eps_ttm = FloatField(column_name='epsTTM', null=True)
    gross_margin_mrq = FloatField(column_name='grossMarginMRQ', null=True)
    gross_margin_ttm = FloatField(column_name='grossMarginTTM', null=True)
    high52 = FloatField(null=True)
    index = IntegerField(index=True, null=True)
    interest_coverage = FloatField(column_name='interestCoverage', null=True)
    low52 = FloatField(null=True)
    lt_debt_to_equity = FloatField(column_name='ltDebtToEquity', null=True)
    market_cap = FloatField(column_name='marketCap', null=True)
    market_cap_float = FloatField(column_name='marketCapFloat', null=True)
    net_profit_margin_mrq = FloatField(column_name='netProfitMarginMRQ', null=True)
    net_profit_margin_ttm = FloatField(column_name='netProfitMarginTTM', null=True)
    operating_margin_mrq = FloatField(column_name='operatingMarginMRQ', null=True)
    operating_margin_ttm = FloatField(column_name='operatingMarginTTM', null=True)
    pb_ratio = FloatField(column_name='pbRatio', null=True)
    pcf_ratio = FloatField(column_name='pcfRatio', null=True)
    pe_ratio = FloatField(column_name='peRatio', null=True)
    peg_ratio = FloatField(column_name='pegRatio', null=True)
    pr_ratio = FloatField(column_name='prRatio', null=True)
    quick_ratio = FloatField(column_name='quickRatio', null=True)
    return_on_assets = FloatField(column_name='returnOnAssets', null=True)
    return_on_equity = FloatField(column_name='returnOnEquity', null=True)
    return_on_investment = FloatField(column_name='returnOnInvestment', null=True)
    rev_change_in = FloatField(column_name='revChangeIn', null=True)
    rev_change_ttm = FloatField(column_name='revChangeTTM', null=True)
    rev_change_year = FloatField(column_name='revChangeYear', null=True)
    shares_outstanding = FloatField(column_name='sharesOutstanding', null=True)
    short_int_day_to_cover = FloatField(column_name='shortIntDayToCover', null=True)
    short_int_to_float = FloatField(column_name='shortIntToFloat', null=True)
    symbol = TextField(null=True)
    total_debt_to_capital = FloatField(column_name='totalDebtToCapital', null=True)
    total_debt_to_equity = FloatField(column_name='totalDebtToEquity', null=True)
    vol10_day_avg = FloatField(column_name='vol10DayAvg', null=True)
    vol1_day_avg = FloatField(column_name='vol1DayAvg', null=True)
    vol3_month_avg = FloatField(column_name='vol3MonthAvg', null=True)

    class Meta:
        table_name = 'fundamentals'
        database = database


class QuoteData(BaseModel):
    _id = AutoField(primary_key=True)
    _52_wk_high = FloatField(column_name='_52WkHigh', null=True)
    _52_wk_low = FloatField(column_name='_52WkLow', null=True)
    ask_id = TextField(column_name='askId', null=True)
    ask_price = FloatField(column_name='askPrice', null=True)
    ask_size = IntegerField(column_name='askSize', null=True)
    asset_main_type = TextField(column_name='assetMainType', null=True)
    asset_sub_type = TextField(column_name='assetSubType', null=True)
    asset_type = TextField(column_name='assetType', null=True)
    bid_id = TextField(column_name='bidId', null=True)
    bid_price = FloatField(column_name='bidPrice', null=True)
    bid_size = IntegerField(column_name='bidSize', null=True)
    bid_tick = TextField(column_name='bidTick', null=True)
    close_price = FloatField(column_name='closePrice', null=True)
    cusip = TextField(null=True)
    date = DateField(null=True)
    delayed = IntegerField(null=True)
    description = TextField(null=True)
    digits = IntegerField(null=True)
    div_amount = FloatField(column_name='divAmount', null=True)
    div_date = DateField(column_name='divDate', null=True)
    div_yield = FloatField(column_name='divYield', null=True)
    exchange = TextField(null=True)
    exchange_name = TextField(column_name='exchangeName', null=True)
    high_price = FloatField(column_name='highPrice', null=True)
    index = IntegerField(index=True, null=True)
    last_id = TextField(column_name='lastId', null=True)
    last_price = FloatField(column_name='lastPrice', null=True)
    last_size = IntegerField(column_name='lastSize', null=True)
    low_price = FloatField(column_name='lowPrice', null=True)
    marginable = IntegerField(null=True)
    mark = FloatField(null=True)
    mark_change_in_double = FloatField(column_name='markChangeInDouble', null=True)
    mark_percent_change_in_double = FloatField(column_name='markPercentChangeInDouble', null=True)
    n_av = FloatField(column_name='nAV', null=True)
    net_change = FloatField(column_name='netChange', null=True)
    net_percent_change_in_double = FloatField(column_name='netPercentChangeInDouble', null=True)
    open_price = FloatField(column_name='openPrice', null=True)
    pe_ratio = FloatField(column_name='peRatio', null=True)
    quote_time_in_long = IntegerField(column_name='quoteTimeInLong', null=True)
    realtime_entitled = IntegerField(column_name='realtimeEntitled', null=True)
    regular_market_last_price = FloatField(column_name='regularMarketLastPrice', null=True)
    regular_market_last_size = IntegerField(column_name='regularMarketLastSize', null=True)
    regular_market_net_change = FloatField(column_name='regularMarketNetChange', null=True)
    regular_market_percent_change_in_double = FloatField(column_name='regularMarketPercentChangeInDouble', null=True)
    regular_market_trade_time_in_long = IntegerField(column_name='regularMarketTradeTimeInLong', null=True)
    security_status = TextField(column_name='securityStatus', null=True)
    shortable = IntegerField(null=True)
    symbol = TextField(null=True)
    total_volume = IntegerField(column_name='totalVolume', null=True)
    trade_time_in_long = IntegerField(column_name='tradeTimeInLong', null=True)
    volatility = FloatField(null=True)

    class Meta:
        table_name = 'quote_data'
        database = database


class MyData(BaseModel):
# This will be for personal reasons like time stamps and what not.
    pass
