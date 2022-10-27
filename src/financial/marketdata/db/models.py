import sqlite3 as sql
import pandas as pd

##################################################################################
# ====================NAME DATABASE IN THE MAIN FILE!!!!======================== #
##################################################################################

# SQL Query to insert the quote data into the database.


def insert_quote_data(quote_df, db):
    """
    :param quote_df: Quote Data Dataframe
    :param db: database connection variable
    """
    try:
        conn = sql.connect(db)
        quote_df.to_sql(name="QuoteData", con=conn,
                        if_exists="append", index=False)
        conn.close()
        print("[4.1] Quote Data Inserted")
    except:
        raise ValueError(
            "[-] Data not inserted correctly. Make sure datatype is correct"
        )


# SQL Query to insert the fundamental data into the database.
def insert_fundamental_data(fun_df, db):
    """
    :param fun_df: Quote Data Dataframe
    :param db: database connection variable
    """
    try:
        conn = sql.connect(db)
        fun_df.to_sql(name="FundamentalData", con=conn,
                      if_exists="append", index=False)
        conn.close()
        print("[4.1] Fundamental Data Inserted")
    except:
        raise ValueError(
            "[-] Data not inserted correctly. Make sure it was a string object."
        )


# TODO: INSERT THE IMPORTED QUOTE AND FUNDAMENTAL DATA INTO THE DATABASE
def insert_quote_and_fundamental_data(quote_data, fundamental_data, db):
    """
    :param quote_data: the quote data from the tdameritrade api
    :param fundamental_data: the fundamental data from the tdameritrade api
    """
    # [1] use the insert_quote_data function imported from models.py
    # to insert quote data into the database.
    insert_quote_data(quote_data, db)

    # [2] use the insert_fundamental_data function imported from models.py
    # to insert fundamental data into the database.
    insert_fundamental_data(fundamental_data, db)
