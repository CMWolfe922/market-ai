import sqlite3 as sql
from stockdata import Get
import os.path
from collections import deque
import pandas as pd

# CREATE A Get() OBJECT
get = Get()


# ----------------------------------------------------------- #
# CREATE FUNCTION TO INSERT PRICE HISTORY DATAFRAMES ONE AT A TIME
# ----------------------------------------------------------- #
# I need to create a function that accepts the symbols dataframe
# and then create a generator function so that I only call one symbol at a time
# create func inside func that gets the price history data and dataframe
# and saves the dataframe to a database
# then after saving to the database, pass the next symbol to the price history
# method and do this until the list of symbols is empty.

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

    def _get_price_history(symbol):
        # This is where the execute method happens
        _df = get.price_history(str(symbol))
        return _df

    def _insert_to_db(symbol, _df, db):
        # function to insert new dataframe into database

        conn = sql.connect(db)
        _df.to_sql(name='one_minute_ph', con=conn,
                   if_exists='append', index=False)
        conn.close()
        print("[+] One Minute Price Data Inserted for {}".format(symbol))

    # create loop/generator to generate one symbol at a time
    # or use a list and treat it like a queue using pop each
    # time the execute method is run:

    # get symbols list for passed arguement
    queue = deque(symbols_list)
    # start while loop
    while True:
        try:
            count = len(queue)
            while count != 0:
                print("Queue Size: " + str(count))
                symbol = queue.popleft()

                # execute get method
                _df = _get_price_history(symbol)

                # insert data into db
                _insert_to_db(symbol, _df, db)
        finally:
            pass
        print("Price history Data Saved to Database Successfully")
        break
    print('finished')


def symbol(db_name):
    """
    :param db_name: name of database to search for symbols (set name in main script)
    :description: This will hold the main logic for this mini program. It will
    check for a database, if it doesn't exist, it will call the get.companies
    method; Next it will create the database we checked for while running the
    insert_copanies method. if it does exist though, it will query the symbols
    into a list by using a sql query statement; finally it will return the symbols
    list that was generated from get.companies or _query_symbols()
    """

    # first step, create the functions:

    # ----------------------------------------------------------- #
    # CREATE FUNCTION TO CHECK IF A DATABASE EXISTS
    # ----------------------------------------------------------- #
    # use the _ if this will be used inside another function eventually
    def _check_for_db(db_name):
        """
        :param db_name: Name of the database that I am checking for
        :return: True if the file exists or False if not.
        """
        if not os.path.exists(db_name):
            print(f"[1] {db_name} doesn't exist..")
            return False
        else:
            print(f"[1] {db_name} exists..")
            return True

    # ----------------------------------------------------------- #
    # CREATE FUNCTION TO QUERY SYMBOLS FROM DB IF IT EXISTS
    # ----------------------------------------------------------- #
    def _query_symbols(db_name, table_name):
        """
        :param db_name: name of database to retrieve symbols from
        :param table_name: name of table symbols are saved in

        :return: all the stock symbols in a list to be chunked
        """
        table = table_name
        db = db_name
        symbols = []
        if os.path.exists(db):
            query_symbols = f"SELECT symbol FROM {table} "
            conn = sql.connect(db)
            cur = conn.cursor()
            for row in cur.execute(query_symbols):
                symbols.append(row)

        if len(symbols) > 19000:
            return symbols

    # ----------------------------------------------------------- #
    # CREATE FUNCTION TO INSERT COMPANY DATA FROM STOCKDATA
    # ----------------------------------------------------------- #
    def _insert_companies(company_df, db_name, table_name):
        """
        :param company_df: pandas DataFrame of list of companies
        :param db_name: name of database to insert data into
        :param table_name: name of table to save data to in database

        :return: Message stating companies were inserted correctly
        or a message saying database and table already exists. If
        table and database already exists, then the query_symbols
        function will be called
        """

        table = table_name
        db = db_name
        df = company_df

        print(f"[1.1.1] Create new database {db}.. ")
        conn = sql.connect(db)  # create database
        df.to_sql(name=table, con=conn, if_exists="replace", index=True)
        conn.close()
        print(f"[1.1.2] Insert data to {table} table in {db}.. ")
        # basically this should only work the very first time
        # the program is run and no database exists yet.

        # ================================================================================ #
        # FUNCTION BEGINS: second step, give values to needed parameter variables
        # ================================================================================ #

    table_name = "companies"

    # third step is to check for the database and assign a variable for the boolean object
    # >>> step 1.1 <<< # check if db exists
    confirmed = _check_for_db(db_name)

    # >>> step 1.2 <<< # use get.companies if db doesn't exist

    if not confirmed:  # if database doesn't exist
        print(f"[1.1] Since DB doesn't exist, call companies method..")
        company_df = get.companies()  # get company data from Get() method
        _insert_companies(company_df, db_name, table_name)  # insert the data
        return company_df

    else:  # database exists
        symbol = []
        # <<< step 1.3 >>> # query symbols from db
        symbols = _query_symbols(db_name, table_name)
        for tup in symbols:
            symbol.append(tup[0])
        print(f"[1.2] Query Symbols from {db_name}...")
        # return symbol
        data = {'symbol': symbol}
        df = pd.DataFrame(data)
        return df
