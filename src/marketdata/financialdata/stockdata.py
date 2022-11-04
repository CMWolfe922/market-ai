# /usr/bin/.venv python3
# I can't import the required secrets from config.secrets in order to actually execute
# these functions. Required: TDA apikey, consumer_id, username, password
#
# There for I am going to make it a Get class parameter and have it passed to Get
# at that point. From there a class variable will make it available to each
# method.
#
# # This script contains the logic for extracting the stock market data that
# you want to download/write to a database.
#
# remember that I need to make sure that the params for pricehistory should
# be choices for people. so they can choose their own params without picking
# unauthorized params
import os
from bs4 import BeautifulSoup as bs
import string
import requests
import pandas as pd
from datetime import datetime, timezone
import time
import os.path
import sqlite3 as sql

time.tzname[time.localtime().tm_isdst]

BASE = "https://api.tdameritrade.com/v1/"

start = time.time()
# fmt_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(epoch_time))
today = datetime.today()
today_fmt = today.strftime("%m-%d-%Y")
print(today)
print(today_fmt)

#####################################################################
# NEXT STEP CHUNK LIST OF COMPANIES
#####################################################################
# ---> [2] This function chunks the list of symbols into groups of 200
def chunks(l, n):
    """
    :description: Takes in a list of symbols, string items, or integers, and
    then creates multiple lists inside of the initial list. Each list containing
    the number of items specified with the n parameter.

    :param l: takes in a list of items that need to be chunked into groups.
    :param n: This is the size of the chunked items. Lets you know how many
    items to put into each chunk.
    """
    n = max(1, n)
    return (l[i: i + n] for i in range(0, len(l), n))


# Break the symbols up into chunks
# companies_chunked = list(chunks(list(set(_symbols)), 200))
# NYSE_chunked = list(chunks(list(set(NYSE_df['symbol'])), 200))
# NASDAQ_chunked = list(chunks(list(set(NASDAQ_df['symbol'])), 200))
# AMEX_chunked = list(chunks(list(set(AMEX_df['symbol'])), 200))
# OTCBB_chunked = list(chunks(list(set(OTCBB_df['symbol'])), 200))


#####################################################################
# CREATE THE PARAM CLASS:
#####################################################################
# ---> [3] HOLDS PARAMS FOR METHODS IN OTHER CLASSES
class Params:
    # CREATE THE DIFFERENT PARAMS AS ATTRIBUTES TO BE
    # PASSED TO THE TDA CLASS THEN USED IN THEIR
    # METHODS TO CREATE DIFFERENT METHOD CALLS

    #####################################################################
    # CREATE GET COMPANIES FUNCTION:
    #####################################################################

    one_minute_10day = {
        "symbol": "stocks",  # DON'T CHANGE, change stocks exchange param in cleaned_symbols func
        "period": "10",  # 1,2,3,4,5,10
        "periodType": "day",  # day, week, month, year, ytd
        "frequency": "1",  # minute=1,5,10,15,30; daily=1, weekly=1, monthly=1
        "frequencyType": "minute",  # minute, daily, weekly, monthly
        "needExtendedHoursData": "false",
    }

    one_minute_daily = {
        "symbol": "stocks",  # DON'T CHANGE, change stocks exchange param in cleaned_symbols func
        "period": "1",  # 1,2,3,4,5,10
        "periodType": "day",  # day, week, month, year, ytd
        "frequency": "1",  # minute=1,5,10,15,30; daily=1, weekly=1, monthly=1
        "frequencyType": "minute",  # minute, daily, weekly, monthly
        "needExtendedHoursData": "false",
    }

    one_year_daily = {
        "symbol": "stocks",  # DON'T CHANGE, change stocks exchange param in cleaned_symbols func
        "period": "1",  # 1,2,3,4,5,10
        "periodType": "year",  # day, week, month, year, ytd
        "frequency": "1",  # minute=1,5,10,15,30; daily=1, weekly=1, monthly=1
        "frequencyType": "daily",  # minute, daily, weekly, monthly
        "needExtendedHoursData": "false",
    }

    ten_year_daily = {
        "symbol": "stocks",  # DON'T CHANGE, change stocks exchange param in cleaned_symbols func
        "period": "10",  # 1,2,3,4,5,10
        "periodType": "year",  # day, week, month, year, ytd
        "frequency": "1",  # minute=1,5,10,15,30; daily=1, weekly=1, monthly=1
        "frequencyType": "daily",  # minute, daily, weekly, monthly
        "needExtendedHoursData": "false",
    }

    max_daily = {
        "symbol": "stocks",  # DON'T CHANGE, change stocks exchange param in cleaned_symbols func
        "period": "20",  # 1,2,3,4,5,10,15,20
        "periodType": "day",  # day, week, month, year, ytd
        "frequency": "1",  # minute=1,5,10,15,30; daily=1, weekly=1, monthly=1
        "frequencyType": "daily",  # minute, daily, weekly, monthly
        "needExtendedHoursData": "false",
    }


# TODO: CREATE CLI METHOD TO GET PARAMS


