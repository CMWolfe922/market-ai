#!/usr/bin/env python3

# Functions for accessing stock price history data, The
# functions or methods should return a DataFrame or
# be returned in JSON format. Using JSON format
# will make it easier to store the stock price history data
# into MongoDB
#
# DataFrame data will be stored in MySQL or PostgreSQL database.


import requests, os, json
import pandas as pd
from loguru import logger
from time import time
from datetime import datetime

PATH = "../tmp/"
FILE = "scraper.log"
LOG_FILE = os.path.join(PATH, FILE)
logger.add(LOG_FILE, format="{time:MM/DD/YYYY at HH:mm:ss} | {level} | {name} | {message}", diagnose=True, backtrace=True)


today = datetime.today()
today_fmt = today.strftime("%m-%d-%Y")
BASE = "https://api.tdameritrade.com/v1/"



def price_history(symbol, apikey, params:dict):
    """
    :param stock: company symbol/ticker
    :Example: MSFT 10 day minute 10

    :returns: raw json data (Open, High, Low, close, Volume, and Time (epoch time))
    """
    url = "https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(
        symbol
    )

    params = params

    # Other users will need their own TD Ameritrade API Key
    params.update({"apikey": apikey})

    # request price history data
    req = requests.get(url, params=params).json()

    candles = dict(req)  # turn candles into a dict() type
    extracted_candles_list = candles["candles"]
    symbol = candles["symbol"]  # symbol of the compan's price data

    # Create data frame from extracted data
    df = pd.DataFrame.from_dict(extracted_candles_list, orient="columns")
    df.rename(columns={"datetime": "unix"}, inplace=True)
    df["unix"] = [x for x in df["unix"] // 10 ** 3]

    # This is to insert the companies symbol into the data frame
    # in every row next to the unix_time so that I can identify
    # who the data belongs to.
    # df["symbol"] = symbol I DONT NEED THIS RIGHT NOW

    return df


def quotes(apikey, stocks):
    """
    :param stocks: list of stock symbols
    :return: raw json data to be passed to the
    """
    url = BASE + "marketdata/quotes"  # market data url
    params = {"apikey": apikey, "symbol": stocks}
    request = requests.get(url=url, params=params).json()

    time.sleep(1)  # set sleep so that api works

    # create df
    df = pd.DataFrame.from_dict(
        request, orient="index").reset_index(drop=True)

    # Quote Data: formatting the dates and other columns
    # Now I need to add the dates and format the dates for the database
    df["date"] = pd.to_datetime(today_fmt)
    df["date"] = df["date"].dt.date
    df["divDate"] = pd.to_datetime(df["divDate"])
    df["divDate"] = df["divDate"].dt.date

    # Remove anything without a price
    df = df.loc[df["bidPrice"] > 0]

    # Rename columns, They can't start with a number
    df = df.rename(
        columns={"52WkHigh": "_52WkHigh", "52WkLow": "_52WkLow"})

    return df


def fundamentals(apikey, stocks):
    """
    :param stocks: List of stocks chunked into 200 symbol chunks

    :return: This will return tons of information that will then
    be changed into dataframes and inserted into the database.
    """
    url = BASE + "instruments"

    # pass params
    params = {"apikey": apikey, "symbol": stocks,
                "projection": "fundamental"}

    request = requests.get(url=url, params=params).json()

    time.sleep(1)

    # create df
    _df = pd.DataFrame.from_dict(
        request, orient="index").reset_index(drop="True")

    def _reshape_fundamentals(df):

        _fund_list = list(df["fundamental"])
        _df = pd.DataFrame([x for x in _fund_list])
        return _df

    df = _reshape_fundamentals(_df)

    return df
