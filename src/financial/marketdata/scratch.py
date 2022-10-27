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
from os import read
import time
from stockdata import Get
import sqlite3 as sql
from collections import deque
from Model.db import symbol

# Name of the databases I will use:
db = "MarketDatabase.db"
ph_db = "OneMinutePH.db"
# Create a Get() object:
get = Get()


def price_history(symbols_list, ph_db):
    """
    :param symbols_list: The list of stock symbols used to get price_history
    :param ph_db: The ph_db I want to use to store all the data

    :return: Message saying whether or not the function worked
    """
    # LETS CREATE THE FUNCTIONS THAT ARE INSIDE THIS FUNC
    # FIRST, THEN PUT TOGETHER THE LOGICAL FLOW
    # function to insert new dataframe into database
    # create SQL Query
    db = ph_db

    def _write_log(file, msg):
        with open(file, "a") as f:
            f.write(msg)
            f.close()

    def _get_price_history(symbol):
        # This is where the execute method happens
        _df = get.price_history(str(symbol))
        return _df

    def _insert_to_db(symbol, _df, db, table):
        # function to insert new dataframe into database

        conn = sql.connect(db)
        _df.to_sql(name=table, con=conn,
                   if_exists='append', index=False)
        conn.close()
        msg = "[+] One Minute Price Data Inserted for {} \n".format(symbol)
        print(msg)
        _write_log(file, msg)

    # create loop/generator to generate one symbol at a time
    # or use a list and treat it like a queue using pop each
    # time the execute method is run:

    # create a log file to log which symbols didn't save ph
    # data to the database
    file = 'ph_logs.txt'

    # get symbols list for passed arguement
    queue = deque(symbols_list)
    # start while loop
    while True:
        count = len(queue)
        print(f"[5] Retrieve Price History Data!")
        while count != 0:
            try:
                # Reminder of how many more symbols need to be
                # searched for ph data
                print("Queue Size: " + str(count))
                symbol = queue.popleft()

                # execute get method
                _df = _get_price_history(symbol)

                # Create the table name using the symbol
                table = f"{symbol}_OneMinPH"

                # insert data into db
                _insert_to_db(symbol, _df, db, table)
                count -= 1
            except KeyError as err:
                count -= 1
                msg = f"[-] Key {err} doesn't exist for {symbol} \n"
                print(msg)
                _write_log(file, msg)
            except Exception as e:
                count -= 1
                msg = f"Exception Log: \n {e}"
                print(msg)
                _write_log("docs/exception_log.txt", msg)

        print("Price history Data Saved to Database Successfully")
        break
    print('finished')


def read_file(file):
    """
    :param file: file name that I want to read line for line
    :return: a list of all the symbols that didn't work
    """
    # path to second logs:
    successful_log = "docs/success-log.txt"
    unsuccessful_log = "docs/failed-log.txt"

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


if __name__ == '__main__':

    # Time the program:
    start = time.time()

    # Create Get() object
    get = Get()
    # First check for database

    # if it exists query symbols
    companies_df = symbol(db)
    # create a list of companies in the database --- RIGHT NOW IT IS UNDER TEST I NEED TO CHANGE TO MAIN
    # insert_companies(companies_df)

    # create the quote_df to pass to the already created functions
    print(f"[1.3] Retrieve data from DataFrame's symbol column")
    _stocks = companies_df["symbol"]

    # #####################################################################
    # CREATE COMPANIES LIST:
    #####################################################################
    # NOW EXECUTE THE PRICE HISTORY FUNCTION
    price_history(_stocks, ph_db)

    # print(quote_data)
    stop = time.time()

    print("[+] Program finished in {}".format((stop - start) / 60))

    # Separate the logged data:
    f = "ph_logs.txt"
    read_file(f)

    # Now I need to figure out how to add this into the main.py
    # file and keep everything in order.