class TDA(Params):
    """
    [+] TD Ameritrade methods
    -  price_history, quotes, fundamentals, instrument
    """

    # class variables
    BASE = "https://api.tdameritrade.com/v1/"

    # instantiate this class with a apikey parameter
    def __init__(self, apikey):
        self.apikey = apikey


    def price_history(self, stocks):
        """
        :param stock: company symbol/ticker
        :Example: MSFT 10 day minute 10

        :returns: raw json data (Open, High, Low, close, Volume, and Time (epoch time))
        """
        url = "https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(
            stocks
        )

        params = Params.one_minute_10day

        # Other users will need their own TD Ameritrade API Key
        params.update({"apikey": self.apikey})

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

    def quotes(self, stocks):
        """
        :param stocks: list of stock symbols
        :return: raw json data to be passed to the
        """
        url = BASE + "marketdata/quotes"  # market data url
        params = {"apikey": self.apikey, "symbol": stocks}
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

    def fundamentals(self, stocks):
        """
        :param stocks: List of stocks chunked into 200 symbol chunks

        :return: This will return tons of information that will then
        be changed into dataframes and inserted into the database.
        """
        url = BASE + "instruments"

        # pass params
        params = {"apikey": self.apikey, "symbol": stocks,
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


#####################################################################
# CREATE THE GET CLASS:
#####################################################################
# ---> [5] BASE CLASS THAT MAKES GET CALLS LIKE: get.price_history()
class Get(TDA):
    """
    [+] This is a BASE class:
    [+] Class is for sending GET calls to different apis online. The Class
    variables will hold the api information, and the urls to send GET calls
    to.
    [+] Class methods are for utilizing the apis of different apis
    """

    # instantiate the inherited TDA class
    def __init__(self, apikey):
        self.apikey = apikey

    #####################################################################
    # NEXT STEP CHUNK LIST OF COMPANIES
    #####################################################################
    # ---> [2] This function chunks the list of symbols into groups of 200

    def chunks(self, l, n):
        """
        :description: Takes in a list of symbols, string items, or integers, and
        then creates multiple lists inside of the initial list. Each list containing
        the number of items specified with the n parameter.

        :param l: takes in a list of items that need to be chunked into groups.
        :param n: This is the size of the chunked items. Lets you know how many
        items to put into each chunk.
        """
        n = max(1, n)
        print(f"[2] Chunk symbols into groups of 200..")
        return (l[i: i + n] for i in range(0, len(l), n))

    #####################################################################
    # CREATE GET COMPANIES FUNCTION:
    #####################################################################

    def companies(self):

        exchanges = ["NYSE", "NASDAQ", "AMEX", "OTCBB"]

        def get_companies(exchange="NYSE"):
            """
            :param exchange: The Stock exchange for which you want
            to get a current list of all the symbols for.
            Default -> NYSE

            :returns: a list of tuples containing every company name and symbol in
            the market exchange passed to the function
            """
            alpha = list(string.ascii_uppercase)

            symbols = []
            name = []

            # loop through the letters in the alphabet to get the stocks on each page
            # from the table and store them in a list
            for each in alpha:
                url = "http://eoddata.com/stocklist/{}/{}.htm".format(
                    exchange, each)
                resp = requests.get(url)
                site = resp.content
                soup = bs(site, 'html.parser')
                table = soup.find('table', {'class': 'quotes'})
                for row in table.findAll('tr')[1:]:
                    symbols.append(row.findAll('td')[0].text.rstrip())
                for row in table.findAll('tr')[1:]:
                    name.append(row.findAll('td')[1].text.rstrip())

            # remove the extra letters on the end of the symbols
            symbols_clean = []
            name_clean = []

            for each in symbols:
                each = each.replace('.', '-')
                symbols_clean.append((each.split('-')[0]))

            for each in name:
                each = each.replace('.', '-')
                name_clean.append((each.split('-')[0]))

            return name_clean, symbols_clean

        NYSE_company, NYSE_symbol = get_companies(exchanges[0])
        NASDAQ_company, NASDAQ_symbol = get_companies(exchanges[1])
        AMEX_company, AMEX_symbol = get_companies(exchanges[2])
        OTCBB_company, OTCBB_symbol = get_companies(exchanges[3])

        columns = ["exchange", "symbol", "name"]

        # New York Stock Exchange companies
        NYSE = list(zip(NYSE_symbol, NYSE_company))
        NYSE = [("NYSE",) + elem for elem in NYSE]
        NYSE_df = pd.DataFrame([x for x in NYSE], columns=columns)

        # NASDAQ Companies
        NASDAQ = list(zip(NASDAQ_symbol, NASDAQ_company))
        NASDAQ = [("NASDAQ",) + elem for elem in NASDAQ]
        NASDAQ_df = pd.DataFrame([x for x in NASDAQ], columns=columns)

        # American Stock Exchange Companies
        AMEX = list(zip(AMEX_symbol, AMEX_company))
        AMEX = [("AMEX",) + elem for elem in AMEX]
        AMEX_df = pd.DataFrame([x for x in AMEX], columns=columns)

        # Over the Counter Bulletin Board Exchange "Pink Sheets"
        # These are the penny stocks and I think their is a lot of
        # possibilities with finding a niche in here
        OTCBB = list(zip(OTCBB_symbol, OTCBB_company))
        OTCBB = [("OTCBB",) + elem for elem in OTCBB]
        OTCBB_df = pd.DataFrame([x for x in OTCBB], columns=columns)

        # Now we append all the dataframes together so that we have
        # one massive master list. Also, the good think is we can still
        # use the smaller datasets if need be.

        companies_df = NYSE_df.append(NASDAQ_df)
        companies_df = companies_df.append(AMEX_df)
        companies_df = companies_df.append(OTCBB_df)

        # Now check for duplicates and drop them from the main dataset
        companies_df = companies_df.drop_duplicates(
            subset="symbol", keep="first")
        companies_df = companies_df.drop_duplicates(
            subset="name", keep="first")

        return companies_df

# =========================================================== #
# [+] THIS IS THE END OF THE `marketdata` VERSION OF STOCKDATA
# AND THE BEGINNING OF WHERE WE ADD click FUNCTIONALITY:
# =========================================================== #
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


# =========================================================== #
# Building new stock data functions to get the data I need
# Some of these will be scraping the internet for the
# data needed.
# =========================================================== #
