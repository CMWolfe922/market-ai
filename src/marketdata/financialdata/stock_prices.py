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
from marketdata import tempdir

log_file = os.path.join(tempdir,__file__)
format = "{time:MM-DD-YYYY at HH:mm:ss}:{level} | {message}: "
logger.add(log_file, format=format, diagnose=True, backtrace=True, colorize=True)



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
