import sqlite3 as sql
from time import time
import pandas as pd
import os
from loguru import logger


market_db_path = '/home/blackbox/projects/finance/market-ai/src/marketdata/data/marketdata.db'
ph_db_path = '/home/blackbox/projects/finance/market-ai/src/marketdata/data/pricehistory.db'

# ----------------------------------------------------------- #
# CREATE FUNCTION TO INSERT COMPANY DATA FROM STOCKDATA
# ----------------------------------------------------------- #
def _insert_companies(company_df, db_name=market_db_path, table_name="companies"):
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

    logger.info("[+] Create new database {}.. ", db)
    conn = sql.connect(db)  # create database
    df.to_sql(name=table, con=conn, if_exists="replace", index=True)
    conn.close()
    logger.success("[+] Inserted data to {} table in {}.. ", table, db)
    # basically this should only work the very first time
    # the program is run and no database exists yet.


# ----------------------------------------------------------- #
# CREATE FUNCTION TO QUERY SYMBOLS FROM DB
# ----------------------------------------------------------- #


def _query_symbols(path=market_db_path):
    """
    :param db_path: name of database to retrieve symbols from
    :param table_name: name of table symbols are saved in
    :return: all the stock symbols in a list to be chunked
    """
    table = "companies"
    db = path
    symbols = []
    if os.path.exists(db):
        query_symbols = f"SELECT symbol FROM {table} "
        conn = sql.connect(db)
        cur = conn.cursor()
        for row in cur.execute(query_symbols):
            symbols.append(row)

        if len(symbols) > 14000:
            logger.success("[+] All symbols retrieved")
    cleaned_symbols = [each[0] for each in symbols]
    return cleaned_symbols



# ----------------------------------------------------------- #
# CREATE FUNCTION THAT UTILIZES THE _query_symbols FUNC TO
# YIELD 1 SYMBOL AT A TIME.
# ----------------------------------------------------------- #

def generate_symbols():
    data = _query_symbols()
    symbols = [stock[0] for stock in data]
    for symbol in symbols:
        yield symbol

# THIS VERSION IS FOR SERVER SIDE DATABASES. UNLIKE THE
# SQLITE ONE ABOVER, THIS WILL NEED TO GET THE NAME
# OF THE DATABASE ATLEAST

# def _query_symbols(db_path, table_name):
#     """
#     :param db_path: name of database to retrieve symbols from
#     :param table_name: name of table symbols are saved in

#     :return: all the stock symbols in a list to be chunked
#     """
#     table = table_name
#     db = db_path
#     symbols = []
#     if os.path.exists(db):
#         query_symbols = f"SELECT symbol FROM {table} "
#         conn = sql.connect(db)
#         cur = conn.cursor()
#         for row in cur.execute(query_symbols):
#             symbols.append(row)

#         if len(symbols) > 19000:
#             print("[+] Queried Symbols")
#             return symbols


def insert_price_data(table_name, df):
    db = ph_db_path
    conn = sql.connect(db)
    df.to_sql(name=table_name, con=conn, if_exists="append", index=False)
    conn.close()
    logger.success("[+] Price Data inserted")


# ========================================================================================== #
# FUNCTIONS TO INSERT QUOTE AND FUNDAMENTAL DATA INTO THE MARKETDATA DATABASE
# ========================================================================================== #

# FUNCTION TO INSERT QUOTE DATA INTO DATABASE
def insert_quote_data(quote_df, db_name=market_db_path):
    """
    :param quote_df: Quote Data Dataframe
    :param engine: database connection variable for mysql
    """
    try:
        conn = sql.connect(db_name)
        quote_df.to_sql(name="quote_data", con=conn,
                        if_exists="append", index=False)
        logger.info("[+] Quote data inserted successfully")
    except:
        logger.error("[-] Quote data not inserted correctly")
        raise ValueError(
            "[-] Data not inserted correctly. Make sure datatype is correct"
        )


# FUNCTION TO INSERT FUNDAMENTAL DATA INTO DATABASE
def insert_fundamental_data(fun_df, db_name=market_db_path):
    """
    :param fun_df: Quote Data Dataframe
    :param db: database connection variable
    """
    try:
        conn = sql.connect(db_name)
        fun_df.to_sql(name="fundamental_data", con=conn,
                      if_exists="append", index=False)
        logger.info("[+] Fundamental Data Inserted")
    except:
        logger.error("[-] Fundamental data not inserted correctly")
        raise ValueError(
            "[-] Data not inserted correctly. Make sure it was a string object."
        )


# FUNCTION TO INSERT THE IMPORTED QUOTE AND FUNDAMENTAL DATA INTO THE DATABASE
def insert_quote_and_fundamental_data(quote_data, fundamental_data, db_name=market_db_path):
    """
    :param quote_data: the quote data from the tdameritrade api
    :param fundamental_data: the fundamental data from the tdameritrade api
    """
    # [1] use the insert_quote_data function imported from models.py
    # to insert quote data into the database.
    insert_quote_data(quote_data, db_name)

    # [2] use the insert_fundamental_data function imported from models.py
    # to insert fundamental data into the database.
    insert_fundamental_data(fundamental_data, db_name)


# --------
