# [+] CREATE PRICE HISTORY LOOP LOGIC
# --> I may need to try and create a generator that treats
# each symbol as an object as well as each pandas dataframe
#
# I need to create a function that accepts the symbols dataframe
# and then create a generator function so that I only call one symbol at a time
# create func inside func that gets the price history data and dataframe
# and saves the dataframe to a database
# then after saving to the database, pass the next symbol to the price history
# method and do this until the list of symbols is empty.

import pandas as pd
import requests
import time
from stockdata import Get
from collections import deque
from mysql.connector import connect, Error
from Model.models import u, h, pw, db, _select_symbols
from config.secrets import one_min_ph_connect
from sqlalchemy import create_engine
import re

# ======================================================================= #
# CREATE ANALYSIS FUNCTIONS TO ANALYZE THE PH DATA:
# ======================================================================= #


def analyze(df):
    """This function will be used to analyze the ph data received"""
    df = df

    df["close_std"] = df.close.rolling(1).std()
    df[r'close_%chng'] = df.close.rolling(1).pct_change()
    df['sma_90'] = df.close.rolling(90).mean()  # 90 minute sma
    df['sma_30'] = df.close.rolling(30).mean()  # 30 minute sma
    df['sma_15'] = df.close.rolling(15).mean()  # 15 minute sma
    df['sma_5'] = df.close.rolling(5).mean()  # 5 minute sma
    df['sma_ratio'] = ((df['sma_90']/df['sma_30']) /
                       df['sma_15']) / df['sma_5']

    df['sma5_volume'] = df.volume.rolling(5).mean()
    df['sma15_volume'] = df.volume.rolling(15).mean()
    df['sma30_volume'] = df.volume.rolling(30).mean()
    df['sma90_volume'] = df.volume.rolling(90).mean()
    df['sma_volume_ratio'] = (
        (df['sma90_volume']/df['sma30_volume'])/df['sma30_volume'])/df['sma5_volume']

    # difference between open and close prices (tells if price went up or down)
    df['oc_dif'] = df['close'] - df['open']
    df['oc_std'] = df['oc_dif'].rolling(3).std()
    df[r'oc_%chng'] = df['oc_dif'].rolling(1).pct_change()
    # price fluctuation between high and low prices for each candle
    df['hl_dif'] = df['high'] - df['low']
    df['hl_std'] = df['hl_dif'].rolling(1).std()
    df[r'hl_%chng'] = df['hl_dif'].rolling(1).pct_change()
    pass


