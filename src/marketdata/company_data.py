#!/usr/bin/env python3

# Functions for accessing stock price history data, The
# functions or methods should return a DataFrame or
# be returned in JSON format. Using JSON format
# will make it easier to store the stock price history data
# into MongoDB
#
# DataFrame data will be stored in MySQL or PostgreSQL database.


from pytz import timezone
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
TDA_BASE = "https://api.tdameritrade.com/v1/"
TDA_APIKEY = os.environ.get('TDA_APIKEY')

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


# QUOTE DATA FROM TD AMERITRADE
# This script is responsible for creating a class for
# retrieving quote data


# DATE BUILDING AND MANAGEMENT
today = datetime.today().astimezone(timezone("US/Central"))
today_fmt = today.strftime("%m-%d-%Y")

# CREATE THE LOGGER FOR THIS SCRIPT:
log_path = str(os.path.pardir) + '/logs/'
base_fmt = "[{time:YYYY-MM-DD at HH:mm:ss}]|[{name}-<lvl>{message}</lvl>]"
logger.add(log_path+"quotes.log", rotation="2 MB",
           colorize=True, enqueue=True, catch=True)

class Quote:

    def __init__(self, stocks: list):
        self.stocks = stocks
        self.stock_chunks = self.chunks(stocks) # Chunks the stock list upon instantiation
        # self.engine = create_marketdata_engine() # Creates a database connection engine upon instantiation

        # This function chunks the list of symbols into groups of 200
    def chunks(self, l: list, n: int = 200):
        """
        :param l: takes in a list
        :param n: Lets you know how long you want each chunk to be
        """
        n = max(1, n)
        logger.info("[+] Stocks chunked into groups of 200..")
        return (l[i: i + n] for i in range(0, len(l), n))

    def data(self, stock):
        """
        :param stock: a stock symbol
        :return: raw json data to be passed to the
        """
        url = TDA_BASE + "marketdata/quotes"  # market data url
        params = {"apikey": TDA_APIKEY, "symbol": stock}
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

    def execute_main(self):
        """
        :Description: Main method to obtain Quote data for every stock in the stocks list
        passed to the Quotes() class when instantiated. This method will execute the
        Quote.data method using a chunked stocks list.
        """
        logger.info("[-] Executing the main Quote Object Method")
        try:
            quote_data = pd.concat([self.data(each)
                                   for each in self.stock_chunks])
            logger.info("[+] Quote Data Received")
            return quote_data

        except Exception as e:
            logger.error("Error Caused Due to {}", e)


class Fundamental:

    def __init__(self, stocks: list):
        self.stocks = stocks
        self.stock_chunks = self.chunks(stocks)
        # self.engine = create_marketdata_engine()

    # This function chunks the list of symbols into groups of 200
    def chunks(self, l: list, n: int = 200):
        """
        :param l: takes in a list
        :param n: Lets you know how long you want each chunk to be
        """
        n = max(1, n)
        logger.info("[+] Stocks chunked into groups of 200..")
        return (l[i: i + n] for i in range(0, len(l), n))

    def data(self, stock):
        """
        :param stocks: List of stocks chunked into 200 symbol chunks
        :return: This will return tons of information that will then
        be changed into dataframes and inserted into the database.
        """
        url = TDA_BASE + "instruments"

        # pass params
        params = {"apikey": TDA_APIKEY, "symbol": stock,
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

    def execute_main(self):
        """
        :Description: Main method to obtain Fundamental data for every stock in the stocks list
        passed to the Fundamental() class when instantiated. This method will execute the
        Fundamental.data method using a chunked stocks list.
        """
        logger.info("[-] Executing the main Fundamental Object Method")
        try:
            fundamental_data = pd.concat([self.data(each)
                                   for each in self.stock_chunks])
            logger.info("[+] Fundamental Data Received")
            # insert_fundamental_data_mysql(fundamental_data, self.engine)
            return fundamental_data

        except Exception as e:
            logger.error("Error Caused Due to {}", e)