def price_data(stocks):
    """
        :param stock: company symbol/ticker
        :Example: MSFT 10 day minute 10
        :returns: raw json data (Open, High, Low, close, Volume, and Time (epoch time))
        """
    url = "https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(
        stocks)

    params = get.Params.one_minute_10day

    # Other users will need their own TD Ameritrade API Key
    params.update({"apikey": get.TDA.key})

    # request price history data
    req = requests.get(url, params=params).json()

    candles = dict(req)  # turn candles into a dict() type
    extracted_candles_list = candles["candles"]
    symbol = candles["symbol"]  # symbol of the company's price data

    # Create data frame from extracted data
    df = pd.DataFrame.from_dict(extracted_candles_list, orient="columns")
    df.rename(columns={"datetime": "unix"}, inplace=True)
    df["unix"] = [x for x in df["unix"] // 10 ** 3]

    # This is to insert the companies symbol into the data frame
    # in every row next to the unix_time so that I can identify
    # who the data belongs to.
    df["symbol"] = symbol

    return df

# ======================================================================= #
# READ FILE FUNCTION AND CREATE A SUCCESS/UNSUCCESSFUL PH EXECUTION LOG
# ======================================================================= #


def read_file(file):
    """
    :param file: file name that I want to read line for line
    :return: a list of all the symbols that didn't work
    """
    # path to second logs:
    successful_log = "success-log.txt"
    unsuccessful_log = "failed-log.txt"

    # patterns to look for
    successful = "[+]"
    unsuccessful = "[-]"
    with open(file, "r") as f:
        for line in f:
            if successful in line:  # if line contains a success msg
                sf = open(successful_log, 'a')
                sf.write(line)
            elif unsuccessful in line:
                uf = open(unsuccessful_log, 'a')
                uf.write(line)

# ====================================================================== #
# PRICE HISTORY FUNCTIONS BROKEN INTO STEPS
# ====================================================================== #


def _write_log(file, msg):
    with open(file, "a") as f:
        f.write(msg)
        f.close()


def _get_price_history(ticker):
    # This is where the execute method happens
    _df = get.price_data(str(ticker))
    return _df


# connect to MySQL using the connect uri for sqlalchemy
ph_db = "price_history"
mysql_connect = f"mysql://root:MZMfib112358!#@localhost:3306/{ph_db}"
engine = create_engine(one_min_ph_connect, echo=False)


def _insert_to_db(_df, table):
    # function to insert new dataframe into database
    _df.to_sql(name=table, con=engine, if_exists='append')


# ======================================================================= #
# REGEX FUNCTIONS TO EXTRACT DATA FROM THE LOGS
# ======================================================================= #
def read_bad_log(file):
    """
    :param file: file name that I want to read line for line
    :return: a list of all the symbols that didn't work
    """
    bad_list = []
    # [+] regex pattern:
    pattern = re.compile(r"[A-Z]+")
    with open(file, "r") as f:
        for line in f:
            m = re.findall(pattern, line)
            bad_list.append(m)
    return bad_list


def extract_failed_symbols():
    file = "failed-log.txt"
    bad_log = read_bad_log(file)
    bad_list = []
    for lists in bad_log:
        bad_list.append(lists[1])
    return bad_list

# Create a main function just for the steps to shorten the loop:


def main(ticker, logfile):
    table = "minute_data"
    msg = "[+] One Minute Price Data Inserted for {} \n".format(ticker)
    # step 2
    df = _get_price_history(ticker)
    # Take a slight break to complete this step
    time.sleep(.1)
    # step 3
    _insert_to_db(df, engine, table)
    time.sleep(.1)
    # step 4
    print(msg)
    # step 5
    _write_log(logfile, msg)


def one_minute_data(symbols_list, ph_db):
    """
    :param symbols_list: The list of stock symbols used to get price_history
    :param ph_db: The ph_db I want to use to store all the data
    :return: Message saying whether or not the function worked
    """
    # create a log file to log which symbols didn't save ph
    # data to the database
    file = 'ph_logs.txt'

    # get symbols list for passed arguement
    queue = deque(symbols_list)
    # start while loop
    count = len(queue)
    print(f"[5] Retrieve Price History Data!")
    while count != 0:
        try:
            # TRY A FOR LOOP AND USE MAIN() FUNCTION
            # TO EXECUTE THE STEPS:
            # step 1
            print("Queue Size: " + str(count))
            ticker = queue.popleft()
            print(ticker)
            table = f"{ticker}".lower()
            file = 'ph_logs.txt'
            msg = "[+] One Minute Price Data Inserted for {} \n".format(ticker)
            # step 2
            df = _get_price_history(ticker)
            # step 3
            _insert_to_db(df, engine, table)
            # step 4
            print(msg)
            # step 5
            _write_log(file, msg)
            # Read Log and make decision
            with open(file, 'r') as f:
                for line in f:
                    if "[-]" in line:
                        time.sleep(.25)
                        redo_msg = f"{ticker} \n"
                        _write_log("redo.txt", redo_msg)
                    elif "[+]" in line:
                        pass
            count -= 1
        except KeyError as err:
            count -= 1
            msg = f"[-] Key {err} doesn't exist for {ticker} \n"
            print(msg)
            _write_log(file, msg)
        except Exception as e:
            count -= 1
            msg = f"Exception Log: \n {e}"
            print(msg)
            _write_log("docs/exception_log.txt", msg)

    print("Price history Data Saved to Database Successfully")
    print('finished')


if __name__ == '__main__':

    start = time.time()  # Time the program:
    get = Get()  # Create Get() object
    # print(f"[1.3] Retrieve data from DataFrame's symbol column")
    _stocks = _select_symbols()
    queue = deque(_stocks)  # create queue
    count = len(queue)
    logfile = 'main-log.txt'
    print("[5] Execute Price History Loop: ")
    while queue:
        try:
            print("Queue Size: " + str(count))
            ticker = queue.popleft()
            main(ticker, logfile)

            rest = 300
            if rest > 0:
                rest -= 1
                pass
            else:
                print(f"[+] Take 10 second break...")
                time.sleep(10)  # take 10 second nap
                rest += 300  # reset rest
            count -= 1

            # Hopefully this will restart the whole loop
            # if it keeps failing to execute every symbol
            # the first time.
            if count == 0:
                try:
                    uccessful_log = "success-log.txt"
                    unsuccessful_log = "failed-log.txt"

                    # Separate the logged data:
                    read_file(logfile)
                    # read the bad logs
                    failed_symbols = extract_failed_symbols()
                    queue = deque(failed_symbols)
                    count = len(queue)
                except Exception as e:
                    print(e)

        except KeyError as err:
            count -= 1
            msg = f"[-] Key {err} doesn't exist for {ticker} \n"
            print(msg)
            _write_log(logfile, msg)
        except Exception as e:
            count -= 1
            msg = f"Exception Log: \n {e}"
            print(msg)
            _write_log("exception-log.txt", msg)

    # print(quote_data)
    stop = time.time()
